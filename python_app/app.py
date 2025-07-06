"""
Financial Volatility Forecasting with GARCH Models
A Streamlit application for forecasting stock volatility using GARCH(1,1) models.

To run this application:
1. Install required packages: pip install streamlit yfinance arch pandas numpy plotly scipy matplotlib
2. Run the app: streamlit run app.py --server.port 5000
3. Open your browser to the displayed URL

Author: Generated Code
Date: July 06, 2025
"""

import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Import custom modules
from garch_models import GARCHModel
from data_utils import DataProcessor
from plotting_utils import PlotGenerator

# Page configuration
st.set_page_config(
    page_title="Financial Volatility Forecasting",
    page_icon="📈",
    layout="wide"
)

def main():
    """Main application function."""
    st.title("📈 Financial Volatility Forecasting with GARCH Models")
    st.markdown("""
    This application uses GARCH(1,1) models to forecast financial volatility.
    Enter a stock ticker and select a date range to get started.
    """)
    
    # Sidebar for inputs
    st.sidebar.header("📊 Input Parameters")
    
    # Stock ticker input
    ticker = st.sidebar.text_input(
        "Stock Ticker",
        value="AAPL",
        help="Enter a valid stock ticker (e.g., AAPL, GOOGL, TSLA)"
    ).upper()
    
    # Date range selection
    st.sidebar.subheader("Date Range")
    
    # Default date range (2 years)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=730)
    
    start_date_input = st.sidebar.date_input(
        "Start Date",
        value=start_date,
        max_value=end_date - timedelta(days=30)
    )
    
    end_date_input = st.sidebar.date_input(
        "End Date",
        value=end_date,
        max_value=end_date
    )
    
    # Forecast horizon
    forecast_horizon = st.sidebar.selectbox(
        "Forecast Horizon (days)",
        [1, 5, 10, 20],
        index=1,
        help="Number of days to forecast ahead"
    )
    
    # Run analysis button
    run_analysis = st.sidebar.button("🚀 Run Volatility Analysis", type="primary")
    
    # Main content area
    if run_analysis:
        if not ticker:
            st.error("Please enter a valid stock ticker.")
            return
            
        if start_date_input >= end_date_input:
            st.error("Start date must be before end date.")
            return
            
        # Create progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Step 1: Fetch data
            status_text.text("Fetching stock data...")
            progress_bar.progress(20)
            
            data_processor = DataProcessor()
            stock_data = data_processor.fetch_stock_data(ticker, start_date_input, end_date_input)
            
            if stock_data is None or len(stock_data) < 100:
                st.error(f"Insufficient data for {ticker}. Please try a different ticker or date range.")
                return
            
            # Step 2: Calculate returns
            status_text.text("Calculating log returns...")
            progress_bar.progress(40)
            
            returns_data = data_processor.calculate_returns(stock_data)
            
            # Step 3: Fit GARCH model
            status_text.text("Fitting GARCH(1,1) model...")
            progress_bar.progress(60)
            
            garch_model = GARCHModel()
            model_fit = garch_model.fit_garch(returns_data['log_returns'])
            
            if model_fit is None:
                st.error("Failed to fit GARCH model. Please try a different ticker or date range.")
                return
            
            # Step 4: Generate forecasts
            status_text.text("Generating volatility forecasts...")
            progress_bar.progress(80)
            
            forecasts = garch_model.forecast_volatility(model_fit, forecast_horizon)
            
            # Step 5: Create visualizations
            status_text.text("Creating visualizations...")
            progress_bar.progress(100)
            
            plot_generator = PlotGenerator()
            
            # Clear progress indicators
            progress_bar.empty()
            status_text.empty()
            
            # Display results
            st.success(f"✅ Analysis completed for {ticker}")
            
            # Create tabs for different sections
            tab1, tab2, tab3, tab4, tab5 = st.tabs([
                "📊 Data Overview", 
                "📈 Returns Analysis", 
                "🔮 Volatility Forecasts", 
                "📋 Model Summary", 
                "📁 Export Data"
            ])
            
            with tab1:
                st.subheader("Stock Price Data")
                
                # Price chart
                fig_price = plot_generator.plot_price_series(stock_data, ticker)
                st.plotly_chart(fig_price, use_container_width=True)
                
                # Basic statistics
                col1, col2 = st.columns(2)
                
                # Handle different column name formats from yfinance
                if 'Adj Close' in stock_data.columns:
                    price_col = stock_data['Adj Close']
                elif 'Close' in stock_data.columns:
                    price_col = stock_data['Close']
                else:
                    price_col = stock_data.iloc[:, -1]
                
                with col1:
                    st.metric("Start Price", f"${price_col.iloc[0]:.2f}")
                    st.metric("Min Price", f"${price_col.min():.2f}")
                    
                with col2:
                    st.metric("End Price", f"${price_col.iloc[-1]:.2f}")
                    st.metric("Max Price", f"${price_col.max():.2f}")
                
                # Data summary
                st.subheader("Data Summary")
                st.write(f"**Total observations:** {len(stock_data)}")
                st.write(f"**Date range:** {start_date_input} to {end_date_input}")
                
            with tab2:
                st.subheader("Log Returns Analysis")
                
                # Returns chart
                fig_returns = plot_generator.plot_returns_series(returns_data, ticker)
                st.plotly_chart(fig_returns, use_container_width=True)
                
                # Returns statistics
                returns_stats = data_processor.calculate_returns_statistics(returns_data['log_returns'])
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Mean Return", f"{returns_stats['mean']:.4f}")
                    
                with col2:
                    st.metric("Std Deviation", f"{returns_stats['std']:.4f}")
                    
                with col3:
                    st.metric("Skewness", f"{returns_stats['skewness']:.4f}")
                    
                with col4:
                    st.metric("Kurtosis", f"{returns_stats['kurtosis']:.4f}")
                
                # Distribution plot
                fig_dist = plot_generator.plot_returns_distribution(returns_data['log_returns'])
                st.plotly_chart(fig_dist, use_container_width=True)
                
            with tab3:
                st.subheader("GARCH Volatility Forecasts")
                
                # Conditional variance (fitted volatility)
                fig_vol = plot_generator.plot_conditional_variance(model_fit, returns_data)
                st.plotly_chart(fig_vol, use_container_width=True)
                
                # Forecast visualization
                fig_forecast = plot_generator.plot_volatility_forecast(forecasts, forecast_horizon)
                st.plotly_chart(fig_forecast, use_container_width=True)
                
                # Forecast summary
                st.subheader("Forecast Summary")
                forecast_df = pd.DataFrame({
                    'Day': range(1, forecast_horizon + 1),
                    'Forecasted Volatility': forecasts['volatility_forecast']
                })
                st.dataframe(forecast_df, use_container_width=True)
                
            with tab4:
                st.subheader("GARCH Model Summary")
                
                # Model parameters
                model_summary = garch_model.get_model_summary(model_fit)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Model Parameters:**")
                    for param, value in model_summary['parameters'].items():
                        st.write(f"- {param}: {value:.6f}")
                
                with col2:
                    st.write("**Model Statistics:**")
                    st.write(f"- AIC: {model_summary['aic']:.4f}")
                    st.write(f"- BIC: {model_summary['bic']:.4f}")
                    st.write(f"- Log-Likelihood: {model_summary['loglikelihood']:.4f}")
                
                # Diagnostic plots
                st.subheader("Diagnostic Plots")
                
                # Residuals analysis
                fig_diagnostics = plot_generator.plot_model_diagnostics(model_fit)
                st.plotly_chart(fig_diagnostics, use_container_width=True)
                
                # QQ plot
                fig_qq = plot_generator.plot_qq_plot(model_fit)
                st.plotly_chart(fig_qq, use_container_width=True)
                
            with tab5:
                st.subheader("Export Data")
                
                # Prepare export data
                export_data = {
                    'Date': stock_data.index,
                    'Price': stock_data['Adj Close'],
                    'Log_Returns': returns_data['log_returns'],
                    'Conditional_Variance': model_fit.conditional_volatility ** 2
                }
                
                export_df = pd.DataFrame(export_data)
                
                # Add forecasts
                forecast_export = pd.DataFrame({
                    'Forecast_Day': range(1, forecast_horizon + 1),
                    'Forecasted_Volatility': forecasts['volatility_forecast'],
                    'Forecast_Variance': forecasts['variance_forecast']
                })
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Historical Data Preview:**")
                    st.dataframe(export_df.tail(10), use_container_width=True)
                    
                    # Download button for historical data
                    csv_historical = export_df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Historical Data (CSV)",
                        data=csv_historical,
                        file_name=f"{ticker}_historical_data_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv"
                    )
                
                with col2:
                    st.write("**Forecast Data Preview:**")
                    st.dataframe(forecast_export, use_container_width=True)
                    
                    # Download button for forecast data
                    csv_forecast = forecast_export.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Forecast Data (CSV)",
                        data=csv_forecast,
                        file_name=f"{ticker}_volatility_forecast_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv"
                    )
                
        except Exception as e:
            progress_bar.empty()
            status_text.empty()
            st.error(f"An error occurred during analysis: {str(e)}")
            st.error("Please try again with different parameters or contact support if the issue persists.")
    
    else:
        # Show instructions when no analysis is running
        st.info("👈 Enter a stock ticker and select a date range in the sidebar, then click 'Run Volatility Analysis' to get started.")
        
        # Show sample tickers
        st.subheader("Popular Stock Tickers")
        sample_tickers = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN", "NVDA", "META", "NFLX"]
        
        cols = st.columns(4)
        for i, ticker_sample in enumerate(sample_tickers):
            with cols[i % 4]:
                st.code(ticker_sample)
        
        # Show methodology
        st.subheader("Methodology")
        st.markdown("""
        This application uses the following approach:
        
        1. **Data Fetching**: Historical stock prices are fetched using Yahoo Finance
        2. **Returns Calculation**: Log returns are calculated from adjusted closing prices
        3. **GARCH Modeling**: A GARCH(1,1) model is fitted to capture volatility clustering
        4. **Forecasting**: Multi-step ahead volatility forecasts are generated
        5. **Diagnostics**: Model fit is evaluated using various diagnostic tests
        
        The GARCH(1,1) model is defined as:
        - σ²ₜ = ω + α·ε²ₜ₋₁ + β·σ²ₜ₋₁
        
        Where σ²ₜ is the conditional variance, ω is the constant term, α is the ARCH parameter, and β is the GARCH parameter.
        """)

if __name__ == "__main__":
    main()
