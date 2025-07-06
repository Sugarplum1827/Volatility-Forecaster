# Financial Volatility Forecasting with GARCH Models
# An R Shiny Application for analyzing and forecasting stock volatility
# 
# Instructions to run this application:
# 1. Install required packages (run this once):
#    install.packages(c("shiny", "rugarch", "quantmod", "xts", "plotly", "DT", "shinydashboard"))
# 2. Run the application:
#    shiny::runApp()
# 3. Or deploy to shinyapps.io:
#    rsconnect::deployApp()
#
# Author: R Shiny GARCH Application
# Date: July 06, 2025

# Load required libraries
library(shiny)
library(rugarch)
library(quantmod)
library(xts)
library(plotly)
library(DT)
library(shinydashboard)

# Define UI
ui <- dashboardPage(
  dashboardHeader(title = "Financial Volatility Forecasting with GARCH"),
  
  dashboardSidebar(
    sidebarMenu(
      menuItem("Data Input", tabName = "input", icon = icon("upload")),
      menuItem("Analysis", tabName = "analysis", icon = icon("chart-line")),
      menuItem("Forecasting", tabName = "forecast", icon = icon("crystal-ball")),
      menuItem("Diagnostics", tabName = "diagnostics", icon = icon("stethoscope")),
      menuItem("Export", tabName = "export", icon = icon("download"))
    )
  ),
  
  dashboardBody(
    tags$head(
      tags$style(HTML("
        .content-wrapper, .right-side {
          background-color: #f8f9fa;
        }
        .box {
          border-radius: 5px;
          box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
      "))
    ),
    
    tabItems(
      # Data Input Tab
      tabItem(
        tabName = "input",
        fluidRow(
          box(
            title = "Stock Data Configuration", 
            status = "primary", 
            solidHeader = TRUE,
            width = 12,
            fluidRow(
              column(
                width = 4,
                textInput("ticker", "Stock Ticker Symbol:", value = "AAPL",
                         placeholder = "e.g., AAPL, GOOGL, TSLA")
              ),
              column(
                width = 4,
                dateInput("start_date", "Start Date:", 
                         value = Sys.Date() - 365*2,
                         max = Sys.Date() - 30)
              ),
              column(
                width = 4,
                dateInput("end_date", "End Date:", 
                         value = Sys.Date(),
                         max = Sys.Date())
              )
            ),
            br(),
            fluidRow(
              column(
                width = 6,
                selectInput("garch_model", "GARCH Model Type:",
                           choices = c("GARCH(1,1)" = "sGARCH",
                                     "EGARCH(1,1)" = "eGARCH",
                                     "TGARCH(1,1)" = "fGARCH"),
                           selected = "sGARCH")
              ),
              column(
                width = 6,
                selectInput("distribution", "Error Distribution:",
                           choices = c("Normal" = "norm",
                                     "Student-t" = "std",
                                     "Skewed Student-t" = "sstd"),
                           selected = "norm")
              )
            ),
            br(),
            actionButton("load_data", "Load Data & Run Analysis", 
                        class = "btn-primary btn-lg", 
                        icon = icon("play"))
          )
        ),
        
        # Data preview
        fluidRow(
          box(
            title = "Data Preview", 
            status = "info", 
            solidHeader = TRUE,
            width = 12,
            plotlyOutput("price_plot", height = "400px"),
            br(),
            DT::dataTableOutput("data_table")
          )
        )
      ),
      
      # Analysis Tab
      tabItem(
        tabName = "analysis",
        fluidRow(
          # Summary statistics
          box(
            title = "Summary Statistics", 
            status = "primary", 
            solidHeader = TRUE,
            width = 6,
            tableOutput("summary_stats")
          ),
          
          # Model parameters
          box(
            title = "GARCH Model Parameters", 
            status = "success", 
            solidHeader = TRUE,
            width = 6,
            tableOutput("model_params")
          )
        ),
        
        fluidRow(
          # Returns plot
          box(
            title = "Log Returns Time Series", 
            status = "info", 
            solidHeader = TRUE,
            width = 12,
            plotlyOutput("returns_plot", height = "400px")
          )
        ),
        
        fluidRow(
          # Conditional volatility
          box(
            title = "Conditional Volatility", 
            status = "warning", 
            solidHeader = TRUE,
            width = 12,
            plotlyOutput("volatility_plot", height = "400px")
          )
        )
      ),
      
      # Forecasting Tab
      tabItem(
        tabName = "forecast",
        fluidRow(
          box(
            title = "Forecast Settings", 
            status = "primary", 
            solidHeader = TRUE,
            width = 12,
            fluidRow(
              column(
                width = 6,
                numericInput("forecast_horizon", "Forecast Horizon (days):", 
                           value = 5, min = 1, max = 30, step = 1)
              ),
              column(
                width = 6,
                actionButton("run_forecast", "Generate Forecast", 
                           class = "btn-success", 
                           icon = icon("chart-line"))
              )
            )
          )
        ),
        
        fluidRow(
          # Volatility forecast plot
          box(
            title = "Volatility Forecast", 
            status = "success", 
            solidHeader = TRUE,
            width = 12,
            plotlyOutput("forecast_plot", height = "400px")
          )
        ),
        
        fluidRow(
          # Forecast summary table
          box(
            title = "Forecast Summary", 
            status = "info", 
            solidHeader = TRUE,
            width = 12,
            DT::dataTableOutput("forecast_table")
          )
        )
      ),
      
      # Diagnostics Tab
      tabItem(
        tabName = "diagnostics",
        fluidRow(
          # Model fit statistics
          box(
            title = "Model Fit Statistics", 
            status = "primary", 
            solidHeader = TRUE,
            width = 6,
            tableOutput("model_fit_stats")
          ),
          
          # Residual tests
          box(
            title = "Residual Tests", 
            status = "warning", 
            solidHeader = TRUE,
            width = 6,
            tableOutput("residual_tests")
          )
        ),
        
        fluidRow(
          # Q-Q plot
          box(
            title = "Q-Q Plot of Standardized Residuals", 
            status = "info", 
            solidHeader = TRUE,
            width = 6,
            plotlyOutput("qq_plot", height = "400px")
          ),
          
          # ACF plot
          box(
            title = "ACF of Squared Residuals", 
            status = "success", 
            solidHeader = TRUE,
            width = 6,
            plotlyOutput("acf_plot", height = "400px")
          )
        ),
        
        fluidRow(
          # Residuals plot
          box(
            title = "Standardized Residuals", 
            status = "warning", 
            solidHeader = TRUE,
            width = 12,
            plotlyOutput("residuals_plot", height = "400px")
          )
        )
      ),
      
      # Export Tab
      tabItem(
        tabName = "export",
        fluidRow(
          box(
            title = "Export Options", 
            status = "primary", 
            solidHeader = TRUE,
            width = 12,
            h4("Download Data and Results"),
            br(),
            fluidRow(
              column(
                width = 4,
                downloadButton("download_data", "Download Historical Data", 
                              class = "btn-info btn-block",
                              icon = icon("table"))
              ),
              column(
                width = 4,
                downloadButton("download_forecast", "Download Forecast", 
                              class = "btn-success btn-block",
                              icon = icon("chart-line"))
              ),
              column(
                width = 4,
                downloadButton("download_report", "Download Full Report", 
                              class = "btn-warning btn-block",
                              icon = icon("file-pdf"))
              )
            )
          )
        ),
        
        fluidRow(
          box(
            title = "Export Preview", 
            status = "info", 
            solidHeader = TRUE,
            width = 12,
            tabsetPanel(
              tabPanel("Historical Data", DT::dataTableOutput("export_data_preview")),
              tabPanel("Forecast Data", DT::dataTableOutput("export_forecast_preview")),
              tabPanel("Model Summary", verbatimTextOutput("export_model_summary"))
            )
          )
        )
      )
    )
  )
)

# Define Server
server <- function(input, output, session) {
  
  # Reactive values to store data and models
  values <- reactiveValues(
    stock_data = NULL,
    returns = NULL,
    garch_fit = NULL,
    forecast_result = NULL,
    error_message = NULL
  )
  
  # Load data and fit GARCH model
  observeEvent(input$load_data, {
    
    # Validate inputs
    if (is.null(input$ticker) || input$ticker == "") {
      showNotification("Please enter a valid ticker symbol.", type = "error")
      return()
    }
    
    if (input$start_date >= input$end_date) {
      showNotification("Start date must be before end date.", type = "error")
      return()
    }
    
    # Show loading notification
    showNotification("Loading data and fitting GARCH model...", type = "message", duration = NULL, id = "loading")
    
    tryCatch({
      # Fetch stock data using quantmod
      ticker_symbol <- toupper(input$ticker)
      
      # Download data
      stock_data <- getSymbols(ticker_symbol, 
                              src = "yahoo",
                              from = input$start_date,
                              to = input$end_date,
                              auto.assign = FALSE)
      
      if (is.null(stock_data) || nrow(stock_data) < 100) {
        stop("Insufficient data. Please try a different ticker or date range.")
      }
      
      # Calculate log returns
      prices <- Ad(stock_data)  # Adjusted close prices
      returns <- diff(log(prices), na.pad = FALSE)
      returns <- returns[!is.na(returns)]
      
      # Remove extreme outliers (optional)
      returns <- returns[abs(returns) < 0.2]  # Remove returns > 20%
      
      if (length(returns) < 100) {
        stop("Insufficient return data after cleaning.")
      }
      
      # Specify GARCH model
      garch_spec <- ugarchspec(
        variance.model = list(model = input$garch_model, garchOrder = c(1, 1)),
        mean.model = list(armaOrder = c(0, 0), include.mean = TRUE),
        distribution.model = input$distribution
      )
      
      # Fit GARCH model
      garch_fit <- ugarchfit(spec = garch_spec, data = returns)
      
      # Store results
      values$stock_data <- stock_data
      values$returns <- returns
      values$garch_fit <- garch_fit
      values$error_message <- NULL
      
      # Remove loading notification and show success
      removeNotification("loading")
      showNotification("Data loaded and GARCH model fitted successfully!", type = "success")
      
    }, error = function(e) {
      values$error_message <- paste("Error:", e$message)
      removeNotification("loading")
      showNotification(paste("Error:", e$message), type = "error")
    })
  })
  
  # Generate forecast
  observeEvent(input$run_forecast, {
    
    if (is.null(values$garch_fit)) {
      showNotification("Please load data and fit GARCH model first.", type = "warning")
      return()
    }
    
    tryCatch({
      # Generate forecast
      forecast_result <- ugarchforecast(values$garch_fit, n.ahead = input$forecast_horizon)
      values$forecast_result <- forecast_result
      
      showNotification("Forecast generated successfully!", type = "success")
      
    }, error = function(e) {
      showNotification(paste("Forecast error:", e$message), type = "error")
    })
  })
  
  # Price plot
  output$price_plot <- renderPlotly({
    if (is.null(values$stock_data)) {
      return(plotly_empty())
    }
    
    prices <- Ad(values$stock_data)
    dates <- index(values$stock_data)
    
    p <- plot_ly(x = dates, y = as.numeric(prices), type = 'scatter', mode = 'lines',
                line = list(color = 'blue', width = 2),
                name = paste(input$ticker, "Price")) %>%
      layout(title = paste(input$ticker, "Stock Price"),
             xaxis = list(title = "Date"),
             yaxis = list(title = "Price ($)"),
             hovermode = 'x')
    
    return(p)
  })
  
  # Data table
  output$data_table <- DT::renderDataTable({
    if (is.null(values$stock_data)) {
      return(data.frame())
    }
    
    # Convert to data frame for display
    df <- data.frame(
      Date = index(values$stock_data),
      Open = as.numeric(Op(values$stock_data)),
      High = as.numeric(Hi(values$stock_data)),
      Low = as.numeric(Lo(values$stock_data)),
      Close = as.numeric(Cl(values$stock_data)),
      Volume = as.numeric(Vo(values$stock_data)),
      Adjusted = as.numeric(Ad(values$stock_data))
    )
    
    DT::datatable(df, options = list(pageLength = 10, scrollX = TRUE))
  })
  
  # Summary statistics
  output$summary_stats <- renderTable({
    if (is.null(values$returns)) {
      return(data.frame())
    }
    
    returns_vec <- as.numeric(values$returns)
    
    stats <- data.frame(
      Statistic = c("Mean", "Std Dev", "Skewness", "Kurtosis", "Min", "Max", "Observations"),
      Value = c(
        round(mean(returns_vec), 6),
        round(sd(returns_vec), 6),
        round(skewness(returns_vec), 4),
        round(kurtosis(returns_vec), 4),
        round(min(returns_vec), 6),
        round(max(returns_vec), 6),
        length(returns_vec)
      )
    )
    
    return(stats)
  })
  
  # Model parameters
  output$model_params <- renderTable({
    if (is.null(values$garch_fit)) {
      return(data.frame())
    }
    
    coef_values <- coef(values$garch_fit)
    
    params <- data.frame(
      Parameter = names(coef_values),
      Estimate = round(coef_values, 6),
      stringsAsFactors = FALSE
    )
    
    return(params)
  })
  
  # Returns plot
  output$returns_plot <- renderPlotly({
    if (is.null(values$returns)) {
      return(plotly_empty())
    }
    
    dates <- index(values$returns)
    returns_vec <- as.numeric(values$returns)
    
    p <- plot_ly(x = dates, y = returns_vec, type = 'scatter', mode = 'lines',
                line = list(color = 'orange', width = 1),
                name = "Log Returns") %>%
      layout(title = paste(input$ticker, "Log Returns"),
             xaxis = list(title = "Date"),
             yaxis = list(title = "Log Returns"),
             hovermode = 'x')
    
    return(p)
  })
  
  # Volatility plot
  output$volatility_plot <- renderPlotly({
    if (is.null(values$garch_fit)) {
      return(plotly_empty())
    }
    
    cond_vol <- sigma(values$garch_fit)
    dates <- index(values$returns)
    
    p <- plot_ly(x = dates, y = as.numeric(cond_vol), type = 'scatter', mode = 'lines',
                line = list(color = 'green', width = 2),
                name = "Conditional Volatility") %>%
      layout(title = "GARCH Conditional Volatility",
             xaxis = list(title = "Date"),
             yaxis = list(title = "Volatility"),
             hovermode = 'x')
    
    return(p)
  })
  
  # Forecast plot
  output$forecast_plot <- renderPlotly({
    if (is.null(values$forecast_result)) {
      return(plotly_empty())
    }
    
    forecast_vol <- as.numeric(sigma(values$forecast_result))
    forecast_days <- 1:length(forecast_vol)
    
    p <- plot_ly(x = forecast_days, y = forecast_vol, type = 'scatter', mode = 'lines+markers',
                line = list(color = 'red', width = 3),
                marker = list(size = 8),
                name = "Volatility Forecast") %>%
      layout(title = paste(input$forecast_horizon, "Day Ahead Volatility Forecast"),
             xaxis = list(title = "Days Ahead"),
             yaxis = list(title = "Forecasted Volatility"),
             hovermode = 'x')
    
    return(p)
  })
  
  # Forecast table
  output$forecast_table <- DT::renderDataTable({
    if (is.null(values$forecast_result)) {
      return(data.frame())
    }
    
    forecast_vol <- as.numeric(sigma(values$forecast_result))
    forecast_var <- forecast_vol^2
    
    df <- data.frame(
      Day = 1:length(forecast_vol),
      Forecasted_Volatility = round(forecast_vol, 6),
      Forecasted_Variance = round(forecast_var, 8)
    )
    
    DT::datatable(df, options = list(pageLength = 10))
  })
  
  # Model fit statistics
  output$model_fit_stats <- renderTable({
    if (is.null(values$garch_fit)) {
      return(data.frame())
    }
    
    # Extract information criteria
    aic_val <- infocriteria(values$garch_fit)[1]
    bic_val <- infocriteria(values$garch_fit)[2]
    likelihood <- likelihood(values$garch_fit)
    
    stats <- data.frame(
      Statistic = c("AIC", "BIC", "Log-Likelihood", "Observations"),
      Value = c(
        round(aic_val, 4),
        round(bic_val, 4),
        round(likelihood, 4),
        length(values$returns)
      )
    )
    
    return(stats)
  })
  
  # Residual tests
  output$residual_tests <- renderTable({
    if (is.null(values$garch_fit)) {
      return(data.frame())
    }
    
    # Extract standardized residuals
    std_residuals <- residuals(values$garch_fit, standardize = TRUE)
    
    # Ljung-Box test on residuals
    lb_test <- Box.test(std_residuals, lag = 10, type = "Ljung-Box")
    
    # ARCH test on residuals
    arch_test <- ArchTest(std_residuals, lags = 5)
    
    tests <- data.frame(
      Test = c("Ljung-Box (residuals)", "ARCH-LM (residuals)"),
      Statistic = c(round(lb_test$statistic, 4), round(arch_test$statistic, 4)),
      P_Value = c(round(lb_test$p.value, 4), round(arch_test$p.value, 4)),
      Result = c(
        ifelse(lb_test$p.value > 0.05, "No autocorrelation", "Autocorrelation present"),
        ifelse(arch_test$p.value > 0.05, "No ARCH effects", "ARCH effects present")
      )
    )
    
    return(tests)
  })
  
  # Q-Q plot
  output$qq_plot <- renderPlotly({
    if (is.null(values$garch_fit)) {
      return(plotly_empty())
    }
    
    std_residuals <- as.numeric(residuals(values$garch_fit, standardize = TRUE))
    
    # Q-Q plot data
    qqnorm_data <- qqnorm(std_residuals, plot.it = FALSE)
    
    p <- plot_ly(x = qqnorm_data$x, y = qqnorm_data$y, type = 'scatter', mode = 'markers',
                marker = list(color = 'blue', size = 4),
                name = "Sample Quantiles") %>%
      add_trace(x = qqnorm_data$x, y = qqnorm_data$x, type = 'scatter', mode = 'lines',
               line = list(color = 'red', width = 2),
               name = "Normal Line") %>%
      layout(title = "Q-Q Plot: Standardized Residuals",
             xaxis = list(title = "Theoretical Quantiles"),
             yaxis = list(title = "Sample Quantiles"))
    
    return(p)
  })
  
  # ACF plot
  output$acf_plot <- renderPlotly({
    if (is.null(values$garch_fit)) {
      return(plotly_empty())
    }
    
    std_residuals <- as.numeric(residuals(values$garch_fit, standardize = TRUE))
    squared_residuals <- std_residuals^2
    
    # Calculate ACF
    acf_result <- acf(squared_residuals, plot = FALSE, lag.max = 20)
    
    p <- plot_ly(x = acf_result$lag[-1], y = acf_result$acf[-1], type = 'bar',
                marker = list(color = 'darkblue'),
                name = "ACF") %>%
      layout(title = "ACF of Squared Standardized Residuals",
             xaxis = list(title = "Lag"),
             yaxis = list(title = "ACF"))
    
    return(p)
  })
  
  # Residuals plot
  output$residuals_plot <- renderPlotly({
    if (is.null(values$garch_fit)) {
      return(plotly_empty())
    }
    
    std_residuals <- as.numeric(residuals(values$garch_fit, standardize = TRUE))
    dates <- index(values$returns)
    
    p <- plot_ly(x = dates, y = std_residuals, type = 'scatter', mode = 'lines',
                line = list(color = 'purple', width = 1),
                name = "Standardized Residuals") %>%
      layout(title = "Standardized Residuals Over Time",
             xaxis = list(title = "Date"),
             yaxis = list(title = "Standardized Residuals"),
             hovermode = 'x')
    
    return(p)
  })
  
  # Export data preview
  output$export_data_preview <- DT::renderDataTable({
    if (is.null(values$stock_data) || is.null(values$returns)) {
      return(data.frame())
    }
    
    # Prepare export data
    prices <- Ad(values$stock_data)
    returns_aligned <- values$returns
    
    # Align dates
    common_dates <- intersect(index(prices), index(returns_aligned))
    
    df <- data.frame(
      Date = common_dates,
      Price = as.numeric(prices[common_dates]),
      Log_Returns = as.numeric(returns_aligned[common_dates]),
      Conditional_Volatility = if (!is.null(values$garch_fit)) as.numeric(sigma(values$garch_fit)) else NA
    )
    
    DT::datatable(df, options = list(pageLength = 10, scrollX = TRUE))
  })
  
  # Export forecast preview
  output$export_forecast_preview <- DT::renderDataTable({
    if (is.null(values$forecast_result)) {
      return(data.frame())
    }
    
    forecast_vol <- as.numeric(sigma(values$forecast_result))
    forecast_var <- forecast_vol^2
    
    df <- data.frame(
      Forecast_Day = 1:length(forecast_vol),
      Forecasted_Volatility = round(forecast_vol, 6),
      Forecasted_Variance = round(forecast_var, 8)
    )
    
    DT::datatable(df, options = list(pageLength = 10))
  })
  
  # Export model summary
  output$export_model_summary <- renderText({
    if (is.null(values$garch_fit)) {
      return("No model fitted yet.")
    }
    
    # Create model summary text
    summary_text <- paste(
      "GARCH Model Summary",
      "==================",
      "",
      paste("Model Type:", input$garch_model),
      paste("Distribution:", input$distribution),
      paste("Ticker:", input$ticker),
      paste("Sample Period:", input$start_date, "to", input$end_date),
      "",
      "Model Parameters:",
      paste(capture.output(print(coef(values$garch_fit))), collapse = "\n"),
      "",
      "Information Criteria:",
      paste("AIC:", round(infocriteria(values$garch_fit)[1], 4)),
      paste("BIC:", round(infocriteria(values$garch_fit)[2], 4)),
      paste("Log-Likelihood:", round(likelihood(values$garch_fit), 4)),
      "",
      sep = "\n"
    )
    
    return(summary_text)
  })
  
  # Download handlers
  output$download_data <- downloadHandler(
    filename = function() {
      paste(input$ticker, "_historical_data_", Sys.Date(), ".csv", sep = "")
    },
    content = function(file) {
      if (!is.null(values$stock_data) && !is.null(values$returns)) {
        prices <- Ad(values$stock_data)
        returns_aligned <- values$returns
        common_dates <- intersect(index(prices), index(returns_aligned))
        
        df <- data.frame(
          Date = common_dates,
          Price = as.numeric(prices[common_dates]),
          Log_Returns = as.numeric(returns_aligned[common_dates]),
          Conditional_Volatility = if (!is.null(values$garch_fit)) as.numeric(sigma(values$garch_fit)) else NA
        )
        
        write.csv(df, file, row.names = FALSE)
      }
    }
  )
  
  output$download_forecast <- downloadHandler(
    filename = function() {
      paste(input$ticker, "_volatility_forecast_", Sys.Date(), ".csv", sep = "")
    },
    content = function(file) {
      if (!is.null(values$forecast_result)) {
        forecast_vol <- as.numeric(sigma(values$forecast_result))
        forecast_var <- forecast_vol^2
        
        df <- data.frame(
          Forecast_Day = 1:length(forecast_vol),
          Forecasted_Volatility = round(forecast_vol, 6),
          Forecasted_Variance = round(forecast_var, 8)
        )
        
        write.csv(df, file, row.names = FALSE)
      }
    }
  )
  
  output$download_report <- downloadHandler(
    filename = function() {
      paste(input$ticker, "_garch_report_", Sys.Date(), ".txt", sep = "")
    },
    content = function(file) {
      if (!is.null(values$garch_fit)) {
        summary_text <- paste(
          "GARCH Model Analysis Report",
          "===========================",
          "",
          paste("Generated on:", Sys.time()),
          paste("Ticker:", input$ticker),
          paste("Model Type:", input$garch_model),
          paste("Distribution:", input$distribution),
          paste("Sample Period:", input$start_date, "to", input$end_date),
          "",
          "Model Parameters:",
          paste(capture.output(print(coef(values$garch_fit))), collapse = "\n"),
          "",
          "Information Criteria:",
          paste("AIC:", round(infocriteria(values$garch_fit)[1], 4)),
          paste("BIC:", round(infocriteria(values$garch_fit)[2], 4)),
          paste("Log-Likelihood:", round(likelihood(values$garch_fit), 4)),
          "",
          "Forecast Summary:",
          if (!is.null(values$forecast_result)) {
            paste("Forecast Horizon:", input$forecast_horizon, "days")
          } else {
            "No forecast generated."
          },
          "",
          sep = "\n"
        )
        
        writeLines(summary_text, file)
      }
    }
  )
  
  # Helper function for empty plotly
  plotly_empty <- function() {
    plot_ly() %>%
      layout(title = "No data available. Please load data first.")
  }
}

# Run the application
shinyApp(ui = ui, server = server)