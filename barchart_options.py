import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

# Setup ChromeDriver (ensure the path is correct for your ChromeDriver)
service = Service(executable_path="./chromedriver")

# Create a new instance of Chrome Options
chrome_options = Options()

# Add the path to the unpacked extension
chrome_options.add_argument("--load-extension=./adblock")

# Start the WebDriver with the options
driver = webdriver.Chrome(service=service, options=chrome_options)

# Maximize the window
driver.maximize_window()

# URL to scrape
url = "https://www.barchart.com/options/naked-puts?orderBy=potentialReturn&orderDir=desc"

print("Sleeping for 5 seconds, to wait for AdBlock to load. Then, will navigate to the URL.")
time.sleep(5)

# Navigate to the URL
driver.get(url)

# Focus on tab 1
driver.switch_to.window(driver.window_handles[0])

try:
    # Try to locate div.bc-table-wrapper no-top-border table-guid-a584692d-f637-e2ba-f9c8-523e2ee6b357 links-enabled symbol-details sticky-row table-size-20
    print("Trying to find table")
    
    table = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "bc-table-wrapper"))
    )
    print("Table found!")

    # Click on button with id="onetrust-accept-btn-handler"
    driver.find_element(By.ID, "onetrust-accept-btn-handler").click()

    # Scroll until the element is visible
    actions = ActionChains(driver)
    actions.move_to_element(table).perform()

    # Alternative scrolling method (scroll by pixels)
    while True:
        try:
            table.is_displayed()
            break
        except:
            driver.execute_script("window.scrollBy(0, 100);")
            time.sleep(1)

    driver.execute_script("window.scrollBy(0, 380);")
    time.sleep(5)

    # Take a screenshot of the table
    table.screenshot("table.png")

    # print(table.get_attribute("innerHTML"))

    # print("Trying to find shadow root")

    # JavaScript to find all shadow hosts and retrieve their shadow roots
    script = '''
    let shadowHosts = document.querySelectorAll("*");
    let shadowRoots = [];
    shadowHosts.forEach(el => {
        if (el.shadowRoot) {
            shadowRoots.push(el.shadowRoot);
        }
    });
    return shadowRoots;
    '''

    # Execute the script to get all shadow roots
    shadow_roots = driver.execute_script(script)

    # Print the shadow roots
    print("Number of shadow roots found: ", len(shadow_roots))
    for i, root in enumerate(shadow_roots):
        print(f"Shadow Root {i+1}: {root}")
        # Print object keys
        print("Keys: ", dir(root))
        # print("root.find_element(By.ID, '_root'): ", root.find_element(By.ID, "_root"))
        # print("root.find_element(By.ID, '_root').get_attribute('innerHTML'): ", root.find_element(By.ID, "_root").get_attribute("innerHTML"))
        
        html_content = root.find_element(By.ID, "_grid").get_attribute("innerHTML")

        soup = BeautifulSoup(html_content, 'html.parser')

        # Iterate over each set-class element
        for set_class in soup.select('set-class'):
            # Extract the symbol
            symbol = set_class.select_one('div[class="_cell baseSymbol"]')
            if symbol:
                # print(symbol)   
                symbol = symbol.find('a')['href'].split('/')[-2]
                # print(symbol)

                # price = set_class.select_one('div[class="_cell _align_right underlyingLastPrice"]')
                # if price:
                    # Need to extract text-binding which has a shadow root which contains the text we need
                    

except Exception as e:
    print(e)

print("Sleeping for 5 seconds")
time.sleep(5)

# Wait for a specific element to ensure the page has loaded
# Adjust the selector as needed for your target element
# WebDriverWait(driver, 10).until(
#     EC.presence_of_element_located((By.CSS_SELECTOR, "div.bc-datatable ng-isolate-scope"))
# )

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

