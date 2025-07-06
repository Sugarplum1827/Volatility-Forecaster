# Python GARCH Volatility Forecasting App

A Streamlit web application for financial volatility forecasting using GARCH(1,1) models.

## Overview

This Python implementation provides an interactive web interface for analyzing stock volatility using GARCH modeling. It fetches real-time stock data from Yahoo Finance and applies GARCH(1,1) models to forecast future volatility patterns.

## Features

- **Interactive Data Loading**: Enter stock ticker symbols and select date ranges
- **Real-time Data**: Fetches historical stock prices using Yahoo Finance API
- **GARCH(1,1) Modeling**: Fits GARCH models to capture volatility clustering
- **Volatility Forecasting**: Generate 1-20 day ahead volatility predictions
- **Interactive Visualizations**: Plotly-based charts for prices, returns, and forecasts
- **Model Diagnostics**: Statistical tests and diagnostic plots
- **Data Export**: Download historical data and forecasts in CSV format

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Required Packages
Install the required packages using pip:

```bash
pip install streamlit yfinance arch pandas numpy plotly scipy matplotlib statsmodels
```

Or using the provided requirements:

```bash
pip install -r requirements.txt
```

## Usage

### Running the Application

1. **Run the Streamlit app**:
   ```bash
   streamlit run app.py --server.port 5000
   ```

2. **Access the application**:
   - Open your web browser
   - Navigate to `http://localhost:5000`

### Using the Application

1. **Enter Stock Ticker**: Input a valid stock symbol (e.g., AAPL, GOOGL, TSLA)
2. **Select Date Range**: Choose start and end dates for analysis
3. **Set Forecast Horizon**: Select how many days ahead to forecast (1-20 days)
4. **Run Analysis**: Click "Run Volatility Analysis" to process the data
5. **Review Results**: Explore the different tabs for data, analysis, forecasts, and diagnostics

## Application Structure

### Core Files

- **`app.py`**: Main Streamlit application with user interface
- **`data_utils.py`**: Data fetching and processing utilities
- **`garch_models.py`**: GARCH model fitting and forecasting functions
- **`plotting_utils.py`**: Visualization and plotting utilities
- **`.streamlit/config.toml`**: Streamlit configuration file

### Key Components

1. **Data Processing**: 
   - Fetches stock data from Yahoo Finance
   - Calculates log returns and basic statistics
   - Handles data validation and cleaning

2. **GARCH Modeling**:
   - Fits GARCH(1,1) models using the `arch` library
   - Generates volatility forecasts
   - Provides model diagnostics and validation

3. **Visualization**:
   - Interactive price and returns charts
   - Volatility forecasting plots
   - Distribution analysis and Q-Q plots
   - Model diagnostic visualizations

4. **Export Features**:
   - Download historical data with calculated returns
   - Export volatility forecasts
   - Generate summary reports

## Sample Usage

### Popular Stock Tickers
Try these common stock symbols:
- **AAPL** - Apple Inc.
- **GOOGL** - Alphabet Inc.
- **MSFT** - Microsoft Corp.
- **TSLA** - Tesla Inc.
- **AMZN** - Amazon.com Inc.
- **NVDA** - NVIDIA Corp.
- **META** - Meta Platforms Inc.

### Recommended Settings
- **Date Range**: 2-5 years of historical data
- **Forecast Horizon**: 5-10 days for reliable predictions
- **Data Frequency**: Daily data (automatically provided by Yahoo Finance)

## Technical Details

### GARCH(1,1) Model
The application implements the standard GARCH(1,1) model:

σ²ₜ = ω + α·ε²ₜ₋₁ + β·σ²ₜ₋₁

Where:
- σ²ₜ is the conditional variance at time t
- ω is the constant term
- α is the ARCH parameter (impact of past shocks)
- β is the GARCH parameter (persistence of volatility)

### Data Processing
- **Log Returns**: Calculated as ln(Pₜ/Pₜ₋₁)
- **Data Validation**: Automatic handling of missing values and outliers
- **Scaling**: Returns are scaled appropriately for GARCH estimation

### Forecasting
- **Multi-step Forecasting**: Uses simulation methods for horizon > 1
- **Confidence Intervals**: Provides uncertainty estimates for forecasts
- **Model Validation**: Includes diagnostic tests for model adequacy

## Troubleshooting

### Common Issues

1. **Installation Problems**:
   - Ensure Python 3.8+ is installed
   - Update pip: `pip install --upgrade pip`
   - Install packages individually if batch installation fails

2. **Data Loading Errors**:
   - Check internet connection for Yahoo Finance access
   - Verify ticker symbol is valid and actively traded
   - Try different date ranges if data is insufficient

3. **Model Fitting Issues**:
   - Ensure sufficient data (minimum 100 observations recommended)
   - Try different date ranges for better data quality
   - Check for extreme market events that might affect convergence

4. **Performance Issues**:
   - Use reasonable date ranges (avoid extremely long periods)
   - Close other browser tabs if memory issues occur
   - Restart the application if it becomes unresponsive

### Error Messages

- **"Insufficient data"**: Use longer time periods or different ticker
- **"Failed to fit GARCH model"**: Try different date range or ticker
- **"No data found"**: Check ticker symbol spelling and market availability

## Development

### Project Structure
```
Volatility-Forcaster/
├── app.py                 # Main Streamlit application
├── data_utils.py         # Data processing utilities
├── garch_models.py       # GARCH modeling functions
├── plotting_utils.py     # Visualization utilities
├── .streamlit/           # Streamlit configuration
│   └── config.toml
└── README.md            # This file
```

### Adding Features
The modular structure allows easy extension:
- Add new model types in `garch_models.py`
- Extend visualizations in `plotting_utils.py`
- Add data sources in `data_utils.py`
- Modify UI in `app.py`

## Dependencies

- **streamlit**: Web application framework
- **yfinance**: Yahoo Finance data access
- **arch**: GARCH modeling library
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing
- **plotly**: Interactive visualizations
- **scipy**: Statistical functions
- **matplotlib**: Additional plotting capabilities
- **statsmodels**: Statistical models and tests

## License

This application is provided for educational and research purposes. Please ensure compliance with data provider terms of service when using financial data.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Verify all dependencies are correctly installed
3. Ensure data connectivity and ticker validity
4. Review console output for specific error messages

---

**Note**: This application requires an active internet connection to fetch financial data from Yahoo Finance. Data availability depends on the provider's terms and conditions.