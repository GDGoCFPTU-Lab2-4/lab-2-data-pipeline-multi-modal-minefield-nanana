import pandas as pd

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Process sales records, handling type traps and duplicates.


def process_sales_csv(file_path: str) -> list:
    # --- FILE READING (Handled for students) ---
    df = pd.read_csv(file_path)
    df = df.drop_duplicates(subset=["id"])
    # ------------------------------------------

    def clean_price(val):
        if pd.isna(val):
            return 0.0
        val = str(val).strip().lower()
        if val in ['n/a', 'liên hệ', 'null']:
            return 0.0
        if 'five dollars' in val:
            return 5.0
        # Remove currency symbols and comma
        val = val.replace('$', '').replace(',', '')
        try:
            return abs(float(val))
        except ValueError:
            return 0.0

    def clean_date(val):
        try:
            # Handle ordinal suffixes like 16th, 22nd
            val_clean = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', str(val))
            return pd.to_datetime(val_clean).strftime('%Y-%m-%d')
        except:
            return None

    results = []
    import re
    from datetime import datetime

    for _, row in df.iterrows():
        price = clean_price(row['price'])
        date_str = clean_date(row['date_of_sale'])
        
        doc = {
            "document_id": f"csv-{row['id']}",
            "content": f"Product: {row['product_name']}, Category: {row['category']}, Price: {price} {row['currency']}",
            "source_type": "CSV",
            "author": str(row['seller_id']),
            "timestamp": datetime.strptime(date_str, '%Y-%m-%d') if date_str else None,
            "source_metadata": {
                "product_id": int(row['id']),
                "product_name": row['product_name'],
                "category": row['category'],
                "price": price,
                "currency": row['currency'],
                "stock_quantity": row['stock_quantity'] if pd.notna(row['stock_quantity']) else 0
            }
        }
        results.append(doc)

    return results
