# Stock Trends
Building a script to:

Step 1:
* Crawl the barchart.com website and collect the current put option selling opportunities. Then, calculate the probability of profit for each one of those and sort them by that probability. Insert data into the DB.
* Crawl the finviz.com website and collect information on insider transactions. Insert data into the DB.
* Crawl the capitoltrades.com website and collect information on transactions. Insert data into the DB.

Step 2:
* Crawl whalewisdom.com for each symbol collected. Insert data into the DB.

Step 3:
* Find which stock is trending based on the above information. If a stock appears in the barchart.com website, finviz.com, capitoltrades.com, and hedge funds are buying it (according to whalewisdom.com), then it is considered to be trending.

Step 4:
* Display the stocks in the UI sorted by popularity.

## Concerns:
* Compatibility across multiple systems. Since the program opens a chrome window to get the barchart info, the resolution of the display matters.
