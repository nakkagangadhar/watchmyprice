from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def parse_product_page(url):
    print(f"Parsing URL: {url}")
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--ignore-ssl-errors")
    
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    service = Service(ChromeDriverManager().install())
    try:
        driver = webdriver.Chrome(service=service, options=options)
    except Exception as e:
        print(f"Failed to initialize ChromeDriver: {e}")
        return None, None

    try:
        print("Attempting to load page...")
        driver.get(url)
        print("Page loaded successfully")
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Check for error pages
        title = soup.find('title')
        if title and ("Access Denied" in title.text or "This site can’t be reached" in title.text):
            print(f"Error: Loaded an error page. Title: '{title.text}'")
            with open('error_page.html', 'w', encoding='utf-8') as f:
                f.write(str(soup.prettify()))
            print("Saved error page source to 'error_page.html'")
            return None, None

        if 'amazon.in' in url:
            print("Detected Amazon URL")
            return parse_amazon(soup)
        elif 'myntra.com' in url:
            print("Detected Myntra URL")
            return parse_myntra(soup)
        elif 'ajio.com' in url:
            print("Detected Ajio URL")
            return parse_ajio(soup)
        elif 'meesho.com' in url:
            print("Detected Meesho URL")
            return parse_meesho(soup)
        else:
            print(f"Unsupported URL: {url}")
            return None, None
    except Exception as e:
        print(f"Error loading page {url}: {e}")
        return None, None
    finally:
        driver.quit()

def parse_meesho(soup):
    try:
        product_name_element = soup.find('span', class_='sc-eDvSVe fhfLdV')
        if not product_name_element:
            product_name_element = soup.find('h1', class_='product-title')
        if not product_name_element:
            product_name_element = soup.find('h1') or soup.find('h2')

        product_name = product_name_element.text.strip() if product_name_element else None
        if not product_name:
            print("Meesho: Product name not found (tried 'sc-eDvSVe fhfLdV', 'product-title', h1/h2)")
            with open('meesho_page_source.html', 'w', encoding='utf-8') as f:
                f.write(str(soup.prettify()[:2000]))
            print("Meesho: Saved page source to 'meesho_page_source.html' for inspection")
            return None, None
        else:
            print(f"Meesho: Found product name: '{product_name}'")

        price_element = soup.find('h4', class_='sc-eDvSVe biMVPh')
        if not price_element:
            price_element = soup.find('span', class_='sc-eDvSVe kXnfkW')
        if not price_element:
            price_element = soup.find('div', class_='price')
        if not price_element:
            price_element = soup.find('span', class_='final-price')

        if price_element:
            current_price_text = price_element.text.replace('₹', '').replace(',', '').strip()
            try:
                current_price = float(current_price_text)
            except ValueError:
                print(f"Meesho: Could not convert price text to float: '{current_price_text}'")
                return product_name, None
        else:
            print("Meesho: Price element not found (tried 'sc-eDvSVe biMVPh', 'sc-eDvSVe kXnfkW', 'price' div, 'final-price')")
            current_price = None

        print(f"Meesho: Parsed - Name: {product_name}, Price: {current_price}")
        return product_name, current_price
    except Exception as e:
        print(f"Error parsing Meesho page: {e}")
        return None, None

def parse_myntra(soup):
    try:
        product_name_element = soup.find('h1', class_='pdp-title')
        if not product_name_element:
            product_name_element = soup.find('h1', class_='pdp-name')
        if not product_name_element:
            product_name_element = soup.find('div', class_='pdp-title')
        if not product_name_element:
            product_name_element = soup.find('h1') or soup.find('h2')
        if not product_name_element:
            product_name_element = soup.find('div', class_='pdp-product-detail') or soup.find('div', class_='pdp-info')

        product_name = product_name_element.text.strip() if product_name_element else None
        if not product_name:
            print("Myntra: Product name not found (tried 'pdp-title', 'pdp-name', 'pdp-title' div, h1/h2, 'pdp-product-detail', 'pdp-info')")
            with open('myntra_page_source.html', 'w', encoding='utf-8') as f:
                f.write(str(soup.prettify()[:2000]))
            print("Myntra: Saved page source to 'myntra_page_source.html' for inspection")
            return None, None
        else:
            print(f"Myntra: Found product name: '{product_name}'")

        price_element = soup.find('span', class_='pdp-price')
        if not price_element:
            price_element = soup.find('span', class_='discounted-price')
        if not price_element:
            price_element = soup.find('div', class_='pdp-price')
        if not price_element:
            price_element = soup.find('span', class_='pdp-mrp')
        if not price_element:
            price_element = soup.find('span', class_='pdp-cost')

        if price_element:
            current_price_text = price_element.text.replace('₹', '').replace(',', '').strip()
            try:
                current_price = float(current_price_text)
            except ValueError:
                print(f"Myntra: Could not convert price text to float: '{current_price_text}'")
                return product_name, None
        else:
            print("Myntra: Price element not found (tried 'pdp-price', 'discounted-price', 'pdp-price' div, 'pdp-mrp', 'pdp-cost')")
            current_price = None

        print(f"Myntra: Parsed - Name: {product_name}, Price: {current_price}")
        return product_name, current_price
    except Exception as e:
        print(f"Error parsing Myntra page: {e}")
        return None, None

def parse_amazon(soup):
    try:
        title = soup.find('span', id='productTitle')
        product_name = title.get_text(strip=True) if title else None
        if not product_name:
            print("Amazon: Product name not found with id 'productTitle'")
            return None, None

        price_whole = soup.find('span', class_='a-price-whole')
        price_fraction = soup.find('span', class_='a-price-fraction')
        if price_whole:
            whole_text = price_whole.get_text(strip=True).replace(',', '').replace('.', '')
            fraction_text = price_fraction.get_text(strip=True) if price_fraction else '00'
            price_text = f"{whole_text}.{fraction_text}"
            try:
                current_price = float(price_text)
            except ValueError:
                print(f"Amazon: Could not convert price text to float: '{price_text}'")
                return product_name, None
        else:
            print("Amazon: Price element not found with class 'a-price-whole'")
            return product_name, None

        print(f"Amazon: Parsed - Name: {product_name}, Price: {current_price}")
        return product_name, current_price
    except Exception as e:
        print(f"Error parsing Amazon page: {e}")
        return None, None

def parse_ajio(soup):
    try:
        product_name_element = soup.find('h1', class_='prod-name')
        product_name = product_name_element.text.strip() if product_name_element else None
        if not product_name:
            print("Ajio: Product name not found with class 'prod-name'")
            return None, None

        price_element = soup.find('div', class_='prod-sp')
        if price_element:
            current_price_text = price_element.text.replace('₹', '').replace(',', '').strip()
            try:
                current_price = float(current_price_text)
            except ValueError:
                print(f"Ajio: Could not convert price text to float: '{current_price_text}'")
                return product_name, None
        else:
            print("Ajio: Price element not found with class 'prod-sp'")
            current_price = None

        print(f"Ajio: Parsed - Name: {product_name}, Price: {current_price}")
        return product_name, current_price
    except Exception as e:
        print(f"Error parsing Ajio page: {e}")
        return None, None