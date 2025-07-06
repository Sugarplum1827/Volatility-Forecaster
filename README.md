# Financial Volatility Forecasting with GARCH Models - R Shiny App

A comprehensive R Shiny application for analyzing and forecasting financial volatility using GARCH models. This app provides an interactive interface for loading stock data, fitting GARCH models, generating forecasts, and performing diagnostic tests.

## Features

### 📊 **Data Input & Management**
- **Stock Data Loading**: Fetch historical stock prices using Yahoo Finance API
- **Flexible Date Range**: Select custom start and end dates for analysis
- **Multiple Tickers**: Support for any publicly traded stock (AAPL, GOOGL, TSLA, etc.)
- **Data Validation**: Automatic data cleaning and validation

### 🔧 **GARCH Modeling**
- **Multiple Model Types**: 
  - GARCH(1,1) - Standard GARCH model
  - EGARCH(1,1) - Exponential GARCH for asymmetric effects
  - TGARCH(1,1) - Threshold GARCH model
- **Distribution Options**:
  - Normal Distribution
  - Student-t Distribution
  - Skewed Student-t Distribution
- **Automatic Model Fitting**: Robust parameter estimation with error handling

### 📈 **Interactive Visualizations**
- **Price Time Series**: Interactive stock price charts with zoom and pan
- **Log Returns**: Time series plot of calculated log returns
- **Conditional Volatility**: GARCH model fitted volatility over time
- **Volatility Forecasts**: Multi-step ahead volatility predictions
- **Diagnostic Plots**: Q-Q plots, ACF plots, and residual analysis

### 🔮 **Forecasting Capabilities**
- **Flexible Horizon**: Forecast 1-30 days ahead
- **Volatility Predictions**: Generate future volatility estimates
- **Forecast Visualization**: Interactive plots of forecast results
- **Statistical Measures**: Variance and volatility forecasts with confidence intervals

### 🔍 **Model Diagnostics**
- **Residual Analysis**: Standardized residuals and diagnostic tests
- **Statistical Tests**: 
  - Ljung-Box test for autocorrelation
  - ARCH-LM test for remaining heteroscedasticity
- **Q-Q Plots**: Normality assessment of residuals
- **ACF Analysis**: Autocorrelation function of squared residuals
- **Information Criteria**: AIC, BIC, and log-likelihood values

### 💾 **Data Export**
- **Historical Data**: Download processed stock data and returns
- **Forecast Results**: Export volatility forecasts to CSV
- **Model Summary**: Complete model report with parameters and statistics
- **Multiple Formats**: CSV files for data, text reports for summaries

## Installation

### Prerequisites
- R (version 4.0 or higher)
- RStudio (recommended for development)

### Required Packages
Run the installation script to install all required packages:

```r
# Run this in R console
source("install_packages.R")
```

Or manually install packages:

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

### Running Locally

1. **Install Dependencies**:
   ```r
   source("install_packages.R")
   ```

2. **Run the Application**:
   ```r
   shiny::runApp("app.R")
   ```

3. **Access the App**:
   - Open your web browser
   - Navigate to the URL shown in the R console (typically `http://127.0.0.1:xxxx`)

### Deploying to shinyapps.io

1. **Install rsconnect**:
   ```r
   install.packages("rsconnect")
   ```

2. **Configure Account**:
   ```r
   rsconnect::setAccountInfo(name="your-account", 
                            token="your-token", 
                            secret="your-secret")
   ```

3. **Deploy App**:
   ```r
   rsconnect::deployApp()
   ```

## How to Use the Application

### Step 1: Data Input
1. Navigate to the **"Data Input"** tab
2. Enter a stock ticker symbol (e.g., AAPL, GOOGL, TSLA)
3. Select start and end dates for your analysis
4. Choose GARCH model type and error distribution
5. Click **"Load Data & Run Analysis"**

