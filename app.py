import os
from fastapi import FastAPI, File, UploadFile, Query, HTTPException
import pandas as pd
import numpy as np

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}


def calculate_volatility(data: pd.DataFrame):
    # Assuming the CSV file has a column named 'Close' for closing prices
    closing_prices = data['Close']

    # Calculate daily returns
    daily_returns = closing_prices.pct_change()

    # Calculate daily volatility
    daily_volatility = np.std(daily_returns)

    # Annualize volatility (assuming 252 trading days in a year)
    annualized_volatility = daily_volatility * np.sqrt(252)

    return daily_volatility, annualized_volatility


@app.post("/calculate_volatility")
async def calculate_volatility_endpoint(
        file: UploadFile = File(None),
        directory: str = Query(None, description="Directory path to fetch data if file is not provided"),
):
    # Check if either file or directory is provided
    if not file and not directory:
        raise HTTPException(status_code=400, detail="Either file or directory must be provided.")

    # Load data from file or directory
    if file:
        content = await file.read()
        data = pd.read_csv(pd.compat.StringIO(content.decode('utf-8')))
    else:
        # Assuming all CSV files in the directory should be considered
        files_in_directory = [f"{directory}/{file}" for file in os.listdir(directory) if file.endswith(".csv")]
        if not files_in_directory:
            raise HTTPException(status_code=400, detail=f"No CSV files found in the directory: {directory}")

        # Load data from the first CSV file in the directory
        data = pd.read_csv(files_in_directory[0])

    # Check if the CSV file has a 'Close' column
    if 'Close' not in data.columns:
        raise HTTPException(status_code=400, detail="CSV file must contain a 'Close' column for closing prices.")

    # Calculate volatility
    daily_volatility, annualized_volatility = calculate_volatility(data)

    return {"daily_volatility": daily_volatility, "annualized_volatility": annualized_volatility}
