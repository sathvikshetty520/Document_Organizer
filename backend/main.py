from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import tempfile
import os
import shutil
import uvicorn
import logging

from services.pdf_service import extract_text_from_pdf
from services.classifier_service import classify_document
from services.ai_classifier_service import classify_document_ai
from services.storage_service import save_document
from services.search_service import add_to_index, search

app = FastAPI(title="AI Document Organizer API")

AI_CONFIDENCE_THRESHOLD = 0.70

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
        classification_method = "keyword_fallback"
        category = "Other"
        confidence = 0.0
        
        try:
            # Try AI first
            ai_category, ai_confidence = classify_document_ai(text)
            if ai_confidence >= AI_CONFIDENCE_THRESHOLD:
                category = ai_category
                confidence = ai_confidence
                classification_method = "ai"
            else:
                # Fallback to keyword if confidence is low
                category, confidence = classify_document(text)
        except Exception as e:
            logging.warning(f"AI classifier failed, falling back to keyword classifier. Error: {e}")
            category, confidence = classify_document(text)
        
        # 5. Move to correct folder
        saved_path = save_document(temp_path, file.filename, category)
        
        # 6. Add to search index
        add_to_index(file.filename, category, saved_path, text)
        
        return JSONResponse({
            "success": True,
            "filename": file.filename,
            "category": category,
            "confidence": confidence,
            "classification_method": classification_method,
            "path": saved_path
        })
        
    except Exception as e:
        # Cleanup in case of error
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise HTTPException(status_code=500, detail=f"Failed to process document: {e}")

@app.get("/api/documents/search")
async def search_documents(q: str = "", category: str = None):
    if not q or not q.strip():
        return JSONResponse({"success": True, "query": q, "results": []})
        
    try:
        results = search(query=q, category=category)
        return JSONResponse({
            "success": True,
            "query": q,
            "results": results
        })
    except Exception as e:
        logging.error(f"Search error: {e}")
        raise HTTPException(status_code=500, detail="Search failed")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
