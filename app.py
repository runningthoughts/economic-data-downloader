# Dependencies: streamlit, pandas, fredapi

import streamlit as st
import pandas as pd
from fredapi import Fred
from datetime import datetime
import os

# --- App Configuration ---
st.set_page_config(layout="wide")

# --- App Header and README Text ---
st.title("📈 Economic Data Fetcher")
st.markdown("""
This application fetches economic data series from the Federal Reserve Economic Data (FRED) database.
You can select multiple series, specify a date range, and download the combined data as a CSV file.

**No other APIs are needed for basic FRED data.**

To extend this app:
- You can swap in other data sources by editing the `fetch_fred_data` function.
- Consider adding data from sources like the Census Bureau or other economic APIs.
- You could modify the export functionality to support JSON or other formats.
""")

# --- Economic Indicator Explanations ---
# These are the default series codes and their meanings:
# UNRATE: Civilian Unemployment Rate - The percentage of the labor force that is jobless.
# UMCSENT: University of Michigan: Consumer Sentiment - An index tracking consumer confidence.
# FEDFUNDS: Effective Federal Funds Rate - The target rate set by the FOMC for interbank lending.
# CPIAUCSL: Consumer Price Index for All Urban Consumers: All Items in U.S. City Average - A measure of average change over time in the prices paid by urban consumers for a market basket of consumer goods and services.

# --- Sidebar Inputs ---
st.sidebar.header("⚙️ Configuration")

# Get API key from environment variable
api_key = os.environ.get("FRED_API_KEY", "")

# Optional API Key Input (for override)
if not api_key:
    api_key = st.sidebar.text_input(
        "FRED API Key",
        type="password",
        help="Get your free API key from https://fred.stlouisfed.org/docs/api/api_key.html"
    )
else:
    st.sidebar.success("✅ Using FRED API key from environment variable")

# Multi-select for FRED series codes
default_series = ["UNRATE", "UMCSENT", "FEDFUNDS", "CPIAUCSL"]
selected_series_codes = st.sidebar.multiselect(
    "Select FRED Series Codes",
    options=[
        "UNRATE", "UMCSENT", "FEDFUNDS", "CPIAUCSL",  # Defaults
        "GDP", "GDPC1", "PCE", "PCEDG", "PSAVERT", "M2SL", "M1SL", # More common series
        "DGS10", "DGS2", "T10Y2Y", # Treasury yields and spread
        "RECPROUSM156N", # Recession Probability
        "WALCL" # Assets: Total Assets: Total Assets (Less Eliminations from Consolidation)
    ],
    default=default_series,
    help="Select one or more series. For a list of series, visit the FRED website."
)

# Date inputs for Start and End Date
default_start_date = datetime(2020, 1, 1)
default_end_date = datetime.now()

start_date = st.sidebar.date_input(
    "Start Date",
    value=default_start_date,
    min_value=datetime(1900, 1, 1),
    max_value=default_end_date,
    format="YYYY-MM-DD"
)

end_date = st.sidebar.date_input(
    "End Date",
    value=default_end_date,
    min_value=start_date, # Ensures end_date is not before start_date
    max_value=default_end_date,
    format="YYYY-MM-DD"
)

# Text input for Output filename
output_filename = st.sidebar.text_input(
    "Output Filename (.csv)",
    value="econ_data.csv"
)

