# Example Usage of GARCH Volatility Forecasting Functions
# This script demonstrates how to use the core functionality outside of the Shiny interface
# Useful for understanding the underlying methodology and for batch processing

# Load required libraries
library(rugarch)
library(quantmod)
library(xts)
library(plotly)
library(moments)

# Example 1: Basic GARCH Analysis
# ================================

# Function to fetch and prepare data
fetch_stock_data <- function(ticker, start_date, end_date) {
  cat("Fetching data for", ticker, "from", start_date, "to", end_date, "\n")
  
  # Download stock data
  stock_data <- getSymbols(ticker, src = "yahoo", 
                          from = start_date, to = end_date, 
                          auto.assign = FALSE)
  
  # Extract adjusted closing prices
  prices <- Ad(stock_data)
  
  # Calculate log returns
  returns <- diff(log(prices), na.pad = FALSE)
  returns <- returns[!is.na(returns)]
  
  # Remove extreme outliers (optional)
  returns <- returns[abs(returns) < 0.2]
  
  return(list(
    stock_data = stock_data,
    prices = prices,
    returns = returns
  ))
}

# Function to fit GARCH model
fit_garch_model <- function(returns, model_type = "sGARCH", distribution = "norm") {
  cat("Fitting GARCH model...\n")
  
  # Specify GARCH model
  garch_spec <- ugarchspec(
    variance.model = list(model = model_type, garchOrder = c(1, 1)),
    mean.model = list(armaOrder = c(0, 0), include.mean = TRUE),
    distribution.model = distribution
  )
  
  # Fit model
  garch_fit <- ugarchfit(spec = garch_spec, data = returns)
  
  return(garch_fit)
}

# Function to generate forecasts
generate_forecast <- function(garch_fit, horizon = 5) {
  cat("Generating", horizon, "step ahead forecasts...\n")
  
  # Generate forecast
  forecast_result <- ugarchforecast(garch_fit, n.ahead = horizon)
  
  return(forecast_result)
}

# Function to calculate summary statistics
calculate_summary_stats <- function(returns) {
  returns_vec <- as.numeric(returns)
  
  stats <- list(
    mean = mean(returns_vec),
    std_dev = sd(returns_vec),
    skewness = skewness(returns_vec),
    kurtosis = kurtosis(returns_vec),
    min = min(returns_vec),
    max = max(returns_vec),
    observations = length(returns_vec)
  )
  
  return(stats)
}

# Function to perform diagnostic tests
perform_diagnostics <- function(garch_fit) {
  # Extract standardized residuals
  std_residuals <- residuals(garch_fit, standardize = TRUE)
  
  # Ljung-Box test
  lb_test <- Box.test(std_residuals, lag = 10, type = "Ljung-Box")
  
  # ARCH test
  arch_test <- try({
    # Simple ARCH test implementation
    squared_residuals <- std_residuals^2
    n <- length(squared_residuals)
    lags <- 5
    
    # Create lagged matrix
    X <- matrix(1, nrow = n - lags, ncol = lags + 1)
    for (i in 1:lags) {
      X[, i + 1] <- squared_residuals[(lags - i + 1):(n - i)]
    }
    
    y <- squared_residuals[(lags + 1):n]
    
    # OLS regression
    beta <- solve(t(X) %*% X) %*% t(X) %*% y
    fitted <- X %*% beta
    ssr <- sum((y - fitted)^2)
    tss <- sum((y - mean(y))^2)
    r_squared <- 1 - ssr/tss
    
    # LM statistic
    lm_stat <- (n - lags) * r_squared
    p_value <- 1 - pchisq(lm_stat, df = lags)
    
    list(statistic = lm_stat, p.value = p_value)
  }, silent = TRUE)
  
  if (inherits(arch_test, "try-error")) {
    arch_test <- list(statistic = NA, p.value = NA)
  }
  
  return(list(
    ljung_box = lb_test,
    arch_test = arch_test
  ))
}

# Example usage
# =============

# Example 1: Analyze Apple stock
cat("=== Example 1: Apple Stock Analysis ===\n")

# Set parameters
ticker <- "AAPL"
start_date <- "2022-01-01"
end_date <- "2024-12-31"

# Fetch data
data_result <- fetch_stock_data(ticker, start_date, end_date)
returns <- data_result$returns

# Calculate summary statistics
stats <- calculate_summary_stats(returns)
cat("\nSummary Statistics for", ticker, ":\n")
cat("Mean:", round(stats$mean, 6), "\n")
cat("Std Dev:", round(stats$std_dev, 6), "\n")
cat("Skewness:", round(stats$skewness, 4), "\n")
cat("Kurtosis:", round(stats$kurtosis, 4), "\n")
cat("Observations:", stats$observations, "\n")

