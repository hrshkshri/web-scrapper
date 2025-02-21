import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

# Configure Chrome options
options = Options()
options.add_argument("--headless")  # Run in headless mode
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
all_products = []

for category_name, category_url in category_links.items():
    print(f"Scraping category: {category_name}")
    print(category_url)
    driver.get(category_url)
    time.sleep(3)

    # Find all product links
    product_elements = driver.find_elements(
        By.CSS_SELECTOR, "a.product-item-inner-wrap"
    )

    print(product_elements)
    product_links = [elem.get_attribute("href") for elem in product_elements]

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
                By.CSS_SELECTOR, "h1.product-tile__weight"
            ).text.rsplit(" ", 1)[0]
        except:
            quantity = "N/A"

        try:
            barcode = driver.find_element(By.CSS_SELECTOR, "div.product-remark").text
        except:
            barcode = "N/A"

        try:
            product_details = driver.find_element(
                By.CSS_SELECTOR, ".product-description"
            ).text
        except:
            product_details = "N/A"

        try:
            price = driver.find_element(
                By.CSS_SELECTOR, "div.span.product-Details-current-price"
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

        all_products.append(product_data)
        print(f"Scraped: {product_name}")

# Save data to JSON
with open("products.json", "w", encoding="utf-8") as f:
    json.dump(all_products, f, indent=4, ensure_ascii=False)

# Close driver
driver.quit()

print("Scraping completed. Data saved in products.json")
