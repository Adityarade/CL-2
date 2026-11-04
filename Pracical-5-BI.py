# Machine Learning for Genomic Data
# Computer Laboratory-II

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

print("MACHINE LEARNING FOR GENOMIC DATA")
print("-" * 60)


# ---------------------------------------------------------
# 1. CREATE GENOMIC DATASET
# ---------------------------------------------------------

np.random.seed(42)

data = {
    "Gene_1": [
        10, 12, 11, 13, 9,
        80, 85, 82, 90, 88,
        15, 14, 13, 12, 11,
        75, 78, 80, 82, 85
    ],

    "Gene_2": [
        80, 85, 82, 88, 90,
        15, 12, 18, 14, 16,
        78, 80, 82, 85, 88,
        10, 15, 12, 18, 14
    ],

    "Gene_3": [
        20, 22, 19, 21, 23,
        70, 72, 68, 75, 73,
        25, 24, 22, 23, 21,
        65, 68, 70, 72, 74
    ],

    "Gene_4": [
        30, 32, 28, 31, 29,
        60, 65, 62, 68, 64,
        35, 34, 32, 30, 33,
        58, 62, 65, 67, 63
    ],

    "Gene_5": [
        15, 18, 16, 17, 14,
        90, 88, 92, 85, 87,
        20, 19, 17, 18, 16,
        82, 85, 88, 90, 86
    ],

    "Class": [
        0, 0, 0, 0, 0,
        1, 1, 1, 1, 1,
        0, 0, 0, 0, 0,
        1, 1, 1, 1, 1
    ]
}

df = pd.DataFrame(data)


# ---------------------------------------------------------
# 2. DISPLAY DATASET
# ---------------------------------------------------------

print("\nGenomic Dataset:")
print(df)

print("\nDataset Shape:")
print(df.shape)


# ---------------------------------------------------------
# 3. CHECK MISSING VALUES
# ---------------------------------------------------------

print("\nMissing Values:")
print(df.isnull().sum())


# ---------------------------------------------------------
# 4. SEPARATE FEATURES AND TARGET
# ---------------------------------------------------------

X = df.drop("Class", axis=1)

y = df["Class"]


print("\nFeatures:")
print(X.columns.tolist())

print("\nTarget Classes:")
print(y.unique())


# ---------------------------------------------------------
# 5. TRAIN-TEST SPLIT
# ---------------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.30,
    random_state=42,
    stratify=y
)

print("\nTraining Samples:", len(X_train))
print("Testing Samples:", len(X_test))


# ---------------------------------------------------------
# 6. FEATURE SCALING FOR SVM
# ---------------------------------------------------------

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)

X_test_scaled = scaler.transform(X_test)


# ---------------------------------------------------------
# 7. RANDOM FOREST CLASSIFIER
# ---------------------------------------------------------

rf_model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

rf_model.fit(X_train, y_train)

rf_predictions = rf_model.predict(X_test)


# ---------------------------------------------------------
# 8. SUPPORT VECTOR MACHINE
# ---------------------------------------------------------

svm_model = SVC(
    kernel="linear",
    random_state=42
)

svm_model.fit(X_train_scaled, y_train)

svm_predictions = svm_model.predict(X_test_scaled)


# ---------------------------------------------------------
# 9. RANDOM FOREST EVALUATION
# ---------------------------------------------------------

print("\n\nRANDOM FOREST RESULTS")
print("-" * 60)

rf_accuracy = accuracy_score(
    y_test,
    rf_predictions
)

rf_precision = precision_score(
    y_test,
    rf_predictions,
    zero_division=0
)

rf_recall = recall_score(
    y_test,
    rf_predictions,
    zero_division=0
)

rf_f1 = f1_score(
    y_test,
    rf_predictions,
    zero_division=0
)

print("Accuracy :", rf_accuracy)
print("Precision:", rf_precision)
print("Recall   :", rf_recall)
print("F1-Score :", rf_f1)

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        rf_predictions,
        zero_division=0
    )
)


# ---------------------------------------------------------
# 10. SVM EVALUATION
# ---------------------------------------------------------

print("\n\nSVM RESULTS")
print("-" * 60)

svm_accuracy = accuracy_score(
    y_test,
    svm_predictions
)

svm_precision = precision_score(
    y_test,
    svm_predictions,
    zero_division=0
)

svm_recall = recall_score(
    y_test,
    svm_predictions,
    zero_division=0
)

svm_f1 = f1_score(
    y_test,
    svm_predictions,
    zero_division=0
)

print("Accuracy :", svm_accuracy)
print("Precision:", svm_precision)
print("Recall   :", svm_recall)
print("F1-Score :", svm_f1)

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        svm_predictions,
        zero_division=0
    )
)


# ---------------------------------------------------------
# 11. CONFUSION MATRICES
# ---------------------------------------------------------

rf_cm = confusion_matrix(
    y_test,
    rf_predictions
)

svm_cm = confusion_matrix(
    y_test,
    svm_predictions
)


plt.figure(figsize=(6, 5))

sns.heatmap(
    rf_cm,
    annot=True,
    fmt="d"
)

plt.title("Random Forest Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")

plt.tight_layout()
plt.show()


plt.figure(figsize=(6, 5))

sns.heatmap(
    svm_cm,
    annot=True,
    fmt="d"
)

plt.title("SVM Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")

plt.tight_layout()
plt.show()


# ---------------------------------------------------------
# 12. RANDOM FOREST FEATURE IMPORTANCE
# ---------------------------------------------------------

importance = rf_model.feature_importances_

feature_importance = pd.DataFrame({
    "Feature": X.columns,
    "Importance": importance
})

feature_importance = feature_importance.sort_values(
    by="Importance",
    ascending=False
)


print("\n\nFEATURE IMPORTANCE")
print("-" * 60)

print(feature_importance)


# ---------------------------------------------------------
# 13. FEATURE IMPORTANCE GRAPH
# ---------------------------------------------------------

plt.figure(figsize=(8, 5))

plt.bar(
    feature_importance["Feature"],
    feature_importance["Importance"]
)

plt.xlabel("Genomic Features")
plt.ylabel("Importance")
plt.title("Random Forest Feature Importance")

plt.tight_layout()
plt.show()


# ---------------------------------------------------------
# 14. MODEL COMPARISON
# ---------------------------------------------------------

comparison = pd.DataFrame({
    "Model": [
        "Random Forest",
        "SVM"
    ],

    "Accuracy": [
        rf_accuracy,
        svm_accuracy
    ],

    "Precision": [
        rf_precision,
        svm_precision
    ],

    "Recall": [
        rf_recall,
        svm_recall
    ],

    "F1-Score": [
        rf_f1,
        svm_f1
    ]
})

print("\n\nMODEL COMPARISON")
print("-" * 60)

print(comparison.round(4))


# ---------------------------------------------------------
# 15. FINAL RESULT
# ---------------------------------------------------------

print("\n\nRESULT")
print("-" * 60)

if rf_f1 > svm_f1:
    print("Random Forest performed better based on F1-Score.")
elif svm_f1 > rf_f1:
    print("SVM performed better based on F1-Score.")
else:
    print("Both models performed equally based on F1-Score.")

print("\nMachine learning classification completed successfully.")
print("Aditya Rade   BEAD23167")