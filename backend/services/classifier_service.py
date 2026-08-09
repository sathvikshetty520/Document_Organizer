import re

CATEGORIES = {
    "Academic": [
        "college", "university", "student", "semester", "marks", "marksheet", 
        "exam", "course", "degree", "tuition", "academic"
    ],
    "Financial": [
        "bank", "account", "transaction", "statement", "invoice", "payment", 
        "amount", "balance", "debit", "credit"
    ],
    "Government": [
        "government", "department", "certificate", "application", "aadhaar", 
        "official", "ministry", "authority"
    ],
    "Legal": [
        "agreement", "contract", "court", "legal", "clause", "party", "terms", "law"
    ],
    "Medical": [
        "hospital", "doctor", "patient", "diagnosis", "prescription", "medicine", 
        "medical", "clinic"
    ],
    "Bills": [
        "electricity", "water bill", "utility", "consumption", "meter", "billing", "due date"
    ],
    "Receipts": [
        "receipt", "paid", "purchase", "payment received", "transaction receipt"
    ],
    "Personal": [
        "personal", "address", "contact", "family"
    ]
}

def classify_document(text: str) -> tuple[str, float]:
    """
    Returns the category and confidence score based on keyword matching.
    """
    if not text:
        return "Other", 0.0
        
    text = text.lower()
    
    # Simple word tokenization
    words = re.findall(r'\b\w+\b', text)
    word_set = set(words)
    
    scores = {category: 0 for category in CATEGORIES}
    total_hits = 0
    
    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            # Handle multi-word keywords
            if " " in keyword:
                if keyword in text:
                    scores[category] += 2  # Multi-word matches get higher weight
                    total_hits += 2
            else:
                if keyword in word_set:
                    scores[category] += 1
                    total_hits += 1
                    
    if total_hits == 0:
        return "Other", 0.0
        
    # Find the max scoring category
    best_category = max(scores, key=scores.get)
    best_score = scores[best_category]
    
    # Calculate confidence as ratio of best hits to total hits
    confidence = best_score / total_hits
    
    # Threshold for "Other" if confidence is too low or hits are too few
    if best_score < 1 or confidence < 0.2:
        return "Other", round(confidence, 2)
        
    return best_category, round(confidence, 2)
