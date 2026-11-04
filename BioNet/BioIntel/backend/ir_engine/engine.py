import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from rank_bm25 import BM25Okapi
import numpy as np
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sentence_transformers import SentenceTransformer

try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('punkt_tab', quiet=True)
except:
    pass

class IREngine:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.bm25 = None
        self.tfidf_matrix = None
        self.documents = []
        self.doc_ids = []
        try:
            self.semantic_model = SentenceTransformer('all-MiniLM-L6-v2')
        except:
            self.semantic_model = None
        self.semantic_embeddings = None
        try:
            self.stop_words = set(stopwords.words('english'))
        except:
            self.stop_words = set(['the', 'is', 'in', 'and', 'to', 'of', 'a', 'for', 'on', 'with', 'as', 'by', 'an'])

    def preprocess(self, text):
        if not text:
            return ""
        text = text.lower()
        text = text.translate(str.maketrans('', '', string.punctuation))
        try:
            tokens = word_tokenize(text)
        except:
            tokens = text.split()
        tokens = [word for word in tokens if word not in self.stop_words]
        return " ".join(tokens)

    def index_documents(self, db_papers):
        self.documents = []
        self.doc_ids = []
        tokenized_docs = []
        
        for paper in db_papers:
            text = f"{paper.title} {paper.abstract} {paper.keywords}"
            processed_text = self.preprocess(text)
            self.documents.append(processed_text)
            self.doc_ids.append(paper.id)
            tokenized_docs.append(processed_text.split())
            
        if self.documents:
            self.tfidf_matrix = self.vectorizer.fit_transform(self.documents)
            self.bm25 = BM25Okapi(tokenized_docs)
            if self.semantic_model:
                self.semantic_embeddings = self.semantic_model.encode(self.documents)

    def search(self, query, top_k=10, weights=(0.35, 0.35, 0.30)):
        if not self.documents:
            return []
            
        processed_query = self.preprocess(query)
        query_tokens = processed_query.split()
        if not query_tokens:
            return []
        
        query_tfidf = self.vectorizer.transform([processed_query])
        tfidf_scores = cosine_similarity(query_tfidf, self.tfidf_matrix).flatten()
        
        bm25_scores = self.bm25.get_scores(query_tokens)
        
        if np.max(bm25_scores) > 0:
            bm25_scores = bm25_scores / np.max(bm25_scores)
            
        semantic_scores = np.zeros(len(self.documents))
        if self.semantic_model and self.semantic_embeddings is not None:
            query_embedding = self.semantic_model.encode([processed_query])
            semantic_scores = cosine_similarity(query_embedding, self.semantic_embeddings).flatten()
            
        final_scores = (weights[0] * tfidf_scores) + (weights[1] * bm25_scores) + (weights[2] * semantic_scores)
        
        top_indices = final_scores.argsort()[-top_k:][::-1]
        
        results = []
        for idx in top_indices:
            if final_scores[idx] > 0.05:
                results.append({
                    "paper_id": self.doc_ids[idx],
                    "score": float(final_scores[idx]),
                    "tf_idf_score": float(tfidf_scores[idx]),
                    "bm25_score": float(bm25_scores[idx]),
                    "semantic_score": float(semantic_scores[idx]),
                    "matched_terms": list(set(query_tokens).intersection(set(self.documents[idx].split())))
                })
        return results

ir_engine_instance = IREngine()
