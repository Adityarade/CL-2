from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, Table
from sqlalchemy.orm import relationship
from database.database import Base

paper_gene = Table('paper_gene', Base.metadata,
    Column('paper_id', Integer, ForeignKey('papers.id')),
    Column('gene_id', Integer, ForeignKey('genes.id'))
)

paper_disease = Table('paper_disease', Base.metadata,
    Column('paper_id', Integer, ForeignKey('papers.id')),
    Column('disease_id', Integer, ForeignKey('diseases.id'))
)

paper_protein = Table('paper_protein', Base.metadata,
    Column('paper_id', Integer, ForeignKey('papers.id')),
    Column('protein_id', Integer, ForeignKey('proteins.id'))
)

paper_drug = Table('paper_drug', Base.metadata,
    Column('paper_id', Integer, ForeignKey('papers.id')),
    Column('drug_id', Integer, ForeignKey('drugs.id'))
)

gene_disease = Table('gene_disease', Base.metadata,
    Column('gene_id', Integer, ForeignKey('genes.id')),
    Column('disease_id', Integer, ForeignKey('diseases.id'))
)

class Paper(Base):
    __tablename__ = "papers"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    abstract = Column(Text)
    authors = Column(String)
    year = Column(Integer)
    journal = Column(String)
    keywords = Column(String)
    
    genes = relationship("Gene", secondary=paper_gene, back_populates="papers")
    diseases = relationship("Disease", secondary=paper_disease, back_populates="papers")
    proteins = relationship("Protein", secondary=paper_protein, back_populates="papers")
    drugs = relationship("Drug", secondary=paper_drug, back_populates="papers")

class Gene(Base):
    __tablename__ = "genes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    functions = Column(Text)
    
    papers = relationship("Paper", secondary=paper_gene, back_populates="genes")
    diseases = relationship("Disease", secondary=gene_disease, back_populates="diseases")

class Disease(Base):
    __tablename__ = "diseases"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    
    papers = relationship("Paper", secondary=paper_disease, back_populates="diseases")
    genes = relationship("Gene", secondary=gene_disease, back_populates="diseases")

class Protein(Base):
    __tablename__ = "proteins"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    function = Column(Text)
    
    papers = relationship("Paper", secondary=paper_protein, back_populates="proteins")

class Drug(Base):
    __tablename__ = "drugs"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    
    papers = relationship("Paper", secondary=paper_drug, back_populates="drugs")

class SearchHistory(Base):
    __tablename__ = "search_history"
    id = Column(Integer, primary_key=True, index=True)
    query = Column(String, index=True)
    timestamp = Column(String)
