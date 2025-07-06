# Script to run the GARCH Volatility Forecasting Shiny App
# This script ensures all packages are installed and runs the app

# Install required packages if not already installed
if (!requireNamespace("shiny", quietly = TRUE)) {
  install.packages("shiny")
}

if (!requireNamespace("rugarch", quietly = TRUE)) {
  install.packages("rugarch")
}

if (!requireNamespace("quantmod", quietly = TRUE)) {
  install.packages("quantmod")
}

if (!requireNamespace("xts", quietly = TRUE)) {
  install.packages("xts")
}

if (!requireNamespace("plotly", quietly = TRUE)) {
  install.packages("plotly")
}

if (!requireNamespace("DT", quietly = TRUE)) {
  install.packages("DT")
}

if (!requireNamespace("shinydashboard", quietly = TRUE)) {
  install.packages("shinydashboard")
}

if (!requireNamespace("moments", quietly = TRUE)) {
  install.packages("moments")
}

# Load required libraries
library(shiny)

# Run the application
cat("Starting GARCH Volatility Forecasting App...\n")
cat("The app will open in your default web browser.\n")
cat("To stop the app, press Ctrl+C in the console.\n\n")

# Run the app
shiny::runApp("app.R", port = 5000, host = "0.0.0.0")