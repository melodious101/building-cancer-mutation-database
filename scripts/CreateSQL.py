import pandas as pd
import math
import os

patient_file = "final_cleaned_clinical_patient.xlsx"
sample_file = "final_cleaned_data_clinical_sample.xlsx"
mutation_file = "final_cleaned_data_mutations.xlsx"

output_folder = "mysql_upload_sql"
rows_per_file = 750

os.makedirs(output_folder, exist_ok=True)


def clean_dataframe(df):
    null_values = [".", "NA", "N/A", "na", "n/a", "", " ", "null", "NULL", "None"]
    df = df.replace(null_values, pd.NA)
    df = df.drop_duplicates()
    return df


def sql_value(value):
    if pd.isna(value):
        return "NULL"

    if isinstance(value, bool):
        return "1" if value else "0"

    if isinstance(value, (int, float)):
        if isinstance(value, float) and math.isnan(value):
            return "NULL"
        return str(value)

    value = str(value)
    value = value.replace("\\", "\\\\")
    value = value.replace("'", "''")
    return "'" + value + "'"


def write_insert_file(df, table_name, file_number):
    file_path = os.path.join(output_folder, f"{file_number:02d}_{table_name}.sql")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write("SET FOREIGN_KEY_CHECKS = 0;\n\n")

        columns = list(df.columns)
        column_text = ", ".join([f"`{col}`" for col in columns])

        for start in range(0, len(df), rows_per_file):
            chunk = df.iloc[start:start + rows_per_file]

            f.write(f"INSERT IGNORE INTO `{table_name}` ({column_text}) VALUES\n")

            row_texts = []
            for _, row in chunk.iterrows():
                values = [sql_value(row[col]) for col in columns]
                row_texts.append("(" + ", ".join(values) + ")")

            f.write(",\n".join(row_texts))
            f.write(";\n\n")

        f.write("SET FOREIGN_KEY_CHECKS = 1;\n")

    return file_path


patient_df = clean_dataframe(pd.read_excel(patient_file))
sample_df = clean_dataframe(pd.read_excel(sample_file))
mutation_df = clean_dataframe(pd.read_excel(mutation_file))

# Remove mutation rows without SAMPLE_ID
mutation_df = mutation_df[mutation_df["SAMPLE_ID"].notna()].copy()

# Add missing sample IDs from mutation data into sample table
existing_sample_ids = set(sample_df["SAMPLE_ID"].dropna())
mutation_sample_ids = set(mutation_df["SAMPLE_ID"].dropna())
missing_sample_ids = sorted(mutation_sample_ids - existing_sample_ids)

missing_sample_rows = []

for sample_id in missing_sample_ids:
    patient_id = str(sample_id)[0:12]

    missing_sample_rows.append({
        "PATIENT_ID": patient_id,
        "SAMPLE_ID": sample_id,
        "TUMOR_TYPE": None,
        "TISSUE_PROSPECTIVE_COLLECTION_INDICATOR": None,
        "TISSUE_RETROSPECTIVE_COLLECTION_INDICATOR": None,
        "TISSUE_SOURCE_SITE_CODE": None,
        "ANEUPLOIDY_SCORE": None,
        "MSI_SCORE_MANTIS": None,
        "MSI_SENSOR_SCORE": None,
        "TMB_NONSYNONYMOUS": None,
        "TBL_SCORE": None
    })

if missing_sample_rows:
    sample_df = pd.concat([sample_df, pd.DataFrame(missing_sample_rows)], ignore_index=True)

# Create mutation_id because this is one of your actual given IDs
mutation_df.insert(0, "mutation_id", ["MUT" + str(i + 1).zfill(8) for i in range(len(mutation_df))])

# Gene table still needs gene_ID because Mutation_Info links to Gene_Info
# This is a generated biological lookup ID, not AUTO_INCREMENT, because mutation rows need to reference it.
gene_columns = [
    "Hugo_Symbol",
    "Entrez_Gene_Id",
    "HGNC_ID",
    "SYMBOL",
    "SYMBOL_SOURCE",
    "BIOTYPE"
]

gene_df = mutation_df[gene_columns].drop_duplicates().reset_index(drop=True)
gene_df.insert(0, "gene_ID", ["GENE" + str(i + 1).zfill(6) for i in range(len(gene_df))])

mutation_df = mutation_df.merge(gene_df, on=gene_columns, how="left")

patient_table = patient_df.copy()
sample_table = sample_df.copy()

mutation_info = mutation_df[[
    "mutation_id",
    "SAMPLE_ID",
    "gene_ID",
    "Chromosome",
    "Start_Position",
    "End_Position",
    "Reference_Allele",
    "Tumor_Seq_Allele1",
    "Tumor_Seq_Allele2",
    "Match_Norm_Seq_Allele1",
    "Match_Norm_Seq_Allele2",
    "Variant_Classification",
    "Variant_Type",
    "Consequence",
    "IMPACT",
    "SOMATIC"
]].copy()

mutation_info = mutation_info.rename(columns={"SAMPLE_ID": "sample_id"})

