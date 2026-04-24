from bs4 import BeautifulSoup

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Extract product data from the HTML table, ignoring boilerplate.


def parse_html_catalog(file_path: str) -> list[dict]:
    # --- FILE READING (Handled for students) ---
    with open(file_path, encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    # ------------------------------------------

    table = soup.find('table', id='main-catalog')
    if not table:
        return []

    def clean_price(val):
        val = val.strip().lower()
        if val in ['n/a', 'liên hệ']:
            return 0.0
        val = val.replace('vnd', '').replace(',', '').strip()
        try:
            return float(val)
        except:
            return 0.0

    results = []
    rows = table.find('tbody').find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        if len(cols) < 6:
            continue
            
        product_id = cols[0].text.strip()
        product_name = cols[1].text.strip()
        category = cols[2].text.strip()
        price_raw = cols[3].text.strip()
        stock = cols[4].text.strip()
        rating = cols[5].text.strip()
        
        price = clean_price(price_raw)
        
        doc = {
            "document_id": f"html-{product_id}",
            "content": f"Product: {product_name}, Category: {category}, Price: {price} VND, Stock: {stock}, Rating: {rating}",
            "source_type": "HTML",
            "author": "VinShop System",
            "timestamp": None,
            "source_metadata": {
                "product_id": product_id,
                "product_name": product_name,
                "category": category,
                "price": price,
                "stock": stock,
                "rating": rating
            }
        }
        results.append(doc)

    return results
