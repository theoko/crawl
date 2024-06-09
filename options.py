import numpy as np
import scipy.stats as stats
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def probability_of_profit(current_price, strike_price, premium_received, iv, days_to_expiration):
    breakeven_point = strike_price - premium_received
    expected_move = current_price * iv * np.sqrt(days_to_expiration / 365)
    
    # Calculate z-score
    z_score = (np.log(breakeven_point / current_price)) / (iv * np.sqrt(days_to_expiration / 365))
    
    # Calculate POP
    pop = stats.norm.cdf(z_score)
    
    return pop

# Example usage
current_price = 50  # Current stock price
strike_price = 45   # Strike price of the put option
premium_received = 2  # Premium received for writing the put option
iv = 0.30  # Implied volatility (30%)
days_to_expiration = 30  # Days to expiration

pop = probability_of_profit(current_price, strike_price, premium_received, iv, days_to_expiration)
# print(f"The probability of profit is: {pop:.2%}")

# Setup ChromeDriver (ensure the path is correct for your ChromeDriver)
service = Service(executable_path="./chromedriver")
driver = webdriver.Chrome(service=service)

# URL to scrape
url = "https://www.barchart.com/options/naked-puts?orderBy=potentialReturn&orderDir=desc"

# Navigate to the URL
driver.get(url)

# Wait for a specific element to ensure the page has loaded
# Adjust the selector as needed for your target element
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "div.baseSymbol"))
)

# Now that the page is loaded, get the page source
html_source = driver.page_source

# Close the browser
driver.quit()

# Parse the page source with BeautifulSoup
soup = BeautifulSoup(html_source, 'html.parser')

# Your existing safe_get_text function and data extraction logic goes here
# Define a function to safely extract text from a BeautifulSoup find operation
def safe_get_text(soup, tag, class_name):
    element = soup.find(tag, class_=class_name)
    return element.get_text(strip=True) if element else None

# Example of using the safe_get_text function
# Initialize a dictionary to hold the extracted data
extracted_data = {}

# Use the safe_get_text function for each piece of information
extracted_data['baseSymbol'] = safe_get_text(soup, "div", "baseSymbol")
extracted_data['underlyingLastPrice'] = safe_get_text(soup, "div", "underlyingLastPrice")
extracted_data['strikePrice'] = safe_get_text(soup, "div", "strikePrice")
extracted_data['moneyness'] = safe_get_text(soup, "div", "moneyness")
extracted_data['expirationDate'] = safe_get_text(soup, "div", "expirationDate")
extracted_data['bidPrice'] = safe_get_text(soup, "div", "bidPrice")
extracted_data['breakEvenBid'] = safe_get_text(soup, "div", "breakEvenBid")
extracted_data['breakEvenPercent'] = safe_get_text(soup, "div", "breakEvenPercent")
extracted_data['volume'] = safe_get_text(soup, "div", "volume")
extracted_data['openInterest'] = safe_get_text(soup, "div", "openInterest")
extracted_data['volatility'] = safe_get_text(soup, "div", "volatility")
extracted_data['delta'] = safe_get_text(soup, "div", "delta")
extracted_data['potentialReturn'] = safe_get_text(soup, "div", "potentialReturn")
# Add other fields as before

# <set-class class="row _grid_columns selected" role="row" target="." binding="this.rowClass"><div class="_cell" role="cell" draggable="true" tabindex="0"><set-class binding="this.flags." target=".."></set-class><div class="text-center">
            #     <i class="bc-glyph-plus bc-symbol-widgets-modal"></i>
            # </div></div><div class="_cell selected baseSymbol" role="cell" draggable="true" tabindex="0"><set-class binding="this.flags.baseSymbol" target=".."></set-class><a href="/stocks/quotes/GME/overview">
            #     <set-property target=".." binding="this['baseSymbolLink']" property="href" style="display: none;"></set-property>
            #     <text-binding binding="this.baseSymbol"></text-binding>
            # </a></div><div class="_cell _align_right underlyingLastPrice" role="cell" draggable="true" tabindex="0"><set-class binding="this.flags.underlyingLastPrice" target=".."></set-class><text-binding fallbackvalue=" " binding="this.underlyingLastPrice"></text-binding></div><div class="_cell strikePrice" role="cell" draggable="true" tabindex="0"><set-class binding="this.flags.strikePrice" target=".."></set-class><text-binding fallbackvalue=" " binding="this.strikePrice"></text-binding></div><div class="_cell _align_right moneyness up" role="cell" draggable="true" tabindex="0"><set-class binding="this.flags.moneyness" target=".."></set-class><text-binding fallbackvalue=" " binding="this.moneyness"></text-binding></div><div class="_cell expirationDate" role="cell" draggable="true" tabindex="0"><set-class binding="this.flags.expirationDate" target=".."></set-class><text-binding fallbackvalue=" " binding="this.expirationDate"></text-binding></div><div class="_cell _align_right bidPrice" role="cell" draggable="true" tabindex="0"><set-class binding="this.flags.bidPrice" target=".."></set-class><text-binding fallbackvalue=" " binding="this.bidPrice"></text-binding></div><div class="_cell _align_right breakEvenBid" role="cell" draggable="true" tabindex="0"><set-class binding="this.flags.breakEvenBid" target=".."></set-class><text-binding fallbackvalue=" " binding="this.breakEvenBid"></text-binding></div><div class="_cell _align_right breakEvenPercent up" role="cell" draggable="true" tabindex="0"><set-class binding="this.flags.breakEvenPercent" target=".."></set-class><text-binding fallbackvalue=" " binding="this.breakEvenPercent"></text-binding></div><div class="_cell _align_right volume" role="cell" draggable="true" tabindex="0"><set-class binding="this.flags.volume" target=".."></set-class><text-binding fallbackvalue=" " binding="this.volume"></text-binding></div><div class="_cell _align_right openInterest" role="cell" draggable="true" tabindex="0"><set-class binding="this.flags.openInterest" target=".."></set-class><text-binding fallbackvalue=" " binding="this.openInterest"></text-binding></div><div class="_cell _align_right volatility" role="cell" draggable="true" tabindex="0"><set-class binding="this.flags.volatility" target=".."></set-class><text-binding fallbackvalue=" " binding="this.volatility"></text-binding></div><div class="_cell _align_right delta" role="cell" draggable="true" tabindex="0"><set-class binding="this.flags.delta" target=".."></set-class><text-binding fallbackvalue=" " binding="this.delta"></text-binding></div><div class="_cell _align_right potentialReturn" role="cell" draggable="true" tabindex="0"><set-class binding="this.flags.potentialReturn" target=".."></set-class><text-binding fallbackvalue=" " binding="this.potentialReturn"></text-binding></div><div class="_cell _align_right potentialReturnAnnual" role="cell" draggable="true" tabindex="0"><set-class binding="this.flags.potentialReturnAnnual" target=".."></set-class><text-binding fallbackvalue=" " binding="this.potentialReturnAnnual"></text-binding></div><div class="_cell _align_right tradeTime" role="cell" draggable="true" tabindex="0"><set-class binding="this.flags.tradeTime" target=".."></set-class><text-binding fallbackvalue=" " binding="this.tradeTime"></text-binding></div><div class="_cell _align_center" role="cell" draggable="true" tabindex="0"><set-class binding="this.flags." target=".."></set-class><div class="bc-datatable-quicklinks-toggler">
            #     <i class="bc-glyph-ellipsis-v bc-datatable-quicklinks-toggler-open"></i>
            #     <i class="bc-glyph-times bc-datatable-quicklinks-toggler-close"></i>
            # </div></div></set-class>

