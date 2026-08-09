import json
from sklearn.feature_extraction.text import TfidfVectorizer

v = TfidfVectorizer(stop_words='english', ngram_range=(1,2), max_features=10000)
with open('../documents/index.json', encoding='utf-8') as f:
    data = json.load(f)

texts = [f"{d.get('filename','')} {d.get('category','')} {d.get('text','')}" for d in data]
v.fit(texts)
query = "AEC_FINAL_REPORT"
print("Feature sum for query:", v.transform([query]).toarray().sum())
print("Is 'aec_final_report' in vocab?", 'aec_final_report' in v.vocabulary_)
print("Vocab size:", len(v.vocabulary_))
