# pyrefly: ignore [missing-import]
import fitz  # PyMuPDF
from .ocr_service import process_scanned_page
import os

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extracts text from a PDF. If a page contains no text, uses PaddleOCR.
    """
    text_content = []
    
    try:
        doc = fitz.open(pdf_path)
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            page_text = page.get_text("text").strip()
            
            if page_text:
                text_content.append(page_text)
            else:
                # If no text, treat as scanned and use OCR
                pix = page.get_pixmap(dpi=150)
                temp_img_path = f"{pdf_path}_page_{page_num}.png"
                pix.save(temp_img_path)
                
                ocr_text = process_scanned_page(temp_img_path)
                if ocr_text:
                    text_content.append(ocr_text)
                    
                if os.path.exists(temp_img_path):
                    os.remove(temp_img_path)
                    
        return "\n".join(text_content)
    except Exception as e:
        print(f"Error processing PDF: {e}")
        return ""