# No sequencing_evidence_id column here.
# MySQL will create it automatically.
sequencing_quality = mutation_df[[
    "mutation_id",
    "t_depth",
    "t_alt_count",
    "n_depth",
    "n_alt_count",
    "NCALLERS"
]].copy()

# No protein_annotation_id column.
protein_annotation = mutation_df[[
    "mutation_id",
    "HGVSp",
    "Protein_position",
    "Amino_acids",
    "Codons",
    "PolyPhen",
    "SIFT",
    "DOMAINS"
]].copy()

# No transcript_annotation_id column.
transcript_annotation = mutation_df[[
    "mutation_id",
    "Transcript_ID",
    "RefSeq",
    "Feature",
    "EXON",
    "INTRON",
    "CDS_position",
    "cDNA_position",
    "CANONICAL",
    "CCDS",
    "ENSP",
    "SWISSPROT",
    "TREMBL",
    "UNIPARC",
    "HGVS_OFFSET"
]].copy()

# No external_annotation_id column.
external_annotation = mutation_df[[
    "mutation_id",
    "dbSNP_RS",
    "COSMIC",
    "Existing_variation",
    "CLIN_SIG",
    "PUBMED"
]].copy()

# No population_frequency_id column.
population_frequency = mutation_df[[
    "mutation_id",
    "GMAF",
    "SAS_MAF"
]].copy()

# No sequence_context_id column.
sequence_context = mutation_df[[
    "mutation_id",
    "CONTEXT"
]].copy()

schema_sql = """
SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS Sequence_Context;
DROP TABLE IF EXISTS Population_Frequency;
DROP TABLE IF EXISTS External_Variant_Annotation;
DROP TABLE IF EXISTS Transcript_Annotation;
DROP TABLE IF EXISTS Protein_Annotation;
DROP TABLE IF EXISTS Sequencing_Quality;
DROP TABLE IF EXISTS Mutation_Info;
DROP TABLE IF EXISTS Gene_Info;
DROP TABLE IF EXISTS Sample;
DROP TABLE IF EXISTS Patient;

CREATE TABLE Patient (
    PATIENT_ID VARCHAR(25) PRIMARY KEY,
    AGE INT,
    SEX VARCHAR(10),
    ETHNICITY VARCHAR(50),
    RACE VARCHAR(50),
    GENETIC_ANCESTRY_LABEL VARCHAR(50),
    PRIOR_DX BOOLEAN,
    AJCC_PATHOLOGIC_TUMOR_STAGE VARCHAR(20),
    PATH_M_STAGE VARCHAR(10),
    PATH_N_STAGE VARCHAR(10),
    PATH_T_STAGE VARCHAR(10),
    PRIMARY_LYMPH_NODE_PRESENTATION_ASSESSMENT BOOLEAN,
    PERSON_NEOPLASM_CANCER_STATUS VARCHAR(30),
    NEW_TUMOR_EVENT_AFTER_INITIAL_TREATMENT BOOLEAN,
    HISTORY_NEOADJUVANT_TRTYN BOOLEAN,
    RADIATION_THERAPY BOOLEAN,
    OS_STATUS BOOLEAN,
    OS_MONTHS FLOAT,
    DSS_STATUS BOOLEAN,
    DFS_STATUS BOOLEAN,
    DFS_MONTHS FLOAT,
    PFS_STATUS BOOLEAN,
    PFS_MONTHS FLOAT
);

CREATE TABLE Sample (
    SAMPLE_ID VARCHAR(25) PRIMARY KEY,
    PATIENT_ID VARCHAR(25),
    TUMOR_TYPE VARCHAR(100),
    TISSUE_PROSPECTIVE_COLLECTION_INDICATOR VARCHAR(10),
    TISSUE_RETROSPECTIVE_COLLECTION_INDICATOR VARCHAR(10),
    TISSUE_SOURCE_SITE_CODE VARCHAR(10),
    ANEUPLOIDY_SCORE INT,
    MSI_SCORE_MANTIS FLOAT,
    MSI_SENSOR_SCORE FLOAT,
    TMB_NONSYNONYMOUS FLOAT,
    TBL_SCORE INT,
    FOREIGN KEY (PATIENT_ID) REFERENCES Patient(PATIENT_ID)
);

CREATE TABLE Gene_Info (
    gene_ID VARCHAR(20) PRIMARY KEY,
    Hugo_Symbol VARCHAR(25),
    Entrez_Gene_Id INT,
    HGNC_ID INT,
    SYMBOL VARCHAR(25),
    SYMBOL_SOURCE VARCHAR(30),
    BIOTYPE VARCHAR(50)
);

CREATE TABLE Mutation_Info (
    mutation_id VARCHAR(20) PRIMARY KEY,
    sample_id VARCHAR(25),
    gene_ID VARCHAR(20),
    Chromosome VARCHAR(5),
    Start_Position INT,
    End_Position INT,
    Reference_Allele VARCHAR(100),
    Tumor_Seq_Allele1 VARCHAR(100),
    Tumor_Seq_Allele2 VARCHAR(100),
    Match_Norm_Seq_Allele1 VARCHAR(100),
    Match_Norm_Seq_Allele2 VARCHAR(100),
    Variant_Classification VARCHAR(50),
    Variant_Type VARCHAR(20),
    Consequence VARCHAR(150),
    IMPACT VARCHAR(20),
    SOMATIC VARCHAR(25),
    FOREIGN KEY (sample_id) REFERENCES Sample(SAMPLE_ID),
    FOREIGN KEY (gene_ID) REFERENCES Gene_Info(gene_ID)
);

CREATE TABLE Sequencing_Quality (
    sequencing_evidence_id INT AUTO_INCREMENT PRIMARY KEY,
    mutation_id VARCHAR(20),
    t_depth INT,
    t_alt_count INT,
    n_depth INT,
    n_alt_count INT,
    NCALLERS INT,
    FOREIGN KEY (mutation_id) REFERENCES Mutation_Info(mutation_id)
);

CREATE TABLE Protein_Annotation (
    protein_annotation_id INT AUTO_INCREMENT PRIMARY KEY,
    mutation_id VARCHAR(20),
    HGVSp VARCHAR(50),
    Protein_position INT,
    Amino_acids VARCHAR(30),
    Codons VARCHAR(75),
    PolyPhen VARCHAR(50),
    SIFT VARCHAR(50),
    DOMAINS TEXT,
    FOREIGN KEY (mutation_id) REFERENCES Mutation_Info(mutation_id)
);

CREATE TABLE Transcript_Annotation (
    transcript_annotation_id INT AUTO_INCREMENT PRIMARY KEY,
    mutation_id VARCHAR(20),
    Transcript_ID VARCHAR(30),
    RefSeq VARCHAR(30),
    Feature VARCHAR(30),
    EXON VARCHAR(30),
    INTRON VARCHAR(30),
    CDS_position VARCHAR(30),
    cDNA_position VARCHAR(30),
    CANONICAL VARCHAR(10),
    CCDS VARCHAR(30),
    ENSP VARCHAR(30),
    SWISSPROT VARCHAR(100),
    TREMBL TEXT,
    UNIPARC VARCHAR(30),
    HGVS_OFFSET VARCHAR(10),
    FOREIGN KEY (mutation_id) REFERENCES Mutation_Info(mutation_id)
);

CREATE TABLE External_Variant_Annotation (
    external_annotation_id INT AUTO_INCREMENT PRIMARY KEY,
    mutation_id VARCHAR(20),
    dbSNP_RS VARCHAR(50),
    COSMIC TEXT,
    Existing_variation VARCHAR(200),
    CLIN_SIG VARCHAR(100),
    PUBMED VARCHAR(50),
    FOREIGN KEY (mutation_id) REFERENCES Mutation_Info(mutation_id)
);

CREATE TABLE Population_Frequency (
    population_frequency_id INT AUTO_INCREMENT PRIMARY KEY,
    mutation_id VARCHAR(20),
    GMAF VARCHAR(30),
    SAS_MAF VARCHAR(30),
    FOREIGN KEY (mutation_id) REFERENCES Mutation_Info(mutation_id)
);

CREATE TABLE Sequence_Context (
    sequence_context_id INT AUTO_INCREMENT PRIMARY KEY,
    mutation_id VARCHAR(20),
    CONTEXT VARCHAR(100),
    FOREIGN KEY (mutation_id) REFERENCES Mutation_Info(mutation_id)
);

SET FOREIGN_KEY_CHECKS = 1;
"""

schema_path = os.path.join(output_folder, "00_create_tables.sql")

with open(schema_path, "w", encoding="utf-8") as f:
    f.write(schema_sql)

file_number = 1

write_insert_file(patient_table, "Patient", file_number)
file_number += 1

write_insert_file(sample_table, "Sample", file_number)
file_number += 1

write_insert_file(gene_df, "Gene_Info", file_number)
file_number += 1

write_insert_file(mutation_info, "Mutation_Info", file_number)
file_number += 1

write_insert_file(sequencing_quality, "Sequencing_Quality", file_number)
file_number += 1

write_insert_file(protein_annotation, "Protein_Annotation", file_number)
file_number += 1

write_insert_file(transcript_annotation, "Transcript_Annotation", file_number)
file_number += 1

write_insert_file(external_annotation, "External_Variant_Annotation", file_number)
file_number += 1

write_insert_file(population_frequency, "Population_Frequency", file_number)
file_number += 1

write_insert_file(sequence_context, "Sequence_Context", file_number)

print("Done.")
print("SQL files were created in this folder:", output_folder)
print()
print("Upload files to phpMyAdmin in this order:")
print("1. 00_create_tables.sql")
print("2. 01_Patient.sql")
print("3. 02_Sample.sql")
print("4. 03_Gene_Info.sql")
print("5. 04_Mutation_Info.sql")
print("6. Then the rest of the numbered files.")
print()
print("Missing sample IDs added to Sample table:")
print(missing_sample_ids)