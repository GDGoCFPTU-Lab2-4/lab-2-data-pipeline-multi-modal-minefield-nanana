import json
import os

from dotenv import load_dotenv
from google import genai

load_dotenv()


prompt = """
Analyze this document and extract a summary and the author. 
Output exactly as a JSON object matching this exact format:
{
    "document_id": "pdf-doc-001",
    "content": "Summary: [Insert your 3-sentence summary here]",
    "source_type": "PDF",
    "author": "[Insert author name here]",
    "timestamp": null,
    "source_metadata": {"original_file": "lecture_notes.pdf"}
}
"""


def extract_pdf_data(file_path: str) -> list[dict[str, object]]:
    if not os.path.exists(file_path):
        print(f'Error: File not found at {file_path}')
        return None

    # Thay đổi model name để tránh lỗi 404 trên các phiên bản API cũ
    client = genai.Client()
    file = client.files.upload(file=file_path)

    print(f'Uploading {file_path} to Gemini...')
    try:
        response = client.models.generate_content(
            model='gemini-3.1-flash-lite-preview',
            contents=[
                file,
                '\n\n',
                prompt,
            ],
        )
    except Exception as e:
        print(f'Failed to upload file to Gemini: {e}')
        return None

    print('Generating content from PDF using Gemini...')
    content_text = response.text or ''

    # Simple cleanup if the response is wrapped in markdown json block
    if content_text.startswith('```json'):
        content_text = content_text[7:]
    if content_text.endswith('```'):
        content_text = content_text[:-3]
    if content_text.startswith('```'):
        content_text = content_text[3:]

    extracted_data = json.loads(content_text.strip())
    return extracted_data
