"""
GARCH Model Implementation
Handles GARCH model fitting, forecasting, and diagnostics.
"""

import numpy as np
import pandas as pd
from arch import arch_model
from arch.univariate import GARCH
import warnings
warnings.filterwarnings('ignore')

class GARCHModel:
    """Class for GARCH model operations."""
    
    def __init__(self):
        """Initialize GARCH model handler."""
        self.model = None
        self.fitted_model = None
    
    def fit_garch(self, returns, p=1, q=1, dist='normal'):
        """
        Fit GARCH model to returns data.
        
        Parameters:
        -----------
        returns : pd.Series or np.array
            Log returns time series
        p : int
            GARCH order (default: 1)
        q : int
            ARCH order (default: 1)
        dist : str
            Error distribution (default: 'normal')
            
        Returns:
        --------
        model_fit : arch model fit object
            Fitted GARCH model
        """
        try:
            # Remove any NaN values
            returns_clean = pd.Series(returns).dropna()
            
            # Check if we have enough data
            if len(returns_clean) < 50:
                raise ValueError("Insufficient data for GARCH modeling (minimum 50 observations required)")
            
            # Scale returns to percentage (arch expects this)
            returns_scaled = returns_clean * 100
            
            # Create GARCH model
            self.model = arch_model(
                returns_scaled,
                vol='GARCH',
                p=p,
                q=q,
                dist=dist
            )
            
            # Fit the model
            self.fitted_model = self.model.fit(disp='off', show_warning=False)
            
            return self.fitted_model
            
        except Exception as e:
            print(f"Error fitting GARCH model: {str(e)}")
            return None
    
    def forecast_volatility(self, model_fit, horizon=5):
        """
        Generate volatility forecasts.
        
        Parameters:
        -----------
        model_fit : arch model fit object
            Fitted GARCH model
        horizon : int
            Number of periods to forecast
            
        Returns:
        --------
        dict : Dictionary containing forecasts
        """
        try:
            # Generate forecasts
            forecasts = model_fit.forecast(horizon=horizon, method='simulation', simulations=1000)
            
            # Extract variance forecasts
            variance_forecast = forecasts.variance.values[-1, :]
            
            # Convert to volatility (standard deviation)
            volatility_forecast = np.sqrt(variance_forecast)
            
            # Convert back from percentage scale
            volatility_forecast = volatility_forecast / 100
            variance_forecast = variance_forecast / 10000
            
            return {
                'volatility_forecast': volatility_forecast,
                'variance_forecast': variance_forecast,
                'forecast_horizon': horizon
            }
            
        except Exception as e:
            print(f"Error generating forecasts: {str(e)}")
            return None
    
    def get_model_summary(self, model_fit):
        """
        Extract model summary statistics.
        
        Parameters:
        -----------
        model_fit : arch model fit object
            Fitted GARCH model
            
        Returns:
        --------
        dict : Dictionary containing model summary
        """
        try:
            # Extract parameters
            params = model_fit.params
            
            # Model statistics
            aic = model_fit.aic
            bic = model_fit.bic
            loglikelihood = model_fit.loglikelihood
            
            # Parameter dictionary
            param_dict = {}
            for param_name, param_value in params.items():
                param_dict[param_name] = param_value
            
            return {
                'parameters': param_dict,
                'aic': aic,
                'bic': bic,
                'loglikelihood': loglikelihood,
                'num_observations': model_fit.nobs
            }
            
        except Exception as e:
            print(f"Error extracting model summary: {str(e)}")
            return None
    
    def calculate_residuals(self, model_fit):
        """
        Calculate standardized residuals.
        
        Parameters:
        -----------
        model_fit : arch model fit object
            Fitted GARCH model
            
        Returns:
        --------
        pd.Series : Standardized residuals
        """
        try:
            # Get residuals and conditional volatility
            residuals = model_fit.resid
            conditional_volatility = model_fit.conditional_volatility
            
            # Calculate standardized residuals
            standardized_residuals = residuals / conditional_volatility
            
            return standardized_residuals
            
        except Exception as e:
            print(f"Error calculating residuals: {str(e)}")
            return None
    
    def ljung_box_test(self, model_fit, lags=10):
        """
        Perform Ljung-Box test on standardized residuals.
        
        Parameters:
        -----------
        model_fit : arch model fit object
            Fitted GARCH model
        lags : int
            Number of lags for test
            
        Returns:
        --------
        dict : Test results
        """
        try:
            from scipy.stats import chi2
            
            # Get standardized residuals
            std_residuals = self.calculate_residuals(model_fit)
            
            if std_residuals is None:
                return None
            
            # Calculate squared residuals
            squared_residuals = std_residuals ** 2
            
            # Ljung-Box test statistic
            n = len(squared_residuals)
            autocorr = []
            
            for lag in range(1, lags + 1):
                corr = squared_residuals.autocorr(lag)
                autocorr.append(corr)
            
            # Calculate test statistic
            lb_stat = n * (n + 2) * sum([(autocorr[i] ** 2) / (n - i - 1) for i in range(lags)])
            
            # p-value
            p_value = 1 - chi2.cdf(lb_stat, lags)
            
            return {
                'test_statistic': lb_stat,
                'p_value': p_value,
                'lags': lags,
                'critical_value': chi2.ppf(0.95, lags)
            }
            
        except Exception as e:
            print(f"Error performing Ljung-Box test: {str(e)}")
            return None
    
    def arch_lm_test(self, model_fit, lags=5):
        """
        Perform ARCH-LM test for remaining heteroscedasticity.
        
        Parameters:
        -----------
        model_fit : arch model fit object
            Fitted GARCH model
        lags : int
            Number of lags for test
            
        Returns:
        --------
        dict : Test results
        """
        try:
            from scipy.stats import chi2
            
            # Get standardized residuals
            std_residuals = self.calculate_residuals(model_fit)
            
            if std_residuals is None:
                return None
            
            # Calculate squared residuals
            squared_residuals = std_residuals ** 2
            
            # Create lagged variables
            n = len(squared_residuals)
            X = np.ones((n - lags, lags + 1))  # Include intercept
            
            for i in range(lags):
                X[:, i + 1] = squared_residuals.iloc[lags - i - 1:n - i - 1].values
            
            y = squared_residuals.iloc[lags:].values
            
            # OLS regression
            try:
                beta = np.linalg.solve(X.T @ X, X.T @ y)
                fitted_values = X @ beta
                ssr = np.sum((y - fitted_values) ** 2)
                tss = np.sum((y - np.mean(y)) ** 2)
                r_squared = 1 - ssr / tss
                
                # Test statistic
                lm_stat = (n - lags) * r_squared
                p_value = 1 - chi2.cdf(lm_stat, lags)
                
                return {
                    'test_statistic': lm_stat,
                    'p_value': p_value,
                    'lags': lags,
                    'critical_value': chi2.ppf(0.95, lags)
                }
                
            except np.linalg.LinAlgError:
                return None
                
        except Exception as e:
            print(f"Error performing ARCH-LM test: {str(e)}")
            return None
