# Protein Structure Prediction
# Homology Modeling - Basic Sequence Analysis

protein_sequence = "MKTIIALSYIFCLVFADYKDDDDK"

# Convert sequence to uppercase
protein_sequence = protein_sequence.upper()

print("PROTEIN STRUCTURE PREDICTION")
print("-" * 50)

# Display sequence
print("Protein Sequence:")
print(protein_sequence)

# Sequence length
print("\nProtein Length:", len(protein_sequence), "amino acids")


# ------------------------------------------------
# 1. AMINO ACID COMPOSITION
# ------------------------------------------------

print("\n1. AMINO ACID COMPOSITION")
print("-" * 50)

amino_acids = "ACDEFGHIKLMNPQRSTVWY"

for aa in amino_acids:
    count = protein_sequence.count(aa)

    if count > 0:
        print(aa, ":", count)


# ------------------------------------------------
# 2. BASIC PROPERTIES
# ------------------------------------------------

print("\n2. BASIC PROTEIN PROPERTIES")
print("-" * 50)

# Hydrophobic amino acids
hydrophobic = "AILMFWVY"

# Charged amino acids
charged = "DEKR"

hydrophobic_count = sum(
    protein_sequence.count(aa) for aa in hydrophobic
)

charged_count = sum(
    protein_sequence.count(aa) for aa in charged
)

print("Hydrophobic amino acids:", hydrophobic_count)
print("Charged amino acids:", charged_count)


# ------------------------------------------------
# 3. FASTA FILE CREATION
# ------------------------------------------------

print("\n3. FASTA FORMAT")
print("-" * 50)

fasta = ">Target_Protein\n" + protein_sequence

print(fasta)

# Save FASTA file
with open("target_protein.fasta", "w") as file:
    file.write(fasta)

print("\nFASTA file created successfully.")
print("File name: target_protein.fasta")


# ------------------------------------------------
# 4. TEMPLATE IDENTIFICATION
# ------------------------------------------------

print("\n4. HOMOLOGY MODELING WORKFLOW")
print("-" * 50)

print("Step 1: Submit the protein sequence to a")
print("        sequence similarity/search tool.")

print("Step 2: Identify homologous proteins with")
print("        experimentally determined structures.")

print("Step 3: Select the best template based on")
print("        sequence identity and coverage.")

print("Step 4: Align target and template sequences.")

print("Step 5: Build the 3D model.")

print("Step 6: Refine and validate the model.")


# ------------------------------------------------
# 5. FINAL RESULT
# ------------------------------------------------

print("\nRESULT")
print("-" * 50)

print("Target protein sequence analyzed successfully.")
print("FASTA file generated successfully.")
print("The sequence can now be used for homology")
print("modeling and 3D structure prediction.")
print("Aditya Rade   BEAD23167")