# Economic Data Fetcher 📈

This repository contains tools for fetching and visualizing economic and market data:

1. A Streamlit-based web application that fetches and visualizes economic data from the Federal Reserve Economic Data (FRED) database.
2. A CLI tool for fetching market data (DJIA, S&P 500, NASDAQ) from Yahoo Finance.

## FRED Data Fetcher (Web App)

A Streamlit-based web application that fetches and visualizes economic data from the Federal Reserve Economic Data (FRED) database. This tool allows users to select multiple economic indicators, specify date ranges, and download the combined data as CSV files.

## Features

- 📊 Fetch multiple economic indicators simultaneously
- 📅 Customizable date range selection
- 📥 Download data as CSV files
- 📈 Basic data visualization
- 🔒 Secure API key management
- 🎯 Pre-configured popular economic indicators

## Prerequisites

- Python 3.x
- FRED API Key (free)

### Getting a FRED API Key

1. Visit [FRED API Key Registration](https://fred.stlouisfed.org/docs/api/api_key.html)
2. Create an account or sign in
3. Request an API key
4. The key will be sent to your email

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd economic-data
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Set your FRED API key either:
   - As an environment variable: `export FRED_API_KEY='your-api-key'`
   - Or enter it directly in the application's sidebar

2. Run the application:
```bash
streamlit run app.py
```

3. In the web interface:
   - Select one or more economic indicators from the sidebar
   - Choose your desired date range
   - Click to fetch data
   - Download the results as CSV

## Available Economic Indicators

The application includes several pre-configured economic indicators:

- **UNRATE**: Civilian Unemployment Rate
- **UMCSENT**: University of Michigan Consumer Sentiment
- **FEDFUNDS**: Effective Federal Funds Rate
- **CPIAUCSL**: Consumer Price Index
- **GDP**: Gross Domestic Product
- **GDPC1**: Real Gross Domestic Product
- **PCE**: Personal Consumption Expenditures
- **PCEDG**: Personal Consumption Expenditures: Durable Goods
- **PSAVERT**: Personal Saving Rate
- **M2SL**: M2 Money Stock
- **M1SL**: M1 Money Stock
- **DGS10**: 10-Year Treasury Rate
- **DGS2**: 2-Year Treasury Rate
- **T10Y2Y**: 10-Year Treasury Constant Maturity Minus 2-Year Treasury Constant Maturity
- **RECPROUSM156N**: Recession Probability
- **WALCL**: Total Assets (Less Eliminations from Consolidation)

## Extending the Application

The application is designed to be easily extensible:

1. Add new data sources by modifying the `fetch_fred_data` function
2. Include additional economic indicators by adding their FRED series codes
3. Modify the export functionality to support different formats (JSON, Excel, etc.)
4. Enhance visualization capabilities using Streamlit's charting features

## Dependencies

- streamlit
- pandas
- fredapi

## License

[Add your chosen license here]

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- Data provided by [FRED, Federal Reserve Bank of St. Louis](https://fred.stlouisfed.org/)
- Built with [Streamlit](https://streamlit.io/)

## Market Data CLI Tool

A Python CLI tool that fetches daily closing data for DJIA, S&P 500, and NASDAQ over a given date range and saves it to CSV.

### Setting up the Virtual Environment

First, ensure you have the required packages for creating virtual environments:

```bash
# On Debian/Ubuntu
sudo apt install python3-venv

# On other systems, the venv module might be included by default
```

Then create and activate the virtual environment:

```bash
cd economic-data
python3 -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate.bat       # Windows
pip install -r requirements.txt
```

### Usage

```bash
python fetch_market_data.py --start 2024-01-01 --end 2024-12-31 --out djia_sp500_nasdaq.csv
```

Command line arguments:
- `--start`: Start date in YYYY-MM-DD format (default: 2024-01-01)
- `--end`: End date in YYYY-MM-DD format (default: today)
- `--out`: Output CSV file path (default: market_data.csv)

### Future Extensions

The market data tool is designed for easy extension:
- Add support for fetching additional market symbols
- Implement data visualization and plotting
- Integrate with other economic indicators
- Add data transformation and analysis capabilities

## Dependencies

- streamlit
- pandas
- fredapi
- yfinance

## License

[Add your chosen license here] 