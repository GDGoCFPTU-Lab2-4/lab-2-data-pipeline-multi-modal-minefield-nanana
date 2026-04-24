import json
import time
import os


# Robust path handling
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DATA_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), 'raw_data')


# Import role-specific modules
from process_csv import process_sales_csv
from process_html import parse_html_catalog
from process_legacy_code import extract_logic_from_code
from process_pdf import extract_pdf_data
from process_transcript import clean_transcript
from quality_check import run_quality_gate
from schema import UnifiedDocument

# ==========================================
# ROLE 4: DEVOPS & INTEGRATION SPECIALIST
# ==========================================
# Task: Orchestrate the ingestion pipeline and handle errors/SLA.


def main():
    start_time = time.time()
    final_kb = []

    # --- FILE PATH SETUP (Handled for students) ---
    pdf_path = os.path.join(RAW_DATA_DIR, 'lecture_notes.pdf')
    trans_path = os.path.join(RAW_DATA_DIR, 'demo_transcript.txt')
    html_path = os.path.join(RAW_DATA_DIR, 'product_catalog.html')
    csv_path = os.path.join(RAW_DATA_DIR, 'sales_records.csv')
    code_path = os.path.join(RAW_DATA_DIR, 'legacy_pipeline.py')

    output_path = os.path.join(
        os.path.dirname(SCRIPT_DIR), 'processed_knowledge_base.json'
    )
    # ----------------------------------------------

    # 1. Process PDF
    try:
        doc_pdf = extract_pdf_data(pdf_path)
        if doc_pdf and run_quality_gate(doc_pdf):
            final_kb.append(doc_pdf)
    except Exception as e:
        print(f'Error processing PDF: {e}')

    # 2. Process Transcript
    try:
        doc_trans = clean_transcript(trans_path)
        if doc_trans and run_quality_gate(doc_trans):
            final_kb.append(doc_trans)
    except Exception as e:
        print(f'Error processing Transcript: {e}')

    # 3. Process HTML
    try:
        docs_html = parse_html_catalog(html_path)
        for doc in docs_html:
            if doc and run_quality_gate(doc):
                final_kb.append(doc)
    except Exception as e:
        print(f'Error processing HTML: {e}')

    # 4. Process CSV
    try:
        docs_csv = process_sales_csv(csv_path)
        for doc in docs_csv:
            if doc and run_quality_gate(doc):
                final_kb.append(doc)
    except Exception as e:
        print(f'Error processing CSV: {e}')

    # 5. Process Legacy Code
    try:
        doc_code = extract_logic_from_code(code_path)
        if doc_code and run_quality_gate(doc_code):
            final_kb.append(doc_code)
    except Exception as e:
        print(f'Error processing Code: {e}')

    # Save final_kb to output_path using json.dump
    # Note: Using UnifiedDocument to validate and handle datetime serialization
    validated_kb = []
    for doc in final_kb:
        try:
            # Ensure it matches schema and serialize to JSON-safe format
            validated_kb.append(UnifiedDocument(**doc).model_dump(mode='json'))
        except Exception as e:
            print(f'Validation error for {doc.get("document_id")}: {e}')

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(validated_kb, f, indent=4, ensure_ascii=False)

    end_time = time.time()
    print(f'Pipeline finished in {end_time - start_time:.2f} seconds.')
    print(f'Total valid documents stored: {len(validated_kb)}')


def test() -> None:
    '''Test func'''
if __name__ == '__main__':
    main()
    test()
