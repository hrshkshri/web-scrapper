# Tops.co.th Web Scraper

A Python-based web scraper that extracts product information from Tops.co.th online supermarket website.

## Description

This scraper navigates through the Tops.co.th website to collect detailed product information across different categories. It extracts data such as:

- Product names
- Images
- Quantities
- Barcodes
- Product details
- Prices
- Special labels
- Product URLs

## Prerequisites

- Python 3.x
- Chrome browser installed

## Installation

1. Clone this repository:

```bash
git clone https://github.com/hrshkshri/web-scrapper.git
```

2. Install required dependencies:

```bash
pip install selenium webdriver-manager
```

## Configuration

The script includes two configuration options at the top:

```python
TEST_MODE = True  # Set to False for full scraping
PRODUCT_LIMIT = 3  # Number of products to scrape per category in test mode
```

## Usage

1. Run the script:

```bash
python scraper.py
```

2. The script will:
   - Launch a headless Chrome browser
   - Navigate through product categories
   - Extract product information
   - Save the data to `products.json`

## Output

The scraped data is saved in JSON format with the following structure:

```json
{
  "Category Name": [
    {
      "name": "Product Name",
      "images": ["image_url1", "image_url2"],
      "quantity": "Product Quantity",
      "barcode": "Product Barcode",
      "details": "Product Details",
      "price": "Product Price",
      "labels": ["label1", "label2"],
      "url": "product_url"
    }
  ]
}
```

## Features

- Headless browser operation
- Test mode for limited scraping
- Structured JSON output
- Category-based organization

## Notes

- The script includes delays to respect the website's loading times
- Error handling ensures the script continues even if some data is unavailable
- In test mode, only the first 3 products from each category are scraped
- In case you want to scrape more products, you can set `TEST_MODE` to `False` OR increase `PRODUCT_LIMIT` as per your requirement.


