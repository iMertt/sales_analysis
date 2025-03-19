from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd

def generate_forecast(analyzer, months=3):
    # Get monthly sales data
    monthly_sales = analyzer.get_monthly_sales()
    
    # Prepare data for forecasting
    X = np.arange(len(monthly_sales)).reshape(-1, 1)
    y = monthly_sales.values
    
    # Train model
    model = LinearRegression()
    model.fit(X, y)
    
    # Generate forecast
    future_months = np.arange(len(monthly_sales), len(monthly_sales) + months).reshape(-1, 1)
    forecast = model.predict(future_months)
    
    # Create forecast DataFrame
    dates = pd.date_range(start=monthly_sales.index[-1], periods=months+1, freq='M')[1:]
    forecast_df = pd.Series(forecast, index=dates, name='Forecasted Revenue')
    
    return forecast_df