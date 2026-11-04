from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from datetime import datetime

from database.database import engine, Base, get_db
from models import models
from schemas import schemas
from ir_engine.engine import ir_engine_instance
import nltk

Base.metadata.create_all(bind=engine)

app = FastAPI(title="BioIntel API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    db = next(get_db())
    papers = db.query(models.Paper).all()
    if papers:
        print("Indexing documents for search...")
        ir_engine_instance.index_documents(papers)
        print(f"Indexed {len(papers)} documents.")

@app.get("/api/health")
def health_check():
    return {"status": "healthy"}

@app.get("/api/stats")
def get_stats(db: Session = Depends(get_db)):
    return {
        "papers": db.query(models.Paper).count(),
        "genes": db.query(models.Gene).count(),
        "diseases": db.query(models.Disease).count(),
        "proteins": db.query(models.Protein).count(),
        "drugs": db.query(models.Drug).count(),
    }

@app.get("/api/search", response_model=List[schemas.SearchResult])
def search_papers(
    q: str, 
    entity_type: str = Query("All"), 
    ranking: str = Query("Hybrid"),
    db: Session = Depends(get_db)
):
    # Save search history
    history = models.SearchHistory(query=q, timestamp=datetime.now().isoformat())
    db.add(history)
    db.commit()

    weights = (0.35, 0.35, 0.30) # Hybrid
    if ranking == "TF-IDF":
        weights = (1.0, 0.0, 0.0)
    elif ranking == "BM25":
        weights = (0.0, 1.0, 0.0)
    elif ranking == "Semantic":
        weights = (0.0, 0.0, 1.0)
        
    results = ir_engine_instance.search(q, weights=weights)
    
    formatted_results = []
    for res in results:
        paper = db.query(models.Paper).filter(models.Paper.id == res["paper_id"]).first()
        if paper:
            # Filter by entity type if needed
            if entity_type != "All":
                if entity_type == "Gene" and not paper.genes: continue
                if entity_type == "Disease" and not paper.diseases: continue
                if entity_type == "Protein" and not paper.proteins: continue
                if entity_type == "Drug" and not paper.drugs: continue
                
            entities = []
            for g in paper.genes: entities.append(g.name)
            for d in paper.diseases: entities.append(d.name)
            for p in paper.proteins: entities.append(p.name)
            for dr in paper.drugs: entities.append(dr.name)
            
            # Find matched entities
            matched_entities = [e for e in entities if e.lower() in q.lower()]
            
            # Highlight abstract (simple implementation)
            formatted_results.append({
                "paper": paper,
                "score": res["score"],
                "tf_idf_score": res["tf_idf_score"],
                "bm25_score": res["bm25_score"],
                "semantic_score": res["semantic_score"],
                "matched_terms": res["matched_terms"],
                "matched_entities": matched_entities
            })
            
    return formatted_results

@app.get("/api/papers", response_model=List[schemas.Paper])
def get_papers(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return db.query(models.Paper).offset(skip).limit(limit).all()

@app.get("/api/papers/{id}", response_model=schemas.Paper)
def get_paper(id: int, db: Session = Depends(get_db)):
    paper = db.query(models.Paper).filter(models.Paper.id == id).first()
    if not paper: raise HTTPException(status_code=404, detail="Paper not found")
    return paper

@app.get("/api/genes", response_model=List[schemas.Gene])
def get_genes(db: Session = Depends(get_db)):
    return db.query(models.Gene).all()

@app.get("/api/genes/{id}", response_model=schemas.Gene)
def get_gene(id: int, db: Session = Depends(get_db)):
    gene = db.query(models.Gene).filter(models.Gene.id == id).first()
    if not gene: raise HTTPException(status_code=404, detail="Gene not found")
    return gene
    
@app.get("/api/diseases", response_model=List[schemas.Disease])
def get_diseases(db: Session = Depends(get_db)):
    return db.query(models.Disease).all()

@app.get("/api/diseases/{id}", response_model=schemas.Disease)
def get_disease(id: int, db: Session = Depends(get_db)):
    disease = db.query(models.Disease).filter(models.Disease.id == id).first()
    if not disease: raise HTTPException(status_code=404, detail="Disease not found")
    return disease

@app.get("/api/proteins", response_model=List[schemas.Protein])
def get_proteins(db: Session = Depends(get_db)):
    return db.query(models.Protein).all()

@app.get("/api/proteins/{id}", response_model=schemas.Protein)
def get_protein(id: int, db: Session = Depends(get_db)):
    protein = db.query(models.Protein).filter(models.Protein.id == id).first()
    if not protein: raise HTTPException(status_code=404, detail="Protein not found")
    return protein

@app.get("/api/search-history", response_model=List[schemas.SearchHistory])
def get_search_history(limit: int = 10, db: Session = Depends(get_db)):
    return db.query(models.SearchHistory).order_by(models.SearchHistory.id.desc()).limit(limit).all()

@app.get("/api/analytics")
def get_analytics(db: Session = Depends(get_db)):
    # Very basic analytics mapping
    papers_by_year = {}
    papers = db.query(models.Paper).all()
    for p in papers:
        if p.year not in papers_by_year:
            papers_by_year[p.year] = 0
        papers_by_year[p.year] += 1
        
    return {
        "papers_by_year": [{"year": k, "count": v} for k, v in sorted(papers_by_year.items())],
        "entity_distribution": [
            {"name": "Genes", "value": db.query(models.Gene).count()},
            {"name": "Diseases", "value": db.query(models.Disease).count()},
            {"name": "Proteins", "value": db.query(models.Protein).count()},
            {"name": "Drugs", "value": db.query(models.Drug).count()},
        ]
    }
