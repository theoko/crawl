import requests
from bs4 import BeautifulSoup

# Define the URL to crawl
url = "https://finviz.com/insidertrading.ashx?tc=1"

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
                    "value": amounts[i + 1],
                    "shares_total": amounts[i + 2],
                }
                # Add the stock data to the list
                data.append(stock_data)

    # Print the extracted data
    for info in data:
        print(info)

else:
    print("Failed to retrieve data. Status code:", response.status_code)
