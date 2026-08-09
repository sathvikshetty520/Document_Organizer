# Smart Document Organizer

A local document organization system. This application allows users to upload PDF documents, automatically extracts text (using AI-based OCR when necessary), and sorts them into appropriate folders (e.g., Academic, Bills, Financial, etc.) based on keyword heuristics.

## Features
- **Local PDF Processing**: Uses `PyMuPDF` for fast text extraction from standard PDFs.
- **OCR Fallback**: Uses CPU-optimized `PaddleOCR` to extract text from scanned documents or images within PDFs.
- **AI & Heuristic Categorization**: Uses a local AI model (TF-IDF + Cosine Similarity) via `scikit-learn` for intelligent document classification, with a lightweight keyword scoring algorithm as a fallback.
- **Auto-Organization**: Automatically creates missing folders and securely moves/renames documents to prevent data loss or overwriting.
- **Modern UI**: A beautiful, premium dark-mode React frontend with glassmorphism aesthetics.
- **FastAPI Backend**: A highly concurrent, well-structured Python backend.

## Project Structure
```text
project_root/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── requirements.txt        # Python dependencies
│   ├── services/
│   │   ├── ai_classifier_service.py # AI categorization logic
│   │   ├── classifier_service.py # Fallback categorization logic
│   │   ├── ocr_service.py        # PaddleOCR integration
│   │   ├── pdf_service.py        # PyMuPDF integration
│   │   └── storage_service.py    # File system management
│   └── venv/                   # Python virtual environment
├── documents/                  # Automatically generated storage folders
└── frontend/
    ├── src/
    │   ├── App.jsx             # Main React application
    │   ├── App.css             # Component styles
    │   └── index.css           # Global theme & styles
    └── package.json            # Node dependencies
```

## Setup Instructions

### 1. Backend API
Open a command prompt (`cmd`) and run the following to start the FastAPI server:

```cmd
cd backend
.\venv\Scripts\python.exe main.py
```
*(The API will be available at `http://localhost:8000`, and interactive docs at `http://localhost:8000/docs`)*

### 2. Frontend UI
Open a separate command prompt (`cmd`) and run the following to start the React development server:

```cmd
cd frontend
npm run dev
```
*(The web interface will be available at `http://localhost:5173`)*

## Future Roadmap
- Add PostgreSQL for tracking document metadata and history.
- Implement vector search / RAG for conversational queries against your documents.
- Add user authentication.
- Dockerize the entire application for easier deployment.
