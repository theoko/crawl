import requests
from bs4 import BeautifulSoup
import json
from elasticsearch import Elasticsearch

# Define the URL to crawl
url = "https://finviz.com/insidertrading.ashx?or=-10&tv=100000&tc=1&o=-transactionValue"

# Send a GET request to the URL
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
}
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # TODO: Write your code to extract data from the parsed HTML
    # Find all <a> tags with class "tab-link"
    links = soup.find_all("a", class_="tab-link")

    stock_tickers = []

    # Extract the text from each <a> tag
    for link in links:
        text = link.text
        # Check if the text is a stock ticker
        if len(text) <= 5 and text.isupper():
            stock_tickers.append(text)

    # Find all <td class="text-right">902,044</td>
    td = soup.find_all("td", class_="text-right")

    # Extract the text from each <td> tag
    amounts = []
    for td in td:
        text = td.text
        # Check if the text is a dollar amount (e.g., 902,044)
        if text.replace(",", "").isdigit():
            amounts.append(text)

    # Extract the text from this tag: E.g. <a href="http://www.sec.gov/Archives/edgar/data/1162194/000091957424003252/xslF345X05/ownership.xml" class="tab-link" target="_blank">May 17 08:11 PM</a>
    # It's wrapped in <td class="whitespace-nowrap text-center tabular-nums" onclick="ignoreOnClick=true;"><a href="http://www.sec.gov/Archives/edgar/data/1162194/000091957424003252/xslF345X05/ownership.xml" class="tab-link" target="_blank">May 17 08:11 PM</a></td>
    dates_td = soup.find_all("td", class_="whitespace-nowrap text-center tabular-nums", onclick="ignoreOnClick=true;")
    dates = []
    for date in dates_td:
        dates.append(date.text)

    # Create a list to store the extracted data
    data = []

    # Iterate over the extracted amounts
    for i, amount in enumerate(amounts):
        # every three entries correspond to a single stock ticker
        # Check if the index is divisible by 3
        if i % 3 == 0:
            # Calculate the index of the stock ticker
            index = i // 3
            # Check if the index is within the range of the stock tickers
            if index < len(stock_tickers):
                # Get the stock ticker using the index
                stock_ticker = stock_tickers[index]
                # Create a dictionary to store the stock ticker and amount
                stock_data = {
                    "symbol": stock_ticker, 
                    "num_shares": amount,
                    "dollar_value": amounts[i + 1],
                    "shares_total": amounts[i + 2],
                    "date": dates[index]
                }
                # Add the stock data to the list
                data.append(stock_data)

    # Sort by dollar_value
    data.sort(key=lambda x: int(x["dollar_value"].replace(",", "")), reverse=True)
    # Print the sorted data
    # print("Sorted by dollar_value:")
    # for info in data:
    #     print(info)

    # Store the entire HTML content (tags from begginning to end) into a JSON object
    json_data_finviz = json.dumps(soup.prettify())
    # Print the JSON object
    # print(json_data_finviz)

    # # Connect to Elasticsearch
    # es = Elasticsearch()

    # # Index the extracted data into Elasticsearch
    # for info in data:
    #     # Convert the dictionary to JSON
    #     json_data = json.dumps(info)
    #     # Index the JSON data into Elasticsearch
    #     es.index(index='stock_data', body=json_data)

    # # Confirm successful indexing
    # print("Data indexed into Elasticsearch.")

    # Get those which have a dollar_value greater than 1,000,000
    data_1m = []
    print("Transactions with dollar_value greater than 1,000,000:")
    for info in data:
        if int(info["dollar_value"].replace(",", "")) > 1000000:
            print(info)
            data_1m.append(info)
    
    # Check https://finance.yahoo.com/quote/ALLO/options for each symbol in data_1m
    # for info in data_1m:
    #     url_yahoo = "https://finance.yahoo.com/quote/" + info["symbol"] + "/options"
    #     response_yahoo = requests.get(url_yahoo, headers=headers)
    #     if response_yahoo.status_code == 200:
    #         soup_yahoo = BeautifulSoup(response_yahoo.content, "html.parser")
    #         json_data_yahoo = json.dumps(soup_yahoo.prettify())
            
    #     else:
    #         print("Failed to retrieve data from Yahoo Finance. Status code:", response_yahoo.status_code)

else:
    print("Failed to retrieve data. Status code:", response.status_code)

# Now crawl https://www.capitoltrades.com/trades?per_page=96&txType=buy
url_capitoltrades = "https://www.capitoltrades.com/trades?per_page=96&txType=buy"
response_capitoltrades = requests.get(url_capitoltrades, headers=headers)
if response_capitoltrades.status_code == 200:
    soup_capitoltrades = BeautifulSoup(response_capitoltrades.content, "html.parser")
    json_data_capitoltrades = json.dumps(soup_capitoltrades.prettify())

    # Extract text from all <span class="q-field issuer-ticker">FLJP:US</span>
    issuer_tickers = soup_capitoltrades.find_all("span", class_="q-field issuer-ticker")
    issuer_tickers_list = []
    for issuer_ticker in issuer_tickers:
        issuer_tickers_list.append(issuer_ticker.text)

    # print(json_data_capitoltrades)

    # Get text from all <td class="q-td  q-column--txDate"><div class="q-cell cell--tx-date"> <div class="q-cell cell--count-issuers flavour--lv"> <div class="q-label">2024</div><div class="q-value"> 25 Apr</div></div></div></td>
    tx_dates = soup_capitoltrades.find_all("td", class_="q-td q-column--txDate")
    tx_dates_list = []
    for tx_date in tx_dates:
        tx_dates_list.append(tx_date.text)
        # print(tx_date.text)
    
    # Associate issuers_tickers_list with tx_dates_list
    data_capitoltrades = []
    for i in range(len(issuer_tickers_list)):
        data_capitoltrades.append({"symbol": issuer_tickers_list[i], "date": tx_dates_list[i]})

    # If it ends with ":US", it's a US stock, add it to the final list as "FLJP" for example (without ":US")
    data_capitoltrades_us = []
    for info in data_capitoltrades:
        if info["symbol"].endswith(":US"):
            info["symbol"] = info["symbol"][:-3]
            data_capitoltrades_us.append(info)

    print(data_capitoltrades_us)

    # Check if the symbol is in the data_1m list
    print("Transactions with dollar_value greater than 1,000,000:")
    for info in data_1m:
        for info_capitol in data_capitoltrades_us:
            if info["symbol"] == info_capitol["symbol"]:
                print(info)
                print(info_capitol)

    # Store the data in data_1m and data_capitoltrades_us in Elasticsearch to later check if the same symbol appears in both
    # Connect to Elasticsearch
    es = Elasticsearch()

    # Index the extracted data into Elasticsearch
    for info in data_1m:
        # Convert the dictionary to JSON
        json_data = json.dumps(info)
        # Index the JSON data into Elasticsearch
        es.index(index='stock_data_insiders', body=json_data)

    for info in data_capitoltrades_us:
        # Convert the dictionary to JSON
        json_data = json.dumps(info)
        # Index the JSON data into Elasticsearch
        es.index(index='stock_data_politicians', body=json_data)
else:
    print("Failed to retrieve data from CapitolTrades. Status code:", response_capitoltrades.status_code)
