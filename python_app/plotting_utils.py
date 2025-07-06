"""
Plotting Utilities
Handles all visualization and plotting functions.
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

class PlotGenerator:
    """Class for generating all plots and visualizations."""
    
    def __init__(self):
        """Initialize plot generator."""
        pass
    
    def plot_price_series(self, stock_data, ticker):
        """
        Plot stock price time series.
        
        Parameters:
        -----------
        stock_data : pd.DataFrame
            Stock price data
        ticker : str
            Stock ticker symbol
            
        Returns:
        --------
        plotly.graph_objects.Figure : Price plot
        """
        try:
            fig = go.Figure()
            
            # Handle different column name formats from yfinance
            if 'Adj Close' in stock_data.columns:
                price_col = stock_data['Adj Close']
            elif 'Close' in stock_data.columns:
                price_col = stock_data['Close']
            else:
                # Find the last column if standard names don't exist
                price_col = stock_data.iloc[:, -1]
            
            # Add price line
            fig.add_trace(go.Scatter(
                x=stock_data.index,
                y=price_col,
                mode='lines',
                name=f'{ticker} Price',
                line=dict(color='#1f77b4', width=2)
            ))
            
            # Update layout
            fig.update_layout(
                title=f'{ticker} Stock Price Over Time',
                xaxis_title='Date',
                yaxis_title='Price ($)',
                hovermode='x unified',
                showlegend=True,
                height=500
            )
            
            return fig
            
        except Exception as e:
            print(f"Error creating price plot: {str(e)}")
            return go.Figure()
    
    def plot_returns_series(self, returns_data, ticker):
        """
        Plot returns time series.
        
        Parameters:
        -----------
        returns_data : pd.DataFrame
            Returns data
        ticker : str
            Stock ticker symbol
            
        Returns:
        --------
        plotly.graph_objects.Figure : Returns plot
        """
        try:
            fig = go.Figure()
            
            # Add returns line
            fig.add_trace(go.Scatter(
                x=returns_data.index,
                y=returns_data['log_returns'],
                mode='lines',
                name=f'{ticker} Log Returns',
                line=dict(color='#ff7f0e', width=1)
            ))
            
            # Add zero line
            fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
            
            # Update layout
            fig.update_layout(
                title=f'{ticker} Log Returns Over Time',
                xaxis_title='Date',
                yaxis_title='Log Returns',
                hovermode='x unified',
                showlegend=True,
                height=500
            )
            
            return fig
            
        except Exception as e:
            print(f"Error creating returns plot: {str(e)}")
            return go.Figure()
    
    def plot_returns_distribution(self, returns):
        """
        Plot returns distribution with normal overlay.
        
        Parameters:
        -----------
        returns : pd.Series
            Returns time series
            
        Returns:
        --------
        plotly.graph_objects.Figure : Distribution plot
        """
        try:
            returns_clean = pd.Series(returns).dropna()
            
            # Create subplots
            fig = make_subplots(
                rows=1, cols=2,
                subplot_titles=('Returns Distribution', 'Q-Q Plot'),
                specs=[[{"secondary_y": False}, {"secondary_y": False}]]
            )
            
            # Histogram
            fig.add_trace(
                go.Histogram(
                    x=returns_clean,
                    nbinsx=50,
                    name='Returns',
                    opacity=0.7,
                    showlegend=False
                ),
                row=1, col=1
            )
            
            # Normal distribution overlay
            x_range = np.linspace(returns_clean.min(), returns_clean.max(), 100)
            normal_dist = stats.norm.pdf(x_range, returns_clean.mean(), returns_clean.std())
            
            fig.add_trace(
                go.Scatter(
                    x=x_range,
                    y=normal_dist * len(returns_clean) * (returns_clean.max() - returns_clean.min()) / 50,
                    mode='lines',
                    name='Normal Distribution',
                    line=dict(color='red', width=2),
                    showlegend=False
                ),
                row=1, col=1
            )
            
            # Q-Q plot
            (osm, osr), (slope, intercept, r) = stats.probplot(returns_clean, dist="norm")
            
            fig.add_trace(
                go.Scatter(
                    x=osm,
                    y=osr,
                    mode='markers',
                    name='Sample Quantiles',
                    marker=dict(color='blue', size=4),
                    showlegend=False
                ),
                row=1, col=2
            )
            
            # Q-Q line
            fig.add_trace(
                go.Scatter(
                    x=osm,
                    y=slope * osm + intercept,
                    mode='lines',
                    name='Theoretical Line',
                    line=dict(color='red', width=2),
                    showlegend=False
                ),
                row=1, col=2
            )
            
            # Update layout
            fig.update_layout(
                title='Returns Distribution Analysis',
                height=500
            )
            
            fig.update_xaxes(title_text="Returns", row=1, col=1)
            fig.update_yaxes(title_text="Frequency", row=1, col=1)
            fig.update_xaxes(title_text="Theoretical Quantiles", row=1, col=2)
            fig.update_yaxes(title_text="Sample Quantiles", row=1, col=2)
            
            return fig
            
        except Exception as e:
            print(f"Error creating distribution plot: {str(e)}")
            return go.Figure()
    
    def plot_conditional_variance(self, model_fit, returns_data):
        """
        Plot conditional variance from GARCH model.
        
        Parameters:
        -----------
        model_fit : arch model fit object
            Fitted GARCH model
        returns_data : pd.DataFrame
            Returns data
            
        Returns:
        --------
        plotly.graph_objects.Figure : Conditional variance plot
        """
        try:
            # Create subplots
            fig = make_subplots(
                rows=2, cols=1,
                subplot_titles=('Log Returns', 'Conditional Volatility'),
                shared_xaxes=True,
                vertical_spacing=0.1
            )
            
            # Returns plot
            fig.add_trace(
                go.Scatter(
                    x=returns_data.index,
                    y=returns_data['log_returns'],
                    mode='lines',
                    name='Log Returns',
                    line=dict(color='#ff7f0e', width=1)
                ),
                row=1, col=1
            )
            
            # Conditional volatility
            cond_vol = model_fit.conditional_volatility / 100  # Convert back from percentage
            
            fig.add_trace(
                go.Scatter(
                    x=returns_data.index,
                    y=cond_vol,
                    mode='lines',
                    name='Conditional Volatility',
                    line=dict(color='#2ca02c', width=2)
                ),
                row=2, col=1
            )
            
            # Update layout
            fig.update_layout(
                title='GARCH Model: Returns and Conditional Volatility',
                height=600,
                hovermode='x unified'
            )
            
            fig.update_xaxes(title_text="Date", row=2, col=1)
            fig.update_yaxes(title_text="Log Returns", row=1, col=1)
            fig.update_yaxes(title_text="Volatility", row=2, col=1)
            
            return fig
            
        except Exception as e:
            print(f"Error creating conditional variance plot: {str(e)}")
            return go.Figure()
    
    def plot_volatility_forecast(self, forecasts, horizon):
        """
        Plot volatility forecasts.
        
        Parameters:
        -----------
        forecasts : dict
            Forecast results
        horizon : int
            Forecast horizon
            
        Returns:
        --------
        plotly.graph_objects.Figure : Forecast plot
        """
        try:
            forecast_days = list(range(1, horizon + 1))
            
            fig = go.Figure()
            
            # Add forecast line
            fig.add_trace(go.Scatter(
                x=forecast_days,
                y=forecasts['volatility_forecast'],
                mode='lines+markers',
                name='Volatility Forecast',
                line=dict(color='#d62728', width=3),
                marker=dict(size=8)
            ))
            
            # Update layout
            fig.update_layout(
                title=f'{horizon}-Day Ahead Volatility Forecast',
                xaxis_title='Days Ahead',
                yaxis_title='Forecasted Volatility',
                hovermode='x',
                height=400
            )
            
            # Add grid
            fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
            fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
            
            return fig
            
        except Exception as e:
            print(f"Error creating forecast plot: {str(e)}")
            return go.Figure()
    
    def plot_model_diagnostics(self, model_fit):
        """
        Plot model diagnostic plots.
        
        Parameters:
        -----------
        model_fit : arch model fit object
            Fitted GARCH model
            
        Returns:
        --------
        plotly.graph_objects.Figure : Diagnostic plots
        """
        try:
            # Get residuals
            residuals = model_fit.resid
            std_residuals = model_fit.std_resid
            
            # Create subplots
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=(
                    'Residuals Over Time',
                    'Squared Residuals',
                    'Standardized Residuals',
                    'ACF of Squared Residuals'
                )
            )
            
            # Residuals over time
            fig.add_trace(
                go.Scatter(
                    x=list(range(len(residuals))),
                    y=residuals,
                    mode='lines',
                    name='Residuals',
                    line=dict(color='blue', width=1),
                    showlegend=False
                ),
                row=1, col=1
            )
            
            # Squared residuals
            fig.add_trace(
                go.Scatter(
                    x=list(range(len(residuals))),
                    y=residuals**2,
                    mode='lines',
                    name='Squared Residuals',
                    line=dict(color='orange', width=1),
                    showlegend=False
                ),
                row=1, col=2
            )
            
            # Standardized residuals
            fig.add_trace(
                go.Scatter(
                    x=list(range(len(std_residuals))),
                    y=std_residuals,
                    mode='lines',
                    name='Standardized Residuals',
                    line=dict(color='green', width=1),
                    showlegend=False
                ),
                row=2, col=1
            )
            
            # ACF of squared residuals
            try:
                from statsmodels.tsa.stattools import acf
                
                acf_values = acf(residuals**2, nlags=20, fft=True)
                
                fig.add_trace(
                    go.Bar(
                        x=list(range(len(acf_values))),
                        y=acf_values,
                        name='ACF',
                        marker_color='red',
                        showlegend=False
                    ),
                    row=2, col=2
                )
                
            except ImportError:
                # Fallback if statsmodels not available
                fig.add_trace(
                    go.Scatter(
                        x=[0],
                        y=[0],
                        mode='text',
                        text=['ACF calculation requires statsmodels'],
                        showlegend=False
                    ),
                    row=2, col=2
                )
            
            # Update layout
            fig.update_layout(
                title='GARCH Model Diagnostic Plots',
                height=600
            )
            
            return fig
            
        except Exception as e:
            print(f"Error creating diagnostic plots: {str(e)}")
            return go.Figure()
    
    def plot_qq_plot(self, model_fit):
        """
        Create Q-Q plot for model residuals.
        
        Parameters:
        -----------
        model_fit : arch model fit object
            Fitted GARCH model
            
        Returns:
        --------
        plotly.graph_objects.Figure : Q-Q plot
        """
        try:
            # Get standardized residuals
            std_residuals = model_fit.std_resid
            
            # Create Q-Q plot
            (osm, osr), (slope, intercept, r) = stats.probplot(std_residuals, dist="norm")
            
            fig = go.Figure()
            
            # Add scatter points
            fig.add_trace(
                go.Scatter(
                    x=osm,
                    y=osr,
                    mode='markers',
                    name='Sample Quantiles',
                    marker=dict(color='blue', size=4)
                )
            )
            
            # Add reference line
            fig.add_trace(
                go.Scatter(
                    x=osm,
                    y=slope * osm + intercept,
                    mode='lines',
                    name='Theoretical Line',
                    line=dict(color='red', width=2)
                )
            )
            
            # Update layout
            fig.update_layout(
                title='Q-Q Plot: Standardized Residuals vs Normal Distribution',
                xaxis_title='Theoretical Quantiles',
                yaxis_title='Sample Quantiles',
                height=500
            )
            
            return fig
            
        except Exception as e:
            print(f"Error creating Q-Q plot: {str(e)}")
            return go.Figure()
    
    def plot_volatility_clustering(self, returns):
        """
        Plot to visualize volatility clustering.
        
        Parameters:
        -----------
        returns : pd.Series
            Returns time series
            
        Returns:
        --------
        plotly.graph_objects.Figure : Volatility clustering plot
        """
        try:
            returns_clean = pd.Series(returns).dropna()
            
            # Calculate rolling volatility
            rolling_vol = returns_clean.rolling(window=30).std()
            
            fig = make_subplots(
                rows=2, cols=1,
                subplot_titles=('Returns', 'Rolling Volatility (30-day)'),
                shared_xaxes=True
            )
            
            # Returns
            fig.add_trace(
                go.Scatter(
                    x=returns_clean.index,
                    y=returns_clean,
                    mode='lines',
                    name='Returns',
                    line=dict(color='blue', width=1)
                ),
                row=1, col=1
            )
            
            # Rolling volatility
            fig.add_trace(
                go.Scatter(
                    x=rolling_vol.index,
                    y=rolling_vol,
                    mode='lines',
                    name='Rolling Volatility',
                    line=dict(color='red', width=2)
                ),
                row=2, col=1
            )
            
            fig.update_layout(
                title='Volatility Clustering Analysis',
                height=600
            )
            
            return fig
            
        except Exception as e:
            print(f"Error creating volatility clustering plot: {str(e)}")
            return go.Figure()