# --- Data Fetching Logic ---
@st.cache_data # Cache the data to avoid re-fetching on every interaction
def fetch_fred_data(api_key_input, series_codes_list, start_dt, end_dt):
    """
    Fetches specified series from FRED as a single DataFrame, aligns them to month-start,
    and forward/backward fills missing values.

    Args:
        api_key_input (str): The FRED API key.
        series_codes_list (list): A list of FRED series IDs.
        start_dt (datetime.date): The start date for fetching data.
        end_dt (datetime.date): The end date for fetching data.

    Returns:
        pandas.DataFrame: A DataFrame with a 'date' column and one column per series,
                          or None if fetching fails or no series are selected.
    """
    if not api_key_input:
        st.error("⚠️ FRED API Key is required.")
        return None
    if not series_codes_list:
        st.warning("ℹ️ No series selected.")
        return None

    try:
        fred = Fred(api_key=api_key_input)
        
        # Convert dates to required string format
        start_date_str = start_dt.strftime('%Y-%m-%d')
        end_date_str = end_dt.strftime('%Y-%m-%d')
        
        # Fetch each series individually and combine them
        dfs = []
        for series_id in series_codes_list:
            try:
                series_data = fred.get_series(
                    series_id,
                    observation_start=start_date_str,
                    observation_end=end_date_str
                )
                if not series_data.empty:
                    df = pd.DataFrame(series_data)
                    df.columns = [series_id]
                    dfs.append(df)
            except Exception as e:
                st.warning(f"⚠️ Error fetching series {series_id}: {str(e)}")
        
        if not dfs:
            st.warning("⚠️ No data returned for any of the selected series in the specified date range.")
            return None
            
        # Combine all series into a single DataFrame
        df = pd.concat(dfs, axis=1)
        
        # Convert index to month-start timestamps
        df.index = pd.to_datetime(df.index).to_period("M").to_timestamp()
        
        # Sort by date, fill missing values, and reset index
        df = df.sort_index().ffill().bfill().reset_index().rename(columns={"index": "date"})
        
        return df

    except Exception as e:
        st.error(f"❌ An error occurred during data fetching: {e}")
        return None

# --- Main Application Logic ---
if api_key:
    if selected_series_codes:
        if start_date > end_date:
            st.error("⚠️ Error: Start Date cannot be after End Date.")
        else:
            st.info(f"Fetching data for: {', '.join(selected_series_codes)} from {start_date} to {end_date}...")

            # Add a spinner while data is being fetched
            with st.spinner("🔄 Fetching data from FRED..."):
                df_econ_data = fetch_fred_data(api_key, selected_series_codes, start_date, end_date)

            if df_econ_data is not None and not df_econ_data.empty:
                st.success("✅ Data fetched successfully!")
                st.dataframe(df_econ_data.head()) # Display a preview of the DataFrame

                # --- Data Download ---
                # Prepare CSV data for download
                csv_data = df_econ_data.to_csv(index=False).encode('utf-8')

                st.download_button(
                    label="📥 Download CSV",
                    data=csv_data,
                    file_name=output_filename if output_filename.endswith(".csv") else f"{output_filename}.csv",
                    mime='text/csv',
                    help=f"Downloads the combined economic data as '{output_filename}'"
                )

                # --- Optional: Display Chart ---
                # You can extend this to plot the data
                # Example: Plotting the first selected series if data is available
                st.subheader("📊 Data Visualization (Example)")
                if not df_econ_data.empty and selected_series_codes[0] in df_econ_data.columns:
                    try:
                        chart_data = df_econ_data.set_index('date')[[selected_series_codes[0]]].dropna()
                        if not chart_data.empty:
                             st.line_chart(chart_data)
                        else:
                            st.info(f"No data available to plot for {selected_series_codes[0]} after processing.")
                    except Exception as e:
                        st.warning(f"Could not plot data: {e}")
                else:
                    st.info("Select series and fetch data to see a chart.")

            elif df_econ_data is None: # Handled by errors/warnings in fetch_fred_data
                pass
            else: # df_econ_data is an empty DataFrame
                st.info("ℹ️ No data was returned for the selected series and date range.")
    else: # No series selected
        st.info("Select one or more series codes in the sidebar to begin.")
else:
    st.warning("Please enter your FRED API Key in the sidebar to fetch data or set the FRED_API_KEY environment variable.")

# --- Footer ---
st.markdown("---")
st.markdown("Built with Streamlit, Pandas, and FRED API.")
st.markdown("Data source: [FRED, Federal Reserve Bank of St. Louis](https://fred.stlouisfed.org/)")

# --- Extension Point Comments ---
# To add data from other sources (e.g., Census Bureau API):
# 1. Identify the API and required libraries (e.g., `requests`).
# 2. Create a new function similar to `fetch_fred_data` for the new source.
#    - This function should handle API authentication, data fetching, and initial processing.
# 3. Modify the main app logic to call your new function.
# 4. You might need to merge or align data from different sources if they have different frequencies or date stamps.
#    - Pandas `merge` or `concat` functions will be useful.
#    - Consider a common date index for alignment.

# To change the output format (e.g., to JSON):
# 1. In the download section, instead of `df_econ_data.to_csv()`, use `df_econ_data.to_json()`.
# 2. Update the `mime` type in `st.download_button` (e.g., to `application/json`).
# 3. Change the default `output_filename`