import pandas as pd

# Load the Excel file into a pandas DataFrame
df = pd.read_csv('NIFTY-50.csv')

df['Modified Daily Returns'] = df['Close '].diff() / df['Close '].shift(1)

# Display the results
print("Modified Daily Returns:")
print(df['Modified Daily Returns'].dropna())

# Calculate Daily Volatility
daily_volatility = df['Modified Daily Returns'].std()
print(f"Daily Volatility: {daily_volatility}")

# Calculate Annualized Volatility
length_of_data = len(df)
annualized_volatility = daily_volatility * (length_of_data ** 0.5)
print(f"Annualized Volatility: {annualized_volatility}")