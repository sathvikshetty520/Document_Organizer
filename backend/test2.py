import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

v = TfidfVectorizer(stop_words='english', ngram_range=(1,2), max_features=10000)
with open('../documents/index.json', encoding='utf-8') as f:
    data = json.load(f)

texts = [f"{d.get('filename','')} {d.get('category','')} {d.get('text','')}" for d in data]
tfidf_matrix = v.fit_transform(texts)
query = "AEC_FINAL_REPORT"
query_vec = v.transform([query])
similarities = cosine_similarity(query_vec, tfidf_matrix)[0]

print("Similarities:", similarities)
