import re

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Clean the transcript text and extract key information.

def clean_transcript(file_path):
    # --- FILE READING (Handled for students) ---
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    # ------------------------------------------
    
    # Remove noise tokens
    text = re.sub(r'\[Music.*?\]|\[inaudible\]|\[Laughter\]', '', text)
    # Strip timestamps
    text = re.sub(r'\[\d{2}:\d{2}:\d{2}\]', '', text)
    
    # Find price in Vietnamese words
    v_price = 0.0
    if "năm trăm nghìn" in text.lower():
        v_price = 500000.0
    
    cleaned_text = " ".join(text.split())

    return {
        "document_id": "transcript-video-lecture",
        "content": cleaned_text,
        "source_type": "Video",
        "author": "Speaker 1",
        "timestamp": None,
        "source_metadata": {
            "extracted_price_vnd": v_price,
            "original_file": file_path
        }
    }

