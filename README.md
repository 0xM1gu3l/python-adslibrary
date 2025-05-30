## python-adslibrary: Facebook Ads Library on Python

> ⚠️ This code is still in development so there may have functions that don't work properly.

## Requirements

- Python >= 3.9.6

## Installation

```sh
git clone https://github.com/0xM1gu3l/python-adslibrary
cd python-adslibrary

python setup.py install # Windows
python3 setup.py install # MacOS/Linux
```

## Example code

```py
import adslibrary

# Variables
country = "US"
ad_category = "ALL" # ALL or POLITICAL_AND_ISSUE_ADS

# Initialize client
client = adslibrary.AdsLibrary(country, ad_category)

# Search by query
search_by_query = client.search(type="query", query="Something you want search")

#Search by Page ID
search_by_page_id = client.search(type="page", page_id="18490320840932")

# Search ads in a date range
search_by_query_with_date_range = client.search(type="query", query="Something you want search", date_min="2025-01-01", date_max="2025-01-16") # Return ads that match the query in between these dates

"""
The response will be a SearchResult object that can be used like this:
"""

print("Ad count:", search_by_query.ad_count)
print("Page names:", search_by_query.page_names)
print("Page IDs:", search_by_query.page_ids)
print("Date range:", search_by_query.date_range)
print("Ads:", search_by_query.ads) # This returns the full ad JSON object, it's big!
```

## TODO

- ✅ ~~Make search function~~
- Make some useful tools (Get ads every day in a date range, easy access to important values, etc)
- ...
