import pandas as pd
import os
from fredapi import Fred

# Try to get API key from environment variable, fallback to hardcoded value
api_key = os.environ.get("FRED_API_KEY", "")
fred = Fred(api_key=api_key)

unrate = fred.get_series(
    'UNRATE',
    observation_start='2024-01-01',
    observation_end='2025-04-30'
)
print("UNRATE count:", len(unrate))
print(unrate.head(), unrate.tail())

print("Index min/max:", unrate.index.min(), unrate.index.max())
print("Index freq:", unrate.index.freq)

df = pd.DataFrame({'UNRATE': unrate})
df = df.reset_index().rename(columns={'index':'date'})
print(df.head())
