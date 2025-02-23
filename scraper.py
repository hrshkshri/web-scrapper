import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

TEST_MODE = False
PRODUCT_LIMIT = 3 if TEST_MODE else None

# Configure Chrome options
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Initialize WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Define URL
base_url = "https://www.tops.co.th/en"
driver.get(base_url)
time.sleep(3)  # Allow page to load

# Step 1: Extract product categories
categories = driver.find_elements(By.CSS_SELECTOR, "nav a")
category_links = {
    category.text: category.get_attribute("href") for category in categories[:12]
}

# Step 2: Extract product data from each category
categorized_products = {}

for category_name, category_url in category_links.items():
    print(f"Scraping category: {category_name}")
    print(category_url)
    driver.get(category_url)
    time.sleep(3)

    # Find all product links
    product_elements = driver.find_elements(
        By.CSS_SELECTOR, "a.product-item-inner-wrap"
    )
    product_links = [elem.get_attribute("href") for elem in product_elements]

    if TEST_MODE:
        product_links = product_links[:PRODUCT_LIMIT]  # Limit products if in test mode

    categorized_products[category_name] = []

    for product_url in product_links:
        driver.get(product_url)
        time.sleep(2)

        # Extract product details
        try:
            product_name = driver.find_element(
                By.CSS_SELECTOR, "h1.product-tile__name"
            ).text
        except:
            product_name = "N/A"

        try:
            images = driver.find_elements(By.CSS_SELECTOR, "img.xzoom")
            image_urls = [img.get_attribute("src") for img in images]
        except:
            image_urls = []

        try:
            quantity = driver.find_element(
                By.CSS_SELECTOR, "h1.product-tile__name"
            ).text.rsplit(" ", 1)[0]
        except:
            quantity = "N/A"

        try:
            barcode = driver.find_element(
                By.CSS_SELECTOR, "div.product-Details-sku"
            ).text
        except:
            barcode = "N/A"

        try:
            product_details = driver.find_element(
                By.CSS_SELECTOR, "div.accordion-body"
            ).text
        except:
            product_details = "N/A"

        try:
            price = driver.find_element(
                By.CSS_SELECTOR, "span.product-Details-current-price"
            ).text
        except:
            price = "N/A"

        try:
            labels = [
                label.text
                for label in driver.find_elements(
                    By.CSS_SELECTOR, "p.product-Details-seasonal-label"
                )
            ]
        except:
            labels = []

        # Store data
        product_data = {
            "name": product_name,
            "images": image_urls,
            "quantity": quantity,
            "barcode": barcode,
            "details": product_details,
            "price": price,
            "labels": labels,
            "url": product_url,
        }

        categorized_products[category_name].append(product_data)
        print(f"Scraped: {product_name}")

# Save data to JSON
with open("products.json", "w", encoding="utf-8") as f:
    json.dump(categorized_products, f, indent=4, ensure_ascii=False)

# Close driver
driver.quit()

print("Scraping completed. Data saved in products.json")
