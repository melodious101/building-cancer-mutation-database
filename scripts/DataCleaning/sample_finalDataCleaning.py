import pandas as pd
import numpy as np

# ------------------------------------------------------------
# 1. INPUT / OUTPUT FILES
# ------------------------------------------------------------
input_file = "Data/data_clinical_sample.xlsx"
output_file = "data_clinical_sample_cleaned.xlsx"

# ------------------------------------------------------------
# 2. READ FILE (NO HEADER YET)
# ------------------------------------------------------------
df = pd.read_excel(input_file, header=None)

# ------------------------------------------------------------
# 3. SET ROW 5 AS HEADER (index 4) AND REMOVE FIRST 4 ROWS
# ------------------------------------------------------------
df.columns = df.iloc[4]   # row 5 becomes header
df = df.iloc[5:].reset_index(drop=True)

# ------------------------------------------------------------
# 4. CLEAN MISSING VALUES → NULL
# ------------------------------------------------------------
missing_values = [
    ".", "NA", "N/A", "na", "n/a",
    "", " ", "null", "NULL", "None", "none"
]

df = df.replace(missing_values, np.nan)

# ------------------------------------------------------------
# 5. CONVERT DATA TYPES
# ------------------------------------------------------------

# --- BOOLEAN COLUMNS (Yes/No → True/False) ---
boolean_columns = [
    "TISSUE_PROSPECTIVE_COLLECTION_INDICATOR",
    "TISSUE_RETROSPECTIVE_COLLECTION_INDICATOR"
]

for col in boolean_columns:
    if col in df.columns:
        df[col] = df[col].map({
            "Yes": True,
            "No": False
        })

# --- INTEGER COLUMNS ---
int_columns = [
    "ANEUPLOIDY_SCORE",
    "TBL_SCORE"
]

for col in int_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")

# --- FLOAT COLUMNS ---
float_columns = [
    "MSI_SCORE_MANTIS",
    "MSI_SENSOR_SCORE",
    "TMB_NONSYNONYMOUS"
]

for col in float_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# --- STRING COLUMNS ---
string_columns = [
    "PATIENT_ID",
    "SAMPLE_ID",
    "TUMOR_TYPE",
    "TISSUE_SOURCE_SITE_CODE"
]

for col in string_columns:
    if col in df.columns:
        df[col] = df[col].astype("string")

# ------------------------------------------------------------
# 6. OUTPUT CLEANED FILE
# ------------------------------------------------------------
df.to_excel(output_file, index=False)

print("Cleaned file saved as:", output_file)
print("\nColumn types:")
print(df.dtypes)