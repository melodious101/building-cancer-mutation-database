import pandas as pd
import numpy as np

# -----------------------------
# 1. File paths
# -----------------------------
input_file = "Data/data_clinical_patient_cleaned.xlsx"
output_file = "Data/cleaned_clinical_patient_final.csv"

# -----------------------------
# 2. Load Excel file
# Row 5 in Excel = header row
# Python uses 0-based indexing, so row 5 = header=4
# -----------------------------
df = pd.read_excel(input_file, header=4)

# -----------------------------
# 3. Standardize column names
# -----------------------------
df.columns = df.columns.str.strip()

# -----------------------------
# 4. Replace missing-value symbols with real null values
# -----------------------------
missing_values = [
    ".", "NA", "N/A", "na", "n/a", "NaN", "nan",
    "NULL", "null", "Unknown", "UNKNOWN", "",
    " ", "[Not Available]", "[Unknown]"
]

df = df.replace(missing_values, np.nan)

# -----------------------------
# 5. Remove fully empty rows and duplicate rows
# -----------------------------
df = df.dropna(how="all")
df = df.drop_duplicates()

# -----------------------------
# 6. Clean text fields
# -----------------------------
for col in df.select_dtypes(include="object").columns:
    df[col] = df[col].astype(str).str.strip()
    df[col] = df[col].replace("nan", np.nan)

# -----------------------------
# 7. Convert numeric columns
# -----------------------------
numeric_columns = [
    "AGE",
    "OS_MONTHS",
    "DSS_MONTHS",
    "DFS_MONTHS",
    "PFS_MONTHS"
]

for col in numeric_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# AGE should be whole number
if "AGE" in df.columns:
    df["AGE"] = df["AGE"].astype("Int64")

# -----------------------------
# 8. Convert Yes/No fields to Boolean
# -----------------------------
yes_no_boolean_columns = [
    "PRIOR_DX",
    "NEW_TUMOR_EVENT_AFTER_INITIAL_TREATMENT",
    "HISTORY_NEOADJUVANT_TRTYN",
    "RADIATION_THERAPY",
    "PRIMARY_LYMPH_NODE_PRESENTATION_ASSESSMENT"
]

boolean_map = {
    "Yes": True,
    "YES": True,
    "Y": True,
    "No": False,
    "NO": False,
    "N": False
}

for col in yes_no_boolean_columns:
    if col in df.columns:
        df[col] = df[col].map(boolean_map).astype("boolean")

# -----------------------------
# 9. Convert outcome status columns to Boolean
# True = event occurred
# False = censored/living/disease-free
# -----------------------------
status_boolean_columns = [
    "OS_STATUS",
    "DSS_STATUS",
    "DFS_STATUS",
    "PFS_STATUS"
]

def clean_status(value):
    if pd.isna(value):
        return pd.NA

    value = str(value).upper().strip()

    if value.startswith("1:"):
        return True

    if value.startswith("0:"):
        return False

    if "DECEASED" in value:
        return True

    if "PROGRESSION" in value:
        return True

    if "RECURRED" in value:
        return True

    if "LIVING" in value:
        return False

    if "CENSORED" in value:
        return False

    if "DISEASEFREE" in value or "TUMOR FREE" in value:
        return False

    return pd.NA

for col in status_boolean_columns:
    if col in df.columns:
        df[col] = df[col].apply(clean_status).astype("boolean")

# -----------------------------
# 10. Standardize categorical text values
# -----------------------------
categorical_columns = [
    "SEX",
    "ETHNICITY",
    "RACE",
    "GENETIC_ANCESTRY_LABEL",
    "AJCC_PATHOLOGIC_TUMOR_STAGE",
    "PATH_M_STAGE",
    "PATH_N_STAGE",
    "PATH_T_STAGE",
    "PERSON_NEOPLASM_CANCER_STATUS"
]

for col in categorical_columns:
    if col in df.columns:
        df[col] = df[col].astype("string").str.strip()

# -----------------------------
# 11. Optional: remove columns you decided not to keep
# -----------------------------
columns_to_remove = [
    "DSS_MONTHS",
    "ICD_O_3_SITE"
]

df = df.drop(columns=[col for col in columns_to_remove if col in df.columns])

# -----------------------------
# 12. Final duplicate check by PATIENT_ID
# If your database should only have one row per patient,
# this keeps the first row for each patient.
# -----------------------------
if "PATIENT_ID" in df.columns:
    df = df.drop_duplicates(subset=["PATIENT_ID"], keep="first")

# -----------------------------
# 13. Save cleaned dataset
# -----------------------------
df.to_csv(output_file, index=False)

print("Cleaning complete.")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])
print("Saved file as:", output_file)