import os
import sys

# Ensure backend directory is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

from services.ai_classifier_service import classify_document_ai

samples = {
    "Electricity bill": "utility consumption meter billing due date 200 kWh",
    "Bank statement": "account transaction statement invoice payment amount balance debit credit",
    "College marksheet": "college university student semester marks marksheet exam course degree tuition academic",
    "Government certificate": "government department certificate application aadhaar official ministry authority",
    "Medical prescription": "hospital doctor patient diagnosis prescription medicine medical clinic",
    "Legal agreement": "agreement contract court legal clause party terms law",
    "Random unrelated document": "The quick brown fox jumps over the lazy dog. Recipes for cooking pasta."
}

def main():
    print("Testing AI Classification Model...")
    for name, text in samples.items():
        try:
            cat, conf = classify_document_ai(text)
            print(f"Sample: {name}")
            print(f"  Predicted: {cat} ({conf})")
            if conf < 0.70:
                print("  -> Would fallback to keyword classifier.")
        except Exception as e:
            print(f"Failed on {name}: {e}")

if __name__ == "__main__":
    main()
