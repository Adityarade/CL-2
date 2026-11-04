import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from database.database import SessionLocal, engine
from models import models
import random

models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)

db = SessionLocal()

def seed():
    genes = [
        {"name": "BRCA1", "description": "Breast cancer type 1 susceptibility protein.", "functions": "DNA repair, tumor suppression"},
        {"name": "BRCA2", "description": "Breast cancer type 2 susceptibility protein.", "functions": "DNA repair, homologous recombination"},
        {"name": "TP53", "description": "Tumor protein p53, the guardian of the genome.", "functions": "Cell cycle regulation, apoptosis"},
        {"name": "EGFR", "description": "Epidermal growth factor receptor.", "functions": "Cell growth and differentiation signaling"},
        {"name": "APOE", "description": "Apolipoprotein E.", "functions": "Lipid metabolism and transport"},
        {"name": "APP", "description": "Amyloid precursor protein.", "functions": "Synapse formation, neural plasticity"},
        {"name": "INS", "description": "Insulin gene.", "functions": "Carbohydrate metabolism regulation"},
        {"name": "SLC2A4", "description": "Solute carrier family 2 member 4 (GLUT4).", "functions": "Glucose transport in muscle and fat"},
        {"name": "KRAS", "description": "Kirsten rat sarcoma virus.", "functions": "Intracellular signaling, cell proliferation"},
        {"name": "PTEN", "description": "Phosphatase and tensin homolog.", "functions": "Tumor suppressor, lipid phosphatase"},
    ]
    for i in range(11, 35):
        genes.append({"name": f"GENE{i}", "description": f"Description for GENE{i}", "functions": "Unknown function"})
    
    db_genes = [models.Gene(**g) for g in genes]
    db.add_all(db_genes)
    db.commit()

    diseases = [
        {"name": "Breast Cancer", "description": "Cancer that forms in cells of the breasts."},
        {"name": "Ovarian Cancer", "description": "Cancer that begins in the female organs that produce eggs."},
        {"name": "Alzheimer's Disease", "description": "A progressive disease that destroys memory and other important mental functions."},
        {"name": "Type 2 Diabetes", "description": "A chronic condition that affects the way the body processes blood sugar."},
        {"name": "Lung Cancer", "description": "A cancer that begins in the lungs and most often occurs in people who smoke."},
        {"name": "Colorectal Cancer", "description": "A cancer of the colon or rectum."},
        {"name": "Melanoma", "description": "The most serious type of skin cancer."},
        {"name": "Parkinson's Disease", "description": "A disorder of the central nervous system that affects movement, often including tremors."},
        {"name": "Leukemia", "description": "A cancer of blood-forming tissues, hindering the body's ability to fight infection."},
        {"name": "Glioblastoma", "description": "An aggressive type of cancer that can occur in the brain or spinal cord."},
    ]
    for i in range(11, 25):
        diseases.append({"name": f"Disease{i}", "description": f"Description for Disease{i}"})
        
    db_diseases = [models.Disease(**d) for d in diseases]
    db.add_all(db_diseases)
    db.commit()

    proteins = [
        {"name": "Insulin", "description": "Hormone that regulates blood sugar.", "function": "Lowers blood glucose"},
        {"name": "p53", "description": "Protein that regulates the cell cycle.", "function": "Tumor suppression"},
        {"name": "Amyloid beta", "description": "Peptide that forms plaques in Alzheimer's.", "function": "Unknown exactly, possibly antimicrobial"},
        {"name": "Tau", "description": "Protein that stabilizes microtubules.", "function": "Axonal transport"},
        {"name": "Her2", "description": "Receptor tyrosine-protein kinase erbB-2.", "function": "Cell signaling in growth"},
        {"name": "Glucagon", "description": "Hormone that raises blood sugar.", "function": "Glycogenolysis stimulation"},
        {"name": "Hemoglobin", "description": "Iron-containing transport protein.", "function": "Oxygen transport"},
        {"name": "Albumin", "description": "Main protein of human blood plasma.", "function": "Maintains intravascular oncotic pressure"},
        {"name": "Actin", "description": "Globular multi-functional protein.", "function": "Muscle contraction, cell motility"},
        {"name": "Myosin", "description": "Motor protein.", "function": "Muscle contraction"},
    ]
    for i in range(11, 25):
        proteins.append({"name": f"Protein{i}", "description": f"Description for Protein{i}", "function": "Cell function"})
        
    db_proteins = [models.Protein(**p) for p in proteins]
    db.add_all(db_proteins)
    db.commit()
    
    drugs = [
        {"name": "Metformin", "description": "First-line medication for type 2 diabetes."},
        {"name": "Tamoxifen", "description": "Medication used to prevent and treat breast cancer."},
        {"name": "Trastuzumab", "description": "Monoclonal antibody used to treat breast and stomach cancer."},
        {"name": "Donepezil", "description": "Medication used to treat Alzheimer's disease."},
        {"name": "Erlotinib", "description": "Receptor tyrosine kinase inhibitor for cancer."},
        {"name": "Cisplatin", "description": "Chemotherapy medication."},
        {"name": "Aspirin", "description": "NSAID used to reduce pain, fever, or inflammation."},
        {"name": "Insulin glargine", "description": "Long-acting insulin."},
        {"name": "Levodopa", "description": "Medication used to treat Parkinson's disease."},
        {"name": "Imatinib", "description": "Targeted therapy for leukemia."},
    ]
    for i in range(11, 20):
        drugs.append({"name": f"Drug{i}", "description": f"Description for Drug{i}"})
        
    db_drugs = [models.Drug(**d) for d in drugs]
    db.add_all(db_drugs)
    db.commit()

    abstracts_templates = [
        "This study investigates the role of {gene} in the progression of {disease}. We observed that mutations in {gene} lead to altered function of {protein}, resulting in rapid tumor growth. The efficacy of {drug} was evaluated.",
        "Recent advances in understanding {disease} have highlighted the importance of {gene}. Our experiments demonstrate that {drug} effectively targets {protein}, mitigating the symptoms of {disease}.",
        "A comprehensive review of {gene} mutations and their association with {disease}. We focus on how {protein} stability is affected and discuss {drug} as a potential therapeutic intervention.",
        "Clinical trials of {drug} in patients with {disease} harboring {gene} mutations show promising results. The mechanism primarily involves inhibition of {protein}.",
        "We identified novel variants in {gene} that predispose individuals to {disease}. Functional assays revealed decreased {protein} activity. Current treatments including {drug} were assessed."
    ]

    for i in range(1, 55):
        gene = random.choice(db_genes)
        disease = random.choice(db_diseases)
        protein = random.choice(db_proteins)
        drug = random.choice(db_drugs)
        
        abstract = random.choice(abstracts_templates).format(
            gene=gene.name, disease=disease.name, protein=protein.name, drug=drug.name
        )
        title = f"The Impact of {gene.name} and {protein.name} in {disease.name}: A Review of {drug.name}"
        
        paper = models.Paper(
            title=title,
            abstract=abstract,
            authors=f"Author {i}A, Author {i}B",
            year=random.randint(2015, 2025),
            journal=f"Journal of Medical Research Vol {i}",
            keywords=f"{gene.name}, {disease.name}, {protein.name}, {drug.name}, therapy"
        )
        
        paper.genes.append(gene)
        paper.diseases.append(disease)
        paper.proteins.append(protein)
        paper.drugs.append(drug)
        
        db.add(paper)
    
    db.commit()
    print("Database seeded successfully with dummy data.")

if __name__ == '__main__':
    seed()
