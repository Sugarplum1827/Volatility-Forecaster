# R Shiny GARCH Volatility Forecasting App

A comprehensive R Shiny application for financial volatility forecasting using advanced GARCH models with professional dashboard interface.

## Overview

This R Shiny implementation provides a sophisticated web application for analyzing stock volatility using multiple GARCH model variants. It features a professional dashboard interface with advanced diagnostic tools, multiple model types, and comprehensive export capabilities.

## Features

### Core Functionality
- **Professional Dashboard**: Multi-tab interface with clean, intuitive design
- **Multiple GARCH Models**: GARCH(1,1), EGARCH(1,1), TGARCH(1,1)
- **Error Distributions**: Normal, Student-t, Skewed Student-t
- **Interactive Data Loading**: Real-time stock data from Yahoo Finance
- **Advanced Forecasting**: Flexible horizon forecasting (1-30 days)
- **Comprehensive Diagnostics**: Statistical tests, Q-Q plots, ACF analysis
- **Data Export**: CSV downloads and detailed reports

### User Interface
- **Data Input Tab**: Configure stock ticker, date range, and model parameters
- **Analysis Tab**: Summary statistics, model parameters, and time series plots
- **Forecasting Tab**: Generate and visualize volatility forecasts
- **Diagnostics Tab**: Model validation and residual analysis
- **Export Tab**: Download data, forecasts, and comprehensive reports

## Installation

### Prerequisites
- R (version 4.0 or higher)
- RStudio (recommended for development)
- Internet connection for package installation and data fetching

### Quick Setup

1. **Install all required packages**:
   ```r
   # Run this in R console
   source("install_packages.R")
   ```

2. **Run the application**:
   ```r
   # Option 1: Direct run
   shiny::runApp("app.R")
   
   # Option 2: Using runner script
   source("run_app.R")
   ```

### Manual Package Installation

If automatic installation fails, install packages individually:

```r
install.packages(c(
  "shiny",           # Web application framework
  "rugarch",         # GARCH modeling
  "quantmod",        # Financial data retrieval
  "xts",             # Time series objects
  "plotly",          # Interactive plots
  "DT",              # Data tables
  "shinydashboard",  # Dashboard layout
  "FinTS",           # Financial time series functions
  "moments"          # Statistical moments
))
```

## Usage

### Local Development

1. **Navigate to the r_app directory**:
   ```bash
   cd r_app
   ```

2. **Install dependencies** (run once):
   ```r
   source("install_packages.R")
   ```

3. **Run the application**:
   ```r
   shiny::runApp("app.R", port = 5000, host = "0.0.0.0")
   ```

4. **Access the application**:
   - Open web browser to `http://localhost:5000`

### Cloud Deployment

#### Deploy to shinyapps.io

1. **Install rsconnect**:
   ```r
   install.packages("rsconnect")
   ```

2. **Configure account**:
   ```r
   library(rsconnect)
   rsconnect::setAccountInfo(
     name="your-account-name",
     token="your-token", 
     secret="your-secret"
   )
   ```

3. **Deploy**:
   ```r
   rsconnect::deployApp()
   ```

See `DEPLOYMENT_GUIDE.md` for detailed deployment options including Docker and RStudio Connect.

## Application Workflow

### Step 1: Data Input
- Enter stock ticker symbol (e.g., AAPL, GOOGL, TSLA)
- Select start and end dates for analysis
- Choose GARCH model type and error distribution
- Click "Load Data & Run Analysis"

### Step 2: Analysis Review
- Examine summary statistics of returns data
- Review fitted GARCH model parameters
- View log returns and conditional volatility plots

### Step 3: Generate Forecasts
- Set forecast horizon (1-30 days)
- Click "Generate Forecast"
- View volatility forecast plots and summary tables

### Step 4: Model Diagnostics
- Review model fit statistics (AIC, BIC, Log-Likelihood)
- Examine residual tests for model adequacy
- Check Q-Q plots and ACF analysis

### Step 5: Export Results
- Download historical data with computed statistics
- Export forecast results to CSV
- Generate comprehensive analysis reports

## File Structure

```
r_app/
├── app.R                    # Main Shiny application
├── install_packages.R       # Package installation script
├── example_usage.R         # Standalone R example code
├── run_app.R               # Application runner script
├── DEPLOYMENT_GUIDE.md     # Comprehensive deployment documentation
└── README.md               # This file
```

## Model Details

### Available GARCH Models

#### 1. GARCH(1,1) - Standard GARCH
- **Equation**: σ²ₜ = ω + α·ε²ₜ₋₁ + β·σ²ₜ₋₁
- **Best for**: Basic volatility clustering analysis
- **Parameters**: ω (constant), α (ARCH), β (GARCH)

