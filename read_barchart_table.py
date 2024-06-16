from bs4 import BeautifulSoup

def extract_data_from_html(file_path):
    with open(file_path, 'r') as f:
        contents = f.read()

    soup = BeautifulSoup(contents, 'html.parser')
    
    # Iterate over each set-class element
    for set_class in soup.select('set-class'):
        # Extract the symbol
        symbol = set_class.select_one('div[class="_cell baseSymbol"]')
        if symbol:
            # print(symbol)   
            symbol = symbol.find('a')['href'].split('/')[-2]
            print(symbol)

            price = set_class.select_one('div[class="_cell _align_right underlyingLastPrice"]')
            if price:
                price.find('text-binding').decompose
                print(price)

        

data = extract_data_from_html('shadow_root_1.html')