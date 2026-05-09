import pandas as pd

df = pd.read_csv("data_clinical_patient.csv", header=4)

print(list(df.columns))
df.columns = df.columns.str.strip().str.upper()

# Select relevant columns
# ============================
cols_needed = ["PATIENT_ID", "OS_MONTHS", "DSS_MONTHS", "DFS_MONTHS"]

# Check columns exist
for col in cols_needed:
    if col not in df.columns:
        raise ValueError(f"Column '{col}' not found in dataset")

df_subset = df[cols_needed].copy()


# ============================
# Function to check differences
# ============================
def check_difference(row):
    values = [row["OS_MONTHS"], row["DSS_MONTHS"], row["DFS_MONTHS"]]
    values = [v for v in values if pd.notna(v)]

    # If all values same → no difference
    return len(set(values)) > 1


df_subset["DIFFERENT"] = df_subset.apply(check_difference, axis=1)

# ============================
# Export with highlighting
# ============================
output_file = "Data/months_comparison.xlsx"

with pd.ExcelWriter(output_file, engine="xlsxwriter") as writer:
    df_subset.to_excel(writer, index=False, sheet_name="Comparison")

    workbook = writer.book
    worksheet = writer.sheets["Comparison"]

    # Format for highlighting differences
    highlight_format = workbook.add_format({'bg_color': '#FF9999'})

    # Apply conditional formatting to OS, DSS, DFS columns
    for col_idx in range(1, 4):  # columns 1–3 = OS, DSS, DFS
        col_letter = chr(65 + col_idx)  # Excel column letter

        worksheet.conditional_format(
            f"{col_letter}2:{col_letter}{len(df_subset) + 1}",
            {
                "type": "formula",
                "criteria": f"=$E2=TRUE",  # DIFFERENT column
                "format": highlight_format
            }
        )

print(f"✅ Output saved to: {output_file}")