import os
import shutil

DOCUMENTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'documents'))

def setup_directories():
    """Ensure all category directories exist."""
    categories = [
        "Academic", "Financial", "Government", "Legal", 
        "Medical", "Bills", "Receipts", "Personal", "Other"
    ]
    
    if not os.path.exists(DOCUMENTS_DIR):
        os.makedirs(DOCUMENTS_DIR)
        
    for cat in categories:
        cat_path = os.path.join(DOCUMENTS_DIR, cat)
        if not os.path.exists(cat_path):
            os.makedirs(cat_path)

def save_document(temp_path: str, filename: str, category: str) -> str:
    """
    Moves the document from temp_path to its category folder.
    Handles filename deduplication (e.g., invoice.pdf -> invoice_1.pdf).
    """
    setup_directories()
    
    cat_dir = os.path.join(DOCUMENTS_DIR, category)
    
    # Handle deduplication
    base_name, ext = os.path.splitext(filename)
    new_filename = filename
    counter = 1
    
    dest_path = os.path.join(cat_dir, new_filename)
    while os.path.exists(dest_path):
        new_filename = f"{base_name}_{counter}{ext}"
        dest_path = os.path.join(cat_dir, new_filename)
        counter += 1
        
    # Move file
    shutil.move(temp_path, dest_path)
    
    # Return relative path for response
    return f"documents/{category}/{new_filename}"
