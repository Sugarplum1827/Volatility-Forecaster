# Package Installation Script for GARCH Volatility Forecasting App
# Run this script once to install all required packages

# List of required packages
required_packages <- c(
  "shiny",           # Web application framework
  "rugarch",         # GARCH modeling
  "quantmod",        # Financial data retrieval
  "xts",             # Time series objects
  "plotly",          # Interactive plots
  "DT",              # Data tables
  "shinydashboard",  # Dashboard layout
  "FinTS",           # Additional financial time series functions
  "moments"          # Statistical moments (skewness, kurtosis)
)

# Function to install packages if not already installed
install_if_missing <- function(package) {
  if (!require(package, character.only = TRUE)) {
    cat("Installing", package, "...\n")
    install.packages(package, dependencies = TRUE)
    library(package, character.only = TRUE)
  } else {
    cat(package, "is already installed.\n")
  }
}

# Install all required packages
cat("Installing required packages for GARCH Volatility Forecasting App...\n")
cat("This may take a few minutes...\n\n")

for (package in required_packages) {
  install_if_missing(package)
}

cat("\nAll packages installed successfully!\n")
cat("You can now run the app with: shiny::runApp('app.R')\n")