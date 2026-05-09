
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