# Fit GARCH model
garch_fit <- fit_garch_model(returns, model_type = "sGARCH", distribution = "norm")

# Display model parameters
cat("\nGARCH Model Parameters:\n")
print(coef(garch_fit))

# Display information criteria
cat("\nModel Fit Statistics:\n")
cat("AIC:", round(infocriteria(garch_fit)[1], 4), "\n")
cat("BIC:", round(infocriteria(garch_fit)[2], 4), "\n")
cat("Log-Likelihood:", round(likelihood(garch_fit), 4), "\n")

# Generate forecasts
forecast_result <- generate_forecast(garch_fit, horizon = 5)

# Display forecast results
cat("\nVolatility Forecasts:\n")
forecast_vol <- as.numeric(sigma(forecast_result))
for (i in 1:length(forecast_vol)) {
  cat("Day", i, ":", round(forecast_vol[i], 6), "\n")
}

# Perform diagnostics
diagnostics <- perform_diagnostics(garch_fit)
cat("\nDiagnostic Tests:\n")
cat("Ljung-Box Test - Statistic:", round(diagnostics$ljung_box$statistic, 4), 
    "p-value:", round(diagnostics$ljung_box$p.value, 4), "\n")
cat("ARCH-LM Test - Statistic:", round(diagnostics$arch_test$statistic, 4), 
    "p-value:", round(diagnostics$arch_test$p.value, 4), "\n")

# Example 2: Compare multiple stocks
cat("\n=== Example 2: Multiple Stock Comparison ===\n")

tickers <- c("AAPL", "GOOGL", "MSFT")
comparison_results <- list()

for (ticker in tickers) {
  cat("\nAnalyzing", ticker, "...\n")
  
  tryCatch({
    # Fetch data
    data_result <- fetch_stock_data(ticker, start_date, end_date)
    returns <- data_result$returns
    
    # Fit GARCH model
    garch_fit <- fit_garch_model(returns, model_type = "sGARCH", distribution = "norm")
    
    # Generate forecast
    forecast_result <- generate_forecast(garch_fit, horizon = 5)
    
    # Store results
    comparison_results[[ticker]] <- list(
      returns = returns,
      garch_fit = garch_fit,
      forecast = forecast_result,
      stats = calculate_summary_stats(returns)
    )
    
    cat("✓ Analysis completed for", ticker, "\n")
    
  }, error = function(e) {
    cat("✗ Error analyzing", ticker, ":", e$message, "\n")
  })
}

# Display comparison summary
cat("\n=== Comparison Summary ===\n")
cat(sprintf("%-10s %-10s %-10s %-10s %-10s\n", "Ticker", "Mean", "Std Dev", "Skewness", "Kurtosis"))
cat(paste(rep("-", 55), collapse = ""), "\n")

for (ticker in names(comparison_results)) {
  stats <- comparison_results[[ticker]]$stats
  cat(sprintf("%-10s %-10.6f %-10.6f %-10.4f %-10.4f\n", 
              ticker, stats$mean, stats$std_dev, stats$skewness, stats$kurtosis))
}

# Example 3: Model comparison
cat("\n=== Example 3: Model Comparison ===\n")

if (length(comparison_results) > 0) {
  ticker <- names(comparison_results)[1]
  returns <- comparison_results[[ticker]]$returns
  
  models <- c("sGARCH", "eGARCH", "fGARCH")
  distributions <- c("norm", "std", "sstd")
  
  cat("\nComparing different model specifications for", ticker, ":\n")
  cat(sprintf("%-15s %-10s %-10s %-10s\n", "Model", "AIC", "BIC", "LogLik"))
  cat(paste(rep("-", 50), collapse = ""), "\n")
  
  for (model in models) {
    for (dist in distributions) {
      tryCatch({
        garch_fit <- fit_garch_model(returns, model_type = model, distribution = dist)
        aic <- infocriteria(garch_fit)[1]
        bic <- infocriteria(garch_fit)[2]
        loglik <- likelihood(garch_fit)
        
        model_name <- paste0(model, "-", dist)
        cat(sprintf("%-15s %-10.4f %-10.4f %-10.4f\n", model_name, aic, bic, loglik))
        
      }, error = function(e) {
        cat(sprintf("%-15s %-10s %-10s %-10s\n", paste0(model, "-", dist), "Failed", "Failed", "Failed"))
      })
    }
  }
}

cat("\n=== Analysis Complete ===\n")
cat("This script demonstrates the core functionality of the GARCH volatility forecasting system.\n")
cat("For interactive analysis, use the Shiny application (app.R).\n")