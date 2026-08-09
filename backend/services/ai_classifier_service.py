"""
AI Classifier Service
---------------------
Uses TF-IDF vectorization + cosine similarity to classify documents against
rich reference descriptions for each category.

No PyTorch / CUDA required — works on any machine with scikit-learn.
"""

import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Reference corpus
# Each category has a rich, detailed description paragraph.
# The more descriptive it is, the better TF-IDF cosine similarity works.
# ---------------------------------------------------------------------------
CATEGORY_DESCRIPTIONS = {
    "Academic": (
        "university college school student marksheet transcript grades semester "
        "examination results degree diploma course subjects passed failed CGPA GPA "
        "academic year enrollment tuition fee scholarship certificate of completion "
        "board of education admit card hall ticket roll number"
    ),
    "Financial": (
        "bank statement account number balance debit credit transaction deposit "
        "withdrawal savings current account IFSC interest rate loan EMI mutual fund "
        "investment portfolio dividend statement of account passbook cheque NEFT RTGS "
        "UPI net banking monthly statement financial report"
    ),
    "Government": (
        "government official certificate ministry department authority aadhaar PAN "
        "passport visa driving license voter ID residence certificate domicile caste "
        "income certificate birth certificate death certificate municipality corporation "
        "gazette notification affidavit notary public administration"
    ),
    "Legal": (
        "agreement contract legal clause terms conditions party witness signature "
        "court order judgement deed property sale purchase rent lease notarized "
        "affidavit power of attorney arbitration dispute settlement law advocate "
        "litigation memorandum of understanding MOU compliance obligation"
    ),
    "Medical": (
        "hospital clinic patient doctor physician diagnosis prescription medicine "
        "tablet capsule dosage treatment therapy surgery report blood test lab "
        "pathology radiology X-ray MRI scan health insurance discharge summary "
        "outpatient inpatient OPD IPD consultation medical certificate"
    ),
    "Bills": (
        "electricity bill water bill gas bill telephone bill internet bill utility "
        "consumption units meter reading due date payment amount outstanding balance "
        "service charge connection number billing cycle account holder bill number "
        "previous reading current reading total payable"
    ),
    "Receipts": (
        "receipt paid payment received invoice purchase order sale tax GST CGST SGST "
        "total amount item quantity price subtotal discount cash card UPI transaction ID "
        "shop store vendor customer bill of sale acknowledgement receipt number date"
    ),
    "Personal": (
        "personal letter address contact family friend relationship name date of birth "
        "identity proof self-declaration personal statement cover letter resume CV "
        "biodata personal information photograph signature"
    ),
    "Other": (
        "miscellaneous general document unclassified unknown content mixed various"
    ),
}

# ---------------------------------------------------------------------------
# Build the TF-IDF model once at module load (fast — no network, no GPU)
# ---------------------------------------------------------------------------
_CATEGORIES = list(CATEGORY_DESCRIPTIONS.keys())
_REFERENCE_TEXTS = [CATEGORY_DESCRIPTIONS[c] for c in _CATEGORIES]

_vectorizer = TfidfVectorizer(
    ngram_range=(1, 2),   # unigrams + bigrams for better coverage
    sublinear_tf=True,    # dampen effect of high-frequency terms
    max_features=8000,
)
_reference_matrix = _vectorizer.fit_transform(_REFERENCE_TEXTS)

logger.info("AI classifier (TF-IDF) ready — %d categories loaded.", len(_CATEGORIES))


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
def classify_document_ai(text: str) -> tuple:
    """
    Classify *text* using TF-IDF cosine-similarity against reference descriptions.

    Returns
    -------
    (category: str, confidence: float)
        category   – folder-name category (e.g. "Financial")
        confidence – float in [0, 1]
    """
    if not text or not text.strip():
        return "Other", 0.0

    # Use first 3000 characters — enough context without slowing things down
    snippet = text[:3000].strip()

    doc_vec = _vectorizer.transform([snippet])
    similarities = cosine_similarity(doc_vec, _reference_matrix)[0]

    best_idx: int = int(np.argmax(similarities))
    best_score: float = round(float(similarities[best_idx]), 2)
    category: str = _CATEGORIES[best_idx]

    # Normalise: cosine similarity scores for TF-IDF are typically 0.05 – 0.60.
    # We scale them to the [0, 1] range so they feel comparable to the
    # keyword-based classifier's confidence values.
    # A raw score >= 0.08 maps to >= 0.70 after scaling.
    scaled_score = min(round(best_score / 0.30, 2), 1.0)

    logger.info(
        "AI (TF-IDF) classification → '%s'  raw=%.3f  scaled=%.2f",
        category, best_score, scaled_score,
    )
    return category, scaled_score