#### 2. EGARCH(1,1) - Exponential GARCH
- **Features**: Asymmetric volatility responses
- **Best for**: Markets with leverage effects
- **Advantage**: Captures different impacts of positive vs negative shocks

#### 3. TGARCH(1,1) - Threshold GARCH
- **Features**: Threshold effects for volatility
- **Best for**: Markets with regime changes
- **Advantage**: Allows different volatility dynamics above/below threshold

### Error Distributions

- **Normal**: Standard Gaussian distribution
- **Student-t**: Heavy-tailed distribution for financial returns
- **Skewed Student-t**: Asymmetric returns with heavy tails

## Sample Data

### Recommended Stock Tickers
- **AAPL** - Apple Inc.
- **GOOGL** - Alphabet Inc.
- **MSFT** - Microsoft Corp.
- **TSLA** - Tesla Inc.
- **AMZN** - Amazon.com Inc.
- **NVDA** - NVIDIA Corp.
- **META** - Meta Platforms Inc.
- **JPM** - JPMorgan Chase & Co.

### Optimal Settings
- **Date Range**: 2-5 years for stable parameter estimation
- **Model Type**: Start with GARCH(1,1) and normal distribution
- **Forecast Horizon**: 5-10 days for reliable predictions

## Advanced Features

### Diagnostic Tests
- **Ljung-Box Test**: Tests for autocorrelation in residuals
- **ARCH-LM Test**: Tests for remaining heteroscedasticity
- **Information Criteria**: AIC, BIC for model comparison
- **Residual Analysis**: Standardized residuals evaluation

### Interactive Visualizations
- **Plotly Integration**: Zoom, pan, hover functionality
- **Real-time Updates**: Dynamic plot generation
- **Professional Styling**: Clean, publication-ready charts
- **Export Options**: Save plots as images

### Data Export Capabilities
- **Historical Data**: Prices, returns, conditional volatility
- **Forecast Results**: Multi-step ahead predictions with confidence intervals
- **Model Reports**: Complete analysis summaries
- **Multiple Formats**: CSV for data, text for reports

## Troubleshooting

### Common Installation Issues

1. **Package Installation Failures**:
   ```r
   # Update R and packages
   update.packages(ask = FALSE)
   
   # Install packages individually
   install.packages("rugarch", dependencies = TRUE)
   ```

2. **System Dependencies** (Linux/Mac):
   ```bash
   # For Ubuntu/Debian
   sudo apt-get install libcurl4-openssl-dev libssl-dev libxml2-dev
   
   # For macOS with Homebrew
   brew install openssl libxml2
   ```

### Application Issues

1. **Data Loading Problems**:
   - Verify internet connection
   - Check ticker symbol validity
   - Try different date ranges
   - Ensure sufficient data (minimum 100 observations)

2. **Model Fitting Failures**:
   - Reduce date range if convergence issues
   - Try different model specifications
   - Check for extreme market events
   - Use normal distribution first, then try others

3. **Performance Issues**:
   - Use reasonable forecast horizons (≤ 20 days)
   - Avoid extremely large datasets
   - Close other browser tabs if memory constrained

### Error Resolution

- **"Error in ugarchfit"**: Try different model specification or date range
- **"Insufficient data"**: Extend date range or try different ticker
- **"Package not found"**: Run `install_packages.R` script

## Development

### Extending the Application

1. **Add New Models**:
   - Modify model specification in server logic
   - Update UI dropdown options
   - Add model documentation

2. **Custom Visualizations**:
   - Extend plotting functions
   - Add new diagnostic plots
   - Integrate additional chart types

3. **Enhanced Exports**:
   - Add PDF report generation
   - Include additional data formats
   - Create automated email reports

### Code Organization
- **UI Definition**: Clean separation of interface components
- **Server Logic**: Modular reactive functions
- **Error Handling**: Comprehensive try-catch blocks
- **Documentation**: Inline comments and help text

## Dependencies

### Core Packages
- **shiny**: Web application framework
- **shinydashboard**: Professional dashboard layout
- **rugarch**: Advanced GARCH modeling
- **quantmod**: Financial data access
- **xts**: Time series data structures

### Visualization & UI
- **plotly**: Interactive plots
- **DT**: Advanced data tables
- **htmlwidgets**: Widget integration

### Statistical Analysis
- **moments**: Statistical moments calculation
- **FinTS**: Financial time series tests

## Performance Optimization

- **Reactive Programming**: Efficient data flow
- **Caching**: Minimize redundant calculations
- **Error Handling**: Graceful failure management
- **Memory Management**: Efficient data structures

## License

Educational and research use. Ensure compliance with data provider terms when using financial data.

---

**For detailed deployment instructions, see `DEPLOYMENT_GUIDE.md`**