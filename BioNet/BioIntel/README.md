# BioIntel - Intelligent Biomedical Information Retrieval and Knowledge Discovery Platform

BioIntel is an intelligent biomedical information search engine and knowledge discovery platform. It retrieves and ranks relevant biomedical research documents and displays related biological entities such as genes, diseases, proteins, and drugs.

## Features
- **Biomedical Search Engine**: Advanced search with TF-IDF, BM25, and Semantic Search algorithms.
- **Hybrid Ranking**: Configurable combination of relevance scores.
- **Entity Exploration**: Browse through associated genes, diseases, proteins, and drugs.
- **Analytics Dashboard**: Visualizations of document and entity distributions.
- **"Why this result?"**: Explainable AI feature that breaks down the final relevance score by matching terms and algorithm weights.
- **Search History**: Track and replay recent searches.

## Technology Stack
- **Frontend**: React.js, Vite, Tailwind CSS, Lucide React, Recharts.
- **Backend**: Python, FastAPI, SQLAlchemy, Pydantic.
- **Database**: SQLite (Development) / PostgreSQL (Production ready).
- **IR / NLP**: scikit-learn, rank-bm25, sentence-transformers, NLTK.

## Architecture
```
                 USER
                   |
                   ↓
            React Frontend
                   |
                   ↓
             REST API
                   |
                   ↓
             FastAPI Backend
                   |
        ┌──────────┼───────────┐
        ↓          ↓           ↓
      NLP       IR Engine   Bio Engine
        |          |           |
        ↓          ↓           ↓
     Entity     TF-IDF       Entity
   Extraction   BM25         Mapping
                 |
                 ↓
          Semantic Search
                 |
                 ↓
             Database
                 |
                 ↓
       Biomedical Dataset
```

## Setup Instructions

### 1. Backend Setup
1. Open terminal and navigate to `backend/`.
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # Windows
   ```
3. Install dependencies:
   ```bash
   pip install fastapi uvicorn sqlalchemy pydantic scikit-learn rank-bm25 sentence-transformers pandas nltk
   ```
4. Seed the database with sample biomedical data:
   ```bash
   python ../scripts/seed_database.py
   ```
5. Run the backend server:
   ```bash
   uvicorn main:app --reload
   ```

### 2. Frontend Setup
1. Open a new terminal and navigate to `frontend/`.
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```

### 3. Demo Data
The application comes with a `seed_database.py` script that automatically generates a sample dataset of 50+ papers, 30+ genes, 20+ diseases, 20+ proteins, and 15+ drugs with complex interrelationships mimicking real biomedical abstracts.