### Step 2: Analysis
1. Go to the **"Analysis"** tab
2. Review summary statistics of your data
3. Examine the GARCH model parameters
4. View log returns and conditional volatility plots

### Step 3: Forecasting
1. Switch to the **"Forecasting"** tab
2. Set your desired forecast horizon (1-30 days)
3. Click **"Generate Forecast"**
4. View the volatility forecast plot and summary table

### Step 4: Diagnostics
1. Visit the **"Diagnostics"** tab
2. Review model fit statistics (AIC, BIC, Log-Likelihood)
3. Examine residual tests for model adequacy
4. Check Q-Q plots and ACF plots for diagnostic insights

### Step 5: Export Results
1. Go to the **"Export"** tab
2. Preview your data and results
3. Download historical data, forecasts, or full reports
4. Choose from CSV data files or text summary reports

## Model Details

### GARCH(1,1) Model
The application implements the GARCH(1,1) model:

σ²ₜ = ω + α·ε²ₜ₋₁ + β·σ²ₜ₋₁

Where:
- σ²ₜ is the conditional variance at time t
- ω is the constant term
- α is the ARCH parameter (impact of past shocks)
- β is the GARCH parameter (persistence of volatility)

### Model Variants
- **GARCH**: Standard symmetric GARCH model
- **EGARCH**: Exponential GARCH for asymmetric volatility responses
- **TGARCH**: Threshold GARCH for different responses to positive/negative shocks

### Error Distributions
- **Normal**: Standard Gaussian distribution
- **Student-t**: Heavy-tailed distribution for financial returns
- **Skewed Student-t**: Allows for asymmetric return distributions

## Troubleshooting

### Common Issues

1. **Package Installation Errors**:
   - Update R to the latest version
   - Install packages one by one if batch installation fails
   - Check for system dependencies (especially for rugarch)

2. **Data Loading Issues**:
   - Ensure internet connection for Yahoo Finance API
   - Try different ticker symbols or date ranges
   - Check that the ticker symbol is valid and actively traded

3. **Model Fitting Failures**:
   - Insufficient data: Use longer time periods (minimum 100 observations)
   - Extreme values: The app automatically filters extreme returns
   - Try different model specifications or distributions

4. **Forecast Generation Problems**:
   - Ensure GARCH model is fitted successfully first
   - Reduce forecast horizon if convergence issues occur
   - Check model parameters for stability conditions

### Performance Tips

- Use reasonable date ranges (1-5 years typically work well)
- Start with GARCH(1,1) and normal distribution for initial analysis
- Allow sufficient observations for stable parameter estimation
- Monitor model convergence and diagnostic test results

## Technical Architecture

### Frontend (UI)
- **Framework**: Shiny with shinydashboard
- **Layout**: Multi-tab dashboard with responsive design
- **Visualizations**: Plotly for interactive charts
- **Data Tables**: DT package for interactive tables

### Backend (Server)
- **Data Source**: Yahoo Finance via quantmod
- **Modeling**: rugarch package for GARCH estimation
- **Time Series**: xts package for time series handling
- **Statistics**: Built-in R functions and additional packages

### Data Flow
1. User input → Data fetching (quantmod)
2. Data processing → Return calculation
3. Model specification → GARCH fitting (rugarch)
4. Forecast generation → Volatility prediction
5. Visualization → Interactive plots (plotly)
6. Export → Data download functionality

## License

This application is provided for educational and research purposes. Please ensure compliance with data provider terms of service when using financial data.

## Contributing

This is an open-source project. Contributions are welcome for:
- Additional GARCH model variants
- Enhanced diagnostic tests
- New visualization features
- Performance improvements
- Bug fixes and documentation

## Support

For issues or questions:
1. Check the troubleshooting section
2. Verify all packages are correctly installed
3. Ensure data connectivity and ticker validity
4. Review R console for error messages

---

**Note**: This application requires an active internet connection to fetch financial data from Yahoo Finance. Market data availability depends on the data provider's terms and conditions.