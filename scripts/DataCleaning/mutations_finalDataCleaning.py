import pandas as pd
import numpy as np

# ------------------------------------------------------------
# 1. INPUT FILE
# ------------------------------------------------------------
# Put this Python file in the same folder as your Excel sheet,
# or replace this with the full file path.
input_file = "data_mutations_init_cleaned.xlsx"

# Name of the final cleaned output file
output_file = "data_mutations_final_cleaned.xlsx"

# ------------------------------------------------------------
# 2. READ EXCEL FILE
# ------------------------------------------------------------
df = pd.read_excel(input_file)

# ------------------------------------------------------------
# 3. REPLACE BAD/MISSING VALUES WITH TRUE NULLS
# ------------------------------------------------------------
missing_values = [
    ".",
    "NA",
    "N/A",
    "na",
    "n/a",
    "",
    " ",
    "null",
    "NULL",
    "None",
    "none"
]

df = df.replace(missing_values, np.nan)

# ------------------------------------------------------------
# 4. REORDER COLUMNS LOGICALLY
# ------------------------------------------------------------
column_order = [
    "Tumor_Sample_Barcode",
    "Matched_Norm_Sample_Barcode",
    "Hugo_Symbol",
    "Entrez_Gene_Id",

    "Chromosome",
    "Start_Position",
    "End_Position",

    "Variant_Classification",
    "Variant_Type",
    "Consequence",
    "Reference_Allele",
    "Tumor_Seq_Allele1",
    "Tumor_Seq_Allele2",
    "Match_Norm_Seq_Allele1",
    "Match_Norm_Seq_Allele2",

    "t_depth",
    "t_ref_count",
    "t_alt_count",
    "n_depth",
    "n_ref_count",
    "n_alt_count",
    "NCALLERS",

    "IMPACT",
    "HGVSp",
    "Protein_position",
    "Amino_acids",
    "Codons",
    "PolyPhen",
    "SIFT",
    "CLIN_SIG",

    "dbSNP_RS",
    "COSMIC",
    "Existing_variation",
    "PUBMED",

    "Transcript_ID",
    "RefSeq",
    "Feature",
    "EXON",
    "INTRON",
    "CDS_position",
    "cDNA_position",

    "BIOTYPE",
    "CANONICAL",
    "CCDS",
    "ENSP",
    "SWISSPROT",
    "TREMBL",
    "UNIPARC",
    "DOMAINS",

    "GMAF",
    "SAS_MAF",

    "HGNC_ID",
    "HGVS_OFFSET",
    "CONTEXT",
    "SOMATIC",
    "SYMBOL",
    "SYMBOL_SOURCE",
    "Allele"
]

# Only keep columns that actually exist in your file
existing_columns = [col for col in column_order if col in df.columns]
df = df[existing_columns]

# ------------------------------------------------------------
# 5. CONVERT COLUMN DATA TYPES
# ------------------------------------------------------------

# Integer columns
int_columns = [
    "Entrez_Gene_Id",
    "Start_Position",
    "End_Position",
    "t_depth",
    "t_ref_count",
    "t_alt_count",
    "n_depth",
    "n_ref_count",
    "n_alt_count",
    "NCALLERS",
    "Protein_position",
    "HGNC_ID"
]

for col in int_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")

# Float columns
# These are left as float because they may contain decimal allele frequencies.
float_columns = [
    "GMAF",
    "SAS_MAF"
]

for col in float_columns:
    if col in df.columns:
        # Some values may look like "A:0.001", so only pure numbers will convert.
        df[col] = pd.to_numeric(df[col], errors="coerce")

# String columns
string_columns = [
    "Tumor_Sample_Barcode",
    "Matched_Norm_Sample_Barcode",
    "Hugo_Symbol",
    "Chromosome",
    "Variant_Classification",
    "Variant_Type",
    "Consequence",
    "Reference_Allele",
    "Tumor_Seq_Allele1",
    "Tumor_Seq_Allele2",
    "Match_Norm_Seq_Allele1",
    "Match_Norm_Seq_Allele2",
    "IMPACT",
    "HGVSp",
    "Amino_acids",
    "Codons",
    "PolyPhen",
    "SIFT",
    "CLIN_SIG",
    "dbSNP_RS",
    "COSMIC",
    "Existing_variation",
    "PUBMED",
    "Transcript_ID",
    "RefSeq",
    "Feature",
    "EXON",
    "INTRON",
    "CDS_position",
    "cDNA_position",
    "BIOTYPE",
    "CANONICAL",
    "CCDS",
    "ENSP",
    "SWISSPROT",
    "TREMBL",
    "UNIPARC",
    "DOMAINS",
    "HGVS_OFFSET",
    "CONTEXT",
    "SOMATIC",
    "SYMBOL",
    "SYMBOL_SOURCE",
    "Allele"
]

for col in string_columns:
    if col in df.columns:
        df[col] = df[col].astype("string")

# ------------------------------------------------------------
# 6. OUTPUT FINAL CLEANED EXCEL FILE
# ------------------------------------------------------------
df.to_excel(output_file, index=False)

print("Final cleaned Excel file created:", output_file)
print("Rows:", len(df))
print("Columns:", len(df.columns))
print(df.dtypes)