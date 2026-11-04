# RNA-Seq Data Analysis
# Differential Gene Expression Analysis

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind

print("RNA-SEQ DATA ANALYSIS")
print("-" * 60)


# ---------------------------------------------------------
# 1. CREATE SAMPLE RNA-SEQ COUNT DATA
# ---------------------------------------------------------

data = {
    "Gene": [
        "Gene_A", "Gene_B", "Gene_C", "Gene_D",
        "Gene_E", "Gene_F", "Gene_G", "Gene_H",
        "Gene_I", "Gene_J"
    ],

    "Control_1": [100, 200, 50, 300, 500, 120, 80, 400, 60, 150],
    "Control_2": [110, 190, 55, 310, 480, 130, 85, 390, 65, 145],
    "Control_3": [105, 210, 52, 295, 510, 125, 82, 410, 58, 155],

    "Treatment_1": [300, 180, 200, 290, 520, 500, 75, 390, 250, 145],
    "Treatment_2": [320, 170, 210, 305, 530, 480, 80, 400, 270, 150],
    "Treatment_3": [310, 175, 195, 300, 510, 510, 78, 395, 260, 148]
}

df = pd.DataFrame(data)

print("\nRNA-Seq Count Data:")
print(df)


# ---------------------------------------------------------
# 2. BASIC DATA INFORMATION
# ---------------------------------------------------------

print("\n\nDATASET INFORMATION")
print("-" * 60)

print("Number of genes:", len(df))
print("Number of samples:", len(df.columns) - 1)

print("\nMissing Values:")
print(df.isnull().sum())


# ---------------------------------------------------------
# 3. QUALITY CONTROL
# ---------------------------------------------------------

print("\n\nQUALITY CONTROL")
print("-" * 60)

# Calculate total reads/counts for each sample

sample_columns = df.columns[1:]

library_sizes = df[sample_columns].sum()

print("\nTotal counts in each sample:")
print(library_sizes)


# Plot library sizes

plt.figure(figsize=(10, 5))

library_sizes.plot(kind="bar")

plt.title("RNA-Seq Library Size")
plt.xlabel("Samples")
plt.ylabel("Total Counts")
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()


# ---------------------------------------------------------
# 4. NORMALIZATION
# ---------------------------------------------------------

print("\n\nNORMALIZATION")
print("-" * 60)

# Convert counts to Counts Per Million (CPM)

cpm = df.copy()

for sample in sample_columns:
    cpm[sample] = (
        df[sample] / df[sample].sum()
    ) * 1000000

print("\nNormalized Expression Data (CPM):")
print(cpm.round(2))


# ---------------------------------------------------------
# 5. DIFFERENTIAL GENE EXPRESSION
# ---------------------------------------------------------

print("\n\nDIFFERENTIAL GENE EXPRESSION")
print("-" * 60)

control_columns = [
    "Control_1",
    "Control_2",
    "Control_3"
]

treatment_columns = [
    "Treatment_1",
    "Treatment_2",
    "Treatment_3"
]

results = []

for index, row in cpm.iterrows():

    gene = row["Gene"]

    control_values = row[control_columns].astype(float)
    treatment_values = row[treatment_columns].astype(float)

    control_mean = control_values.mean()
    treatment_mean = treatment_values.mean()

    # Log2 Fold Change
    log2fc = np.log2(
        (treatment_mean + 1) /
        (control_mean + 1)
    )

    # Statistical test
    statistic, p_value = ttest_ind(
        treatment_values,
        control_values,
        equal_var=False
    )

    results.append([
        gene,
        control_mean,
        treatment_mean,
        log2fc,
        p_value
    ])


results_df = pd.DataFrame(
    results,
    columns=[
        "Gene",
        "Control_Mean",
        "Treatment_Mean",
        "Log2_Fold_Change",
        "P_Value"
    ]
)


# ---------------------------------------------------------
# 6. MULTIPLE TESTING CORRECTION
# ---------------------------------------------------------

# Benjamini-Hochberg FDR correction

results_df = results_df.sort_values("P_Value")

n = len(results_df)

results_df["Adjusted_P_Value"] = [
    min(p * n / rank, 1)
    for rank, p in enumerate(
        results_df["P_Value"], start=1
    )
]

results_df = results_df.sort_values(
    "Adjusted_P_Value"
)


# ---------------------------------------------------------
# 7. IDENTIFY DIFFERENTIALLY EXPRESSED GENES
# ---------------------------------------------------------

results_df["Expression"] = "Not Significant"

results_df.loc[
    (results_df["Adjusted_P_Value"] < 0.05) &
    (results_df["Log2_Fold_Change"] > 0),
    "Expression"
] = "Upregulated"

results_df.loc[
    (results_df["Adjusted_P_Value"] < 0.05) &
    (results_df["Log2_Fold_Change"] < 0),
    "Expression"
] = "Downregulated"


print("\nDifferential Expression Results:")
print(results_df.round(4))


# ---------------------------------------------------------
# 8. VOLCANO PLOT
# ---------------------------------------------------------

plt.figure(figsize=(10, 6))

plot_data = results_df.copy()

plot_data["-log10(p-value)"] = -np.log10(
    plot_data["P_Value"] + 1e-10
)

sns.scatterplot(
    data=plot_data,
    x="Log2_Fold_Change",
    y="-log10(p-value)",
    hue="Expression",
    s=100
)

plt.axvline(
    x=1,
    linestyle="--"
)

plt.axvline(
    x=-1,
    linestyle="--"
)

plt.axhline(
    y=-np.log10(0.05),
    linestyle="--"
)

plt.title("Differential Gene Expression - Volcano Plot")

plt.xlabel("Log2 Fold Change")

plt.ylabel("-Log10(P-value)")

plt.tight_layout()

plt.show()


# ---------------------------------------------------------
# 9. HEATMAP
# ---------------------------------------------------------

expression_data = cpm.set_index("Gene")

plt.figure(figsize=(10, 6))

sns.heatmap(
    np.log2(expression_data + 1),
    annot=True,
    fmt=".1f"
)

plt.title("Gene Expression Heatmap")

plt.xlabel("Samples")

plt.ylabel("Genes")

plt.tight_layout()

plt.show()


# ---------------------------------------------------------
# 10. FINAL RESULTS
# ---------------------------------------------------------

print("\n\nFINAL RESULTS")
print("-" * 60)

print("\nUpregulated Genes:")

print(
    results_df[
        results_df["Expression"] == "Upregulated"
    ][
        ["Gene", "Log2_Fold_Change", "Adjusted_P_Value"]
    ].round(4)
)


print("\nDownregulated Genes:")

print(
    results_df[
        results_df["Expression"] == "Downregulated"
    ][
        ["Gene", "Log2_Fold_Change", "Adjusted_P_Value"]
    ].round(4)
)


print("\nRNA-Seq analysis completed successfully.")

print("Aditya Rade   BEAD23167")