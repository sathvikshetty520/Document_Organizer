# pyrefly: ignore [missing-import]
from paddleocr import PaddleOCR
import logging

# Set logging level to avoid PaddleOCR spam
logging.getLogger("ppocr").setLevel(logging.ERROR)

# Initialize OCR model once
# use_angle_cls=True for text orientation, lang='en' for English
# Disable GPU usage explicitly as requested
ocr = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=False)

def process_scanned_page(image_path: str) -> str:
    """
    Extract text from an image using PaddleOCR.
    """
    try:
        result = ocr.ocr(image_path, cls=True)
        if not result or not result[0]:
            return ""
            
        text_lines = []
        for line in result[0]:
            # line is [[box points], (text, confidence)]
            text = line[1][0]
            text_lines.append(text)
            
        return "\n".join(text_lines)
    except Exception as e:
        print(f"OCR Error on {image_path}: {e}")
        return ""
