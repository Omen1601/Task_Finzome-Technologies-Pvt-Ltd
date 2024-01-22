import pandas as pd
from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI with Stock Volatility Calculations"}


@app.get("/calculate_volatility")
def calculate_volatility(csv_file_path: str):
    # Load data from CSV file
    stock_data = pd.read_csv(csv_file_path)

    # 1. Daily Returns
    stock_data['Daily Returns'] = stock_data['Close'].pct_change()

    # 2. Daily Volatility
    daily_volatility = stock_data['Daily Returns'].std()

    # 3. Annualized Volatility
    annualized_volatility = daily_volatility * (252 ** 0.5)  # Assuming 252 trading days in a year

    return {
        'Daily Volatility': daily_volatility,
        'Annualized Volatility': annualized_volatility
    }
