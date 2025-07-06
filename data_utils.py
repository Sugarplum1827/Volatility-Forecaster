"""
Data Utilities
Handles data fetching, processing, and statistical calculations.
"""

import pandas as pd
import numpy as np
import yfinance as yf
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

class DataProcessor:
    """Class for data processing operations."""
    
    def __init__(self):
        """Initialize data processor."""
        pass
    
    def fetch_stock_data(self, ticker, start_date, end_date):
        """
        Fetch stock data from Yahoo Finance.
        
        Parameters:
        -----------
        ticker : str
            Stock ticker symbol
        start_date : datetime
            Start date for data
        end_date : datetime
            End date for data
            
        Returns:
        --------
        pd.DataFrame : Stock price data
        """
        try:
            # Create yfinance ticker object
            stock = yf.Ticker(ticker)
            
            # Download historical data
            data = stock.history(start=start_date, end=end_date)
            
            # Check if data is empty
            if data.empty:
                raise ValueError(f"No data found for ticker {ticker}")
            
            # Check for sufficient data
            if len(data) < 50:
                raise ValueError(f"Insufficient data for {ticker}. Found {len(data)} observations, need at least 50.")
            
            # Remove any rows with NaN values
            data = data.dropna()
            
            return data
            
        except Exception as e:
            print(f"Error fetching data for {ticker}: {str(e)}")
            return None
    
    def calculate_returns(self, price_data):
        """
        Calculate log returns from price data.
        
        Parameters:
        -----------
        price_data : pd.DataFrame
            Price data with 'Adj Close' column
            
        Returns:
        --------
        pd.DataFrame : DataFrame with returns
        """
        try:
            # Handle different column name formats from yfinance
            if 'Adj Close' in price_data.columns:
                prices = price_data['Adj Close']
            elif 'Close' in price_data.columns:
                prices = price_data['Close']
            else:
                # Find the last column if standard names don't exist
                prices = price_data.iloc[:, -1]
            
            # Calculate log returns
            log_returns = np.log(prices / prices.shift(1))
            
            # Remove first NaN value
            log_returns = log_returns.dropna()
            
            # Simple returns for comparison
            simple_returns = prices.pct_change().dropna()
            
            # Create returns DataFrame
            returns_df = pd.DataFrame({
                'log_returns': log_returns,
                'simple_returns': simple_returns[1:],  # Align with log returns
                'price': prices[1:]  # Align with returns
            })
            
            return returns_df
            
        except Exception as e:
            print(f"Error calculating returns: {str(e)}")
            return None
    
    def calculate_returns_statistics(self, returns):
        """
        Calculate descriptive statistics for returns.
        
        Parameters:
        -----------
        returns : pd.Series
            Returns time series
            
        Returns:
        --------
        dict : Dictionary with statistics
        """
        try:
            returns_clean = pd.Series(returns).dropna()
            
            stats_dict = {
                'mean': returns_clean.mean(),
                'std': returns_clean.std(),
                'min': returns_clean.min(),
                'max': returns_clean.max(),
                'skewness': stats.skew(returns_clean),
                'kurtosis': stats.kurtosis(returns_clean),
                'jarque_bera': stats.jarque_bera(returns_clean),
                'count': len(returns_clean)
            }
            
            # Add annualized statistics (assuming daily data)
            stats_dict['annual_mean'] = stats_dict['mean'] * 252
            stats_dict['annual_std'] = stats_dict['std'] * np.sqrt(252)
            stats_dict['sharpe_ratio'] = stats_dict['annual_mean'] / stats_dict['annual_std']
            
            return stats_dict
            
        except Exception as e:
            print(f"Error calculating returns statistics: {str(e)}")
            return None
    
    def detect_outliers(self, returns, method='iqr', threshold=3):
        """
        Detect outliers in returns data.
        
        Parameters:
        -----------
        returns : pd.Series
            Returns time series
        method : str
            Method for outlier detection ('iqr' or 'zscore')
        threshold : float
            Threshold for outlier detection
            
        Returns:
        --------
        dict : Dictionary with outlier information
        """
        try:
            returns_clean = pd.Series(returns).dropna()
            
            if method == 'iqr':
                Q1 = returns_clean.quantile(0.25)
                Q3 = returns_clean.quantile(0.75)
                IQR = Q3 - Q1
                
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                outliers = returns_clean[(returns_clean < lower_bound) | (returns_clean > upper_bound)]
                
            elif method == 'zscore':
                z_scores = np.abs(stats.zscore(returns_clean))
                outliers = returns_clean[z_scores > threshold]
                
            else:
                raise ValueError("Method must be 'iqr' or 'zscore'")
            
            return {
                'outliers': outliers,
                'num_outliers': len(outliers),
                'outlier_percentage': (len(outliers) / len(returns_clean)) * 100,
                'outlier_indices': outliers.index.tolist()
            }
            
        except Exception as e:
            print(f"Error detecting outliers: {str(e)}")
            return None
    
    def calculate_rolling_statistics(self, returns, window=30):
        """
        Calculate rolling statistics for returns.
        
        Parameters:
        -----------
        returns : pd.Series
            Returns time series
        window : int
            Rolling window size
            
        Returns:
        --------
        pd.DataFrame : Rolling statistics
        """
        try:
            returns_series = pd.Series(returns).dropna()
            
            rolling_stats = pd.DataFrame({
                'rolling_mean': returns_series.rolling(window=window).mean(),
                'rolling_std': returns_series.rolling(window=window).std(),
                'rolling_var': returns_series.rolling(window=window).var(),
                'rolling_skew': returns_series.rolling(window=window).skew(),
                'rolling_kurt': returns_series.rolling(window=window).kurt()
            })
            
            return rolling_stats
            
        except Exception as e:
            print(f"Error calculating rolling statistics: {str(e)}")
            return None
    
    def test_stationarity(self, returns):
        """
        Test for stationarity using Augmented Dickey-Fuller test.
        
        Parameters:
        -----------
        returns : pd.Series
            Returns time series
            
        Returns:
        --------
        dict : ADF test results
        """
        try:
            from statsmodels.tsa.stattools import adfuller
            
            returns_clean = pd.Series(returns).dropna()
            
            # Perform ADF test
            adf_result = adfuller(returns_clean, autolag='AIC')
            
            return {
                'adf_statistic': adf_result[0],
                'p_value': adf_result[1],
                'critical_values': adf_result[4],
                'is_stationary': adf_result[1] < 0.05
            }
            
        except Exception as e:
            print(f"Error testing stationarity: {str(e)}")
            return None
    
    def calculate_volatility_measures(self, returns):
        """
        Calculate various volatility measures.
        
        Parameters:
        -----------
        returns : pd.Series
            Returns time series
            
        Returns:
        --------
        dict : Volatility measures
        """
        try:
            returns_clean = pd.Series(returns).dropna()
            
            # Basic volatility (standard deviation)
            volatility = returns_clean.std()
            
            # Annualized volatility
            annual_volatility = volatility * np.sqrt(252)
            
            # Realized volatility (square root of sum of squared returns)
            realized_vol = np.sqrt(np.sum(returns_clean ** 2))
            
            # EWMA volatility
            ewma_vol = returns_clean.ewm(span=30).std().iloc[-1]
            
            # Parkinson volatility (if we had high-low data)
            # This would require OHLC data
            
            return {
                'historical_volatility': volatility,
                'annualized_volatility': annual_volatility,
                'realized_volatility': realized_vol,
                'ewma_volatility': ewma_vol
            }
            
        except Exception as e:
            print(f"Error calculating volatility measures: {str(e)}")
            return None
