#!/usr/bin/env python3
"""
Fetch market data (DJIA, S&P 500, NASDAQ) from Yahoo Finance and save to CSV.
"""
import argparse
import datetime
import pandas as pd
import yfinance as yf


def fetch_data(symbols: list[str], start: str, end: str) -> pd.DataFrame:
    """
    Fetch daily closing data for specified market symbols over a date range.

    Args:
        symbols: List of Yahoo Finance ticker symbols
        start: Start date in YYYY-MM-DD format
        end: End date in YYYY-MM-DD format

    Returns:
        DataFrame containing adjusted close prices for all symbols
    """
    # Map of ticker symbols to display names
    ticker_map = {
        "^DJI": "DJIA",
        "^GSPC": "SP500", 
        "^IXIC": "NASDAQ"
    }
    
    # Download data
    data = yf.download(symbols, start=start, end=end)
    
    # Extract adjusted close prices if available, otherwise use regular close
    try:
        if 'Adj Close' in data.columns:
            price_data = data['Adj Close']
        else:
            # Handle case where data might be in a different structure
            price_data = data['Close']
    except KeyError:
        # If we have a multi-level column index, try to access it differently
        if isinstance(data.columns, pd.MultiIndex):
            # Try to get 'Adj Close' from the first level of MultiIndex
            if 'Adj Close' in data.columns.levels[0]:
                price_data = data['Adj Close']
            else:
                price_data = data['Close']
        else:
            # Fallback to just returning all the data
            price_data = data
    
    # Rename columns from ticker symbols to plain names
    if hasattr(price_data, 'columns'):
        price_data.columns = [ticker_map.get(symbol, symbol) for symbol in price_data.columns]
    
    # Calculate daily percentage changes and add as new columns
    result_df = price_data.copy()
    
    # For each column, calculate the daily percentage change
    for column in result_df.columns:
        # Calculate percentage change: (current_value - previous_value) / previous_value * 100
        change_col_name = f"{column}-change"
        result_df[change_col_name] = result_df[column].pct_change() * 100
    
    # Reorder columns to interleave values and their changes
    reordered_columns = []
    for column in price_data.columns:
        reordered_columns.append(column)
        reordered_columns.append(f"{column}-change")
    
    # Return the DataFrame with original values and percentage changes
    return result_df[reordered_columns]


def save_to_csv(df: pd.DataFrame, filename: str):
    """
    Save DataFrame to CSV file.

    Args:
        df: DataFrame to save
        filename: Output file path
    """
    df.to_csv(filename)
    

def main():
    """Parse command line arguments and fetch market data."""
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Fetch market data for DJIA, S&P 500, and NASDAQ"
    )
    
    # Add command line arguments
    today = datetime.date.today().strftime("%Y-%m-%d")
    parser.add_argument("--start", default="2024-01-01", help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end", default=today, help="End date (YYYY-MM-DD)")
    parser.add_argument("--out", default="market_data.csv", help="Output CSV file path")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Default market symbols
    symbols = ["^DJI", "^GSPC", "^IXIC"]  # DJIA, S&P 500, NASDAQ
    
    # Fetch data and save to CSV
    data = fetch_data(symbols, args.start, args.end)
    save_to_csv(data, args.out)
    
    print(f"Saved to {args.out}")


if __name__ == "__main__":
    main() 