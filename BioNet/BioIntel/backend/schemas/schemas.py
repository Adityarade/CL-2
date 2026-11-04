from pydantic import BaseModel
from typing import List, Optional

class GeneBase(BaseModel):
    name: str
    description: str
    functions: str

class GeneCreate(GeneBase):
    pass

class Gene(GeneBase):
    id: int
    class Config:
        from_attributes = True

class DiseaseBase(BaseModel):
    name: str
    description: str

class DiseaseCreate(DiseaseBase):
    pass

class Disease(DiseaseBase):
    id: int
    class Config:
        from_attributes = True

class ProteinBase(BaseModel):
    name: str
    description: str
    function: str

class ProteinCreate(ProteinBase):
    pass

class Protein(ProteinBase):
    id: int
    class Config:
        from_attributes = True

class DrugBase(BaseModel):
    name: str
    description: str

class DrugCreate(DrugBase):
    pass

class Drug(DrugBase):
    id: int
    class Config:
        from_attributes = True

class PaperBase(BaseModel):
    title: str
    abstract: str
    authors: str
    year: int
    journal: str
    keywords: str

class PaperCreate(PaperBase):
    pass

class Paper(PaperBase):
    id: int
    genes: List[Gene] = []
    diseases: List[Disease] = []
    proteins: List[Protein] = []
    drugs: List[Drug] = []
    class Config:
        from_attributes = True

class SearchHistoryBase(BaseModel):
    query: str
    timestamp: str

class SearchHistoryCreate(SearchHistoryBase):
    pass

class SearchHistory(SearchHistoryBase):
    id: int
    class Config:
        from_attributes = True

class SearchResult(BaseModel):
    paper: Paper
    score: float
    tf_idf_score: float
    bm25_score: float
    semantic_score: float
    matched_terms: List[str]
    matched_entities: List[str]
