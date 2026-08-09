from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import tempfile
import os
import shutil
import uvicorn

from services.pdf_service import extract_text_from_pdf
from services.classifier_service import classify_document
from services.storage_service import save_document

app = FastAPI(title="AI Document Organizer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/documents/upload")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
        
    # 1. Save temporarily
    try:
        fd, temp_path = tempfile.mkstemp(suffix=".pdf")
        with os.fdopen(fd, 'wb') as f:
            shutil.copyfileobj(file.file, f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save temporary file: {e}")

    try:
        # 2 & 3. Extract text (uses PyMuPDF + PaddleOCR)
        text = extract_text_from_pdf(temp_path)
        
        # 4. Classify document
        category, confidence = classify_document(text)
        
        # 5. Move to correct folder
        saved_path = save_document(temp_path, file.filename, category)
        
        return JSONResponse({
            "success": True,
            "filename": file.filename,
            "category": category,
            "confidence": confidence,
            "path": saved_path
        })
        
    except Exception as e:
        # Cleanup in case of error
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise HTTPException(status_code=500, detail=f"Failed to process document: {e}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
