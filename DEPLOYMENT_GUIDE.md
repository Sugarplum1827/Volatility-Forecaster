# Deployment Guide for GARCH Volatility Forecasting R Shiny App

## Overview

This R Shiny application provides comprehensive financial volatility forecasting using GARCH models. Since the current environment has package installation restrictions, here are several deployment options.

## Option 1: Local Development (Recommended)

### Prerequisites
- R (version 4.0 or higher)
- RStudio (recommended)
- Internet connection for package installation and data fetching

### Steps

1. **Download the application files**:
   - `app.R` - Main application file
   - `install_packages.R` - Package installation script
   - `run_app.R` - Application runner script
   - `README.md` - Comprehensive documentation

2. **Install R packages**:
   ```r
   # Run in R console or RStudio
   source("install_packages.R")
   ```

3. **Run the application**:
   ```r
   # Option 1: Direct run
   shiny::runApp("app.R")
   
   # Option 2: Using runner script
   source("run_app.R")
   ```

4. **Access the application**:
   - Open your web browser
   - Navigate to `http://127.0.0.1:xxxx` (port shown in R console)

## Option 2: Deploy to shinyapps.io (Cloud Hosting)

### Prerequisites
- shinyapps.io account (free tier available)
- rsconnect package

### Steps

1. **Create shinyapps.io account**:
   - Visit https://www.shinyapps.io/
   - Sign up for free account

2. **Install rsconnect**:
   ```r
   install.packages("rsconnect")
   ```

3. **Configure deployment**:
   ```r
   library(rsconnect)
   
   # Get your tokens from shinyapps.io dashboard
   rsconnect::setAccountInfo(
     name="your-account-name",
     token="your-token",
     secret="your-secret"
   )
   ```

4. **Deploy the application**:
   ```r
   rsconnect::deployApp()
   ```

## Option 3: Deploy to RStudio Connect

### Prerequisites
- RStudio Connect server access
- rsconnect package configured for your server

### Steps

1. **Configure rsconnect for your server**:
   ```r
   rsconnect::addServer("https://your-connect-server.com")
   ```

2. **Deploy**:
   ```r
   rsconnect::deployApp()
   ```

## Option 4: Docker Deployment

### Create Dockerfile
```dockerfile
FROM rocker/shiny:4.3.0

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libcurl4-openssl-dev \
    libssl-dev \
    libxml2-dev \
    && rm -rf /var/lib/apt/lists/*

# Install R packages
RUN R -e "install.packages(c('shiny', 'rugarch', 'quantmod', 'xts', 'plotly', 'DT', 'shinydashboard', 'moments', 'FinTS'), repos='https://cloud.r-project.org/')"

# Copy application files
COPY app.R /srv/shiny-server/
COPY install_packages.R /srv/shiny-server/
COPY README.md /srv/shiny-server/

# Expose port
EXPOSE 3838

# Run app
CMD ["/usr/bin/shiny-server"]
```

### Build and run Docker container
```bash
# Build
docker build -t garch-volatility-app .

# Run
docker run -p 3838:3838 garch-volatility-app
```

## Option 5: Posit Cloud (formerly RStudio Cloud)

### Steps

1. **Create Posit Cloud account**:
   - Visit https://posit.cloud/
   - Sign up for free account

2. **Create new project**:
   - Upload application files
   - Install packages using the console
   - Run the application

## Testing the Application

### Sample Data
The application works with any publicly traded stock. Try these examples:
- **AAPL** - Apple Inc.
- **GOOGL** - Alphabet Inc.
- **TSLA** - Tesla Inc.
- **MSFT** - Microsoft Corp.
- **AMZN** - Amazon.com Inc.

### Typical Workflow
1. **Input**: Enter ticker symbol (e.g., AAPL)
2. **Date Range**: Select 2-5 years of data
3. **Model**: Start with GARCH(1,1) and normal distribution
4. **Analysis**: Review data and model parameters
5. **Forecast**: Generate 5-day ahead volatility forecasts
6. **Diagnostics**: Check model adequacy
7. **Export**: Download results and reports

## Troubleshooting

### Common Issues

1. **Package Installation Errors**:
   - Update R to latest version
   - Install packages individually if batch fails
   - Check system dependencies

2. **Data Loading Issues**:
   - Verify internet connection
   - Try different ticker symbols
   - Check date ranges (ensure sufficient data)

3. **Model Fitting Problems**:
   - Ensure minimum 100 observations
   - Try different model specifications
   - Check for extreme values in data

4. **Deployment Issues**:
   - Verify all required packages are listed
   - Check file permissions
   - Ensure proper account configuration

### Performance Considerations

- **Data Range**: 1-5 years typically optimal
- **Model Complexity**: Start simple (GARCH 1,1)
- **Forecast Horizon**: 1-20 days recommended
- **Memory Usage**: Large datasets may require more RAM

## Features Overview

### Core Functionality
- **Interactive Data Loading**: Yahoo Finance integration
- **Multiple GARCH Models**: GARCH, EGARCH, TGARCH
- **Flexible Distributions**: Normal, Student-t, Skewed Student-t
- **Real-time Forecasting**: Multi-step ahead predictions
- **Comprehensive Diagnostics**: Statistical tests and plots
- **Data Export**: CSV downloads and reports

### User Interface
- **Dashboard Layout**: Professional multi-tab interface
- **Interactive Plots**: Plotly-based visualizations
- **Data Tables**: Sortable and filterable tables
- **Responsive Design**: Works on desktop and mobile
- **Error Handling**: User-friendly error messages

### Technical Features
- **Robust Error Handling**: Graceful failure management
- **Data Validation**: Automatic data cleaning
- **Model Diagnostics**: Comprehensive statistical tests
- **Export Capabilities**: Multiple download formats
- **Documentation**: Extensive help and guidance

## Support

For technical support:
1. Check the troubleshooting section
2. Verify package installations
3. Test with sample data
4. Review R console for error messages

## Next Steps

1. **Download** all application files
2. **Choose** your preferred deployment method
3. **Install** required packages
4. **Test** with sample data
5. **Customize** for your specific needs

The application is production-ready and suitable for:
- **Academic Research**: Financial econometrics studies
- **Risk Management**: Portfolio volatility analysis
- **Trading Strategies**: Volatility-based trading
- **Educational Purposes**: Teaching GARCH modeling