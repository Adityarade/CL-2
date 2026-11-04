# Molecular Docking and Virtual Screening
# Computer Laboratory-II

import pandas as pd
import matplotlib.pyplot as plt

print("MOLECULAR DOCKING AND VIRTUAL SCREENING")
print("-" * 60)


# ---------------------------------------------------------
# 1. LIGAND DATA
# ---------------------------------------------------------

data = {
    "Ligand": [
        "Ligand_A",
        "Ligand_B",
        "Ligand_C",
        "Ligand_D",
        "Ligand_E",
        "Ligand_F",
        "Ligand_G",
        "Ligand_H"
    ],

    "Binding_Affinity": [
        -5.2,
        -7.8,
        -6.1,
        -9.0,
        -4.8,
        -8.2,
        -6.7,
        -7.1
    ]
}

df = pd.DataFrame(data)


# ---------------------------------------------------------
# 2. DISPLAY DOCKING RESULTS
# ---------------------------------------------------------

print("\nDocking Results:")
print(df)


# ---------------------------------------------------------
# 3. SORT LIGANDS BY BINDING AFFINITY
# ---------------------------------------------------------

# More negative score = better predicted binding

ranked_df = df.sort_values(
    by="Binding_Affinity"
)

ranked_df = ranked_df.reset_index(drop=True)

ranked_df["Rank"] = ranked_df.index + 1


print("\nRanked Ligands:")
print(
    ranked_df[
        ["Rank", "Ligand", "Binding_Affinity"]
    ]
)


# ---------------------------------------------------------
# 4. SELECT TOP CANDIDATES
# ---------------------------------------------------------

top_candidates = ranked_df.head(3)

print("\nTop 3 Potential Drug Candidates:")
print(
    top_candidates[
        ["Rank", "Ligand", "Binding_Affinity"]
    ]
)


# ---------------------------------------------------------
# 5. BEST LIGAND
# ---------------------------------------------------------

best_ligand = ranked_df.iloc[0]

print("\nBest Candidate:")
print("Ligand:", best_ligand["Ligand"])
print(
    "Binding Affinity:",
    best_ligand["Binding_Affinity"],
    "kcal/mol"
)


# ---------------------------------------------------------
# 6. VISUALIZATION
# ---------------------------------------------------------

plt.figure(figsize=(10, 6))

plt.bar(
    ranked_df["Ligand"],
    ranked_df["Binding_Affinity"]
)

plt.xlabel("Ligands")
plt.ylabel("Binding Affinity (kcal/mol)")
plt.title("Molecular Docking Scores")

plt.xticks(rotation=45)

plt.axhline(
    y=0,
    linewidth=1
)

plt.tight_layout()

plt.show()


# ---------------------------------------------------------
# 7. FINAL RESULT
# ---------------------------------------------------------

print("\nRESULT")
print("-" * 60)

print(
    "Virtual screening completed successfully."
)

print(
    "The ligand with the most negative docking score"
)

print(
    "was identified as the best predicted candidate."
)

print("Aditya Rade   BEAD23167")