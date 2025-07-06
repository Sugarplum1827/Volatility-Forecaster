# Financial Volatility Forecasting with GARCH Models

## Overview

This project now includes both Python (Streamlit) and R (Shiny) implementations for financial volatility forecasting using GARCH models. The applications provide comprehensive analysis tools for stock volatility prediction, featuring real-time data fetching, multiple model types, and interactive visualizations.

### Python Implementation (Streamlit)
- Original implementation using Python with Streamlit framework
- Uses yfinance for data fetching and arch library for GARCH modeling
- Currently running on port 5000

### R Implementation (Shiny) - NEW
- Complete R Shiny application with advanced dashboard interface
- Uses quantmod for data fetching and rugarch for GARCH modeling
- Includes multiple model types (GARCH, EGARCH, TGARCH) and distributions
- Comprehensive diagnostic tools and export capabilities

## System Architecture

The application follows a modular architecture with clear separation of concerns:

- **Frontend**: Streamlit-based web interface for user interaction
- **Data Layer**: Yahoo Finance API integration for real-time stock data
- **Analytics Engine**: GARCH model implementation using the `arch` library
- **Visualization Layer**: Plotly-based interactive charts and graphs

## Key Components

### 1. Main Application (`app.py`)
- **Purpose**: Entry point and UI orchestration
- **Framework**: Streamlit with wide layout configuration
- **Features**: Interactive sidebar for parameter input, main dashboard for results display

### 2. Data Processing (`data_utils.py`)
- **Purpose**: Data fetching and preprocessing
- **Key Functions**:
  - Stock data retrieval from Yahoo Finance
  - Data validation and cleaning
  - Statistical calculations preparation
- **Data Requirements**: Minimum 50 observations for reliable analysis

### 3. GARCH Modeling (`garch_models.py`)
- **Purpose**: Volatility modeling and forecasting
- **Model Type**: GARCH(1,1) with configurable parameters
- **Features**:
  - Model fitting with error distribution options
  - Volatility forecasting capabilities
  - Model diagnostics and validation

### 4. Visualization (`plotting_utils.py`)
- **Purpose**: Interactive chart generation
- **Library**: Plotly for interactive web-based visualizations
- **Chart Types**: Price series, volatility plots, and statistical diagnostics

## R Shiny Application Components

### 1. Main Application (`app.R`)
- **Purpose**: Complete R Shiny dashboard for GARCH analysis
- **Framework**: Shiny with shinydashboard for professional UI
- **Features**: 
  - Multi-tab dashboard interface
  - Interactive parameter selection
  - Real-time data loading and model fitting
  - Comprehensive diagnostic tools

### 2. Package Management (`install_packages.R`)
- **Purpose**: Automated R package installation
- **Key Packages**: rugarch, quantmod, xts, plotly, DT, shinydashboard
- **Features**: Dependency checking and installation

### 3. Example Usage (`example_usage.R`)
- **Purpose**: Standalone R script demonstrating core functionality
- **Features**: Batch processing, model comparison, diagnostic testing
- **Use Case**: Educational and research purposes

### 4. Deployment Support
- **Local Development**: Complete setup instructions
- **Cloud Deployment**: shinyapps.io configuration
- **Docker Support**: Containerized deployment option

## Data Flow

1. **User Input**: Ticker symbol and date range selection via Streamlit sidebar
2. **Data Retrieval**: Yahoo Finance API fetches historical stock data
3. **Data Processing**: Raw price data converted to log returns and validated
4. **Model Fitting**: GARCH(1,1) model fitted to processed returns data
5. **Forecasting**: Volatility predictions generated based on fitted model
6. **Visualization**: Interactive plots displayed in Streamlit interface

## External Dependencies

### Core Libraries
- **streamlit**: Web application framework
- **yfinance**: Yahoo Finance API client for stock data
- **arch**: GARCH modeling library
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing
- **plotly**: Interactive visualization
- **scipy**: Statistical functions
- **matplotlib**: Additional plotting capabilities

### Data Source
- **Yahoo Finance API**: Real-time and historical stock market data
- **Access Method**: HTTP requests via yfinance wrapper
- **Rate Limits**: Subject to Yahoo Finance API limitations

## Deployment Strategy

### Development Environment
- **Framework**: Streamlit development server
- **Port**: Configurable (default 5000)
- **Command**: `streamlit run app.py --server.port 5000`

### Production Considerations
- **Hosting**: Can be deployed on Streamlit Cloud, Heroku, or similar platforms
- **Scaling**: Single-threaded application suitable for moderate traffic
- **Monitoring**: Built-in Streamlit health checks

### Installation Requirements
```bash
pip install streamlit yfinance arch pandas numpy plotly scipy matplotlib
```

## Changelog

- July 06, 2025. Initial Python Streamlit setup with GARCH modeling
- July 06, 2025. Added complete R Shiny application with advanced dashboard
- July 06, 2025. Created comprehensive deployment documentation and examples

## Recent Changes

- **R Shiny Implementation**: Created complete R Shiny application (`app.R`) with professional dashboard interface
- **Package Management**: Added automated R package installation script
- **Example Scripts**: Developed standalone R example demonstrating core functionality
- **Deployment Guide**: Created comprehensive deployment documentation for multiple platforms
- **Documentation**: Updated project documentation to reflect dual implementation

## User Preferences

Preferred communication style: Simple, everyday language.