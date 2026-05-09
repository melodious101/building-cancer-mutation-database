import pandas as pd

# ============================
# File paths (EDIT THESE)
# ============================
input_file = "Data/data_mutations.xls"  # your original file
output_file = "cleaned.xlsx"  # output file

# ============================
# Load Excel file
# ============================
df = pd.read_excel(input_file)

print("Original columns:", list(df.columns))

# ============================
# Initialize tracking lists
# ============================
cols_to_keep = []
removed_columns = []
mostly_same_columns = []

# ============================
# Process each column
# ============================
for col in df.columns:
    # Drop NaNs for fair comparison
    col_data = df[col].dropna()

    # Skip completely empty columns
    if len(col_data) == 0:
        removed_columns.append(col)
        continue

    # Get value counts
    value_counts = col_data.value_counts(normalize=True)

    # Most frequent value percentage
    max_freq = value_counts.iloc[0]

    # Case 1: All values identical (100%)
    if max_freq == 1.0:
        removed_columns.append(col)

    # Case 2: ≥95% identical
    elif max_freq >= 0.95:
        mostly_same_columns.append(col)
        cols_to_keep.append(col)

    # Case 3: Normal column
    else:
        cols_to_keep.append(col)

# ============================
# Create cleaned dataframe
# ============================
df_cleaned = df[cols_to_keep]

# ============================
# Save cleaned file
# ============================
df_cleaned.to_excel(output_file, index=False)

# ============================
# Output results
# ============================
print("\n=== RESULTS ===")

print("\nRemoved columns (all values identical):")
print(removed_columns)

print("\nColumns where ≥95% of values are the same:")
print(mostly_same_columns)

print("\nRemaining columns:")
print(list(df_cleaned.columns))

print(f"\nCleaned file saved as: {output_file}")