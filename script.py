import requests
import openai
from dotenv import load_dotenv
import os
import csv
load_dotenv()

POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")

LIMIT = 1000

url = f'https://api.polygon.io/v3/reference/tickers?market=stocks&active=true&order=asc&limit={LIMIT}&sort=ticker&apiKey={POLYGON_API_KEY}'

response = requests.get(url)
tickers = []

data = response.json()
for stock in data['results']:
    tickers.append(stock)

while 'next_url' in data and data['next_url']:
    print('requesting next page', data['next_url'])
    next_url = data['next_url'] + f'&apiKey={POLYGON_API_KEY}'
    try:

        response = requests.get(next_url)
        data = response.json()
        print (data)
        for stock in data['results']:
            tickers.append(stock)
    except Exception as e:
        print("Error fetching next page:", e)
        break

example_ticker = {
    'ticker': 'HTB', 
    'name': 'HomeTrust Bancshares, Inc.', 
    'market': 'stocks', 
    'locale': 'us', 
    'primary_exchange': 'XNYS', 
    'type': 'CS', 
    'active': True, 
    'currency_name': 'usd', 
    'cik': '0001538263', 
    'composite_figi': 'BBG002CV5W70', 
    'share_class_figi': 'BBG002CV5WZ9', 
    'last_updated_utc': '2025-09-20T06:05:17.34210598Z'}


print(len(tickers))

# Write tickers to CSV matching the schema of `example_ticker`
fields = [
    'ticker', 'name', 'market', 'locale', 'primary_exchange',
    'type', 'active', 'currency_name', 'cik', 'composite_figi',
    'share_class_figi', 'last_updated_utc'
]

output_path = 'tickers.csv'
with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fields)
    writer.writeheader()
    for stock in tickers:
        row = {}
        for f in fields:
            v = stock.get(f, '') if isinstance(stock, dict) else ''
            if v is None:
                v = ''
            # Convert non-primitive types to string; booleans will become 'True'/'False'
            if not isinstance(v, (str, int, float, bool)):
                v = str(v)
            row[f] = v
        writer.writerow(row)

print(f"Wrote {len(tickers)} rows to {output_path}")