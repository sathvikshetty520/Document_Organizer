import os
import json
import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

logger = logging.getLogger(__name__)

DOCUMENTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'documents'))
INDEX_FILE = os.path.join(DOCUMENTS_DIR, 'index.json')

_index_data = []
_vectorizer = None
_tfidf_matrix = None

def load_index():
    global _index_data, _vectorizer, _tfidf_matrix
    if os.path.exists(INDEX_FILE):
        try:
            with open(INDEX_FILE, 'r', encoding='utf-8') as f:
                _index_data = json.load(f)
        except Exception as e:
            logger.error(f"Failed to load index.json: {e}")
            _index_data = []
    else:
        _index_data = []

    _rebuild_tfidf()

def _rebuild_tfidf():
    global _vectorizer, _tfidf_matrix, _index_data
    if not _index_data:
        _vectorizer = None
        _tfidf_matrix = None
        return

    # Include filename and category in the searchable text
    texts = [f"{doc.get('filename', '')} {doc.get('category', '')} {doc.get('text', '')}" for doc in _index_data]
    
    _vectorizer = TfidfVectorizer(
        stop_words='english',
        ngram_range=(1, 2),
        max_features=10000
    )
    
    try:
        _tfidf_matrix = _vectorizer.fit_transform(texts)
    except Exception as e:
        logger.warning(f"Failed to build TF-IDF matrix (might be empty texts): {e}")
        _vectorizer = None
        _tfidf_matrix = None

def add_to_index(filename: str, category: str, path: str, text: str):
    global _index_data
    
    # Don't add duplicates based on path
    for doc in _index_data:
        if doc.get("path") == path:
            doc["text"] = text
            doc["category"] = category
            _save_and_rebuild()
            return
            
    _index_data.append({
        "filename": filename,
        "category": category,
        "path": path,
        "text": text
    })
    
    _save_and_rebuild()

def _save_and_rebuild():
    try:
        if not os.path.exists(DOCUMENTS_DIR):
            os.makedirs(DOCUMENTS_DIR)
        with open(INDEX_FILE, 'w', encoding='utf-8') as f:
            json.dump(_index_data, f, indent=2)
    except Exception as e:
        logger.error(f"Failed to save index.json: {e}")
        
    _rebuild_tfidf()

def search(query: str, category: str = None, min_score: float = 0.10, limit: int = 10):
    if not query or not query.strip():
        return []
        
    if not _index_data:
        return []

    has_tfidf = _vectorizer is not None and _tfidf_matrix is not None
    if has_tfidf:
        query_vec = _vectorizer.transform([query])
        similarities = cosine_similarity(query_vec, _tfidf_matrix)[0]
    else:
        similarities = np.zeros(len(_index_data))
    
    results = []
    query_lower = query.lower()
    
    for idx, doc in enumerate(_index_data):
        score = float(similarities[idx]) if has_tfidf else 0.0
        
        # Boost score if query is in filename or category
        if query_lower in doc.get("filename", "").lower():
            score = max(score, 1.0)
        elif query_lower in doc.get("category", "").lower():
            score = max(score, 0.5)
            
        if score >= min_score:
            if category and doc.get("category") != category:
                continue
            
            # Map score so 1.0 is max
            scaled_score = round(min(score, 1.0), 2)
            
            results.append({
                "filename": doc["filename"],
                "category": doc["category"],
                "path": doc["path"],
                "score": scaled_score
            })
            
    # Sort by highest score first
    results.sort(key=lambda x: x["score"], reverse=True)
    
    return results[:limit]

# Load index on module import
load_index()
