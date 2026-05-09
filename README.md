# building-cancer-mutation-database
This repository documents the process of building a database on locally hosted phpMyAdmin from raw data performed by TCGA firefhouse and pulled from cBioPortal. The purpose of the database is to connect mutations in patients with thyroid carcinama to patient outcomes and determine SNPs of interests.

#Tools and Technologies Used:
MySQL, phpMyAdmin, Python 3.13, pandas, numpy, PyCharm

#full sql dump of database: https://doi.org/10.6084/m9.figshare.32229285

#Repository Structure

ThyroidCancerMutationDB/
│
├── data/
│   ├── Raw/
│   │   ├── data_clinical_patient.txt
│   │   ├── data_clinical_sample.txt
│   │   ├── data_mutations.txt
│   │
│   └── Cleaned/
│       └── (cleaned output files generated after preprocessing)
│
├── diagrams/
│   └── RelationalDiagram.pdf
│
├── documents/
│   ├── dataDictionary.md
│   ├── decisionsLimitations.md
│   ├── excludedDataRational.md
│   ├── fullWriteup.pdf
│   └── scriptExecution.md
│
├── scripts/
│   ├── CreateSQL.py
│   │
│   └── DataCleaning/
│       ├── CheckSimilarities.py
│       ├── CheckUniqueInfo.py
│       ├── mutations_finalDataCleaning.py
│       ├── patient_finalDataCleaning.py
│       └── sample_finalDataCleaning.py
│
└── sql/
    ├── TestSQL.sql
    │
    └── DB_upload/
        ├── 00_create_tables.sql
        ├── 01_Patient.sql
        ├── 02_Sample.sql
        ├── 03_Gene_Info.sql
        ├── 04_Mutation_Info.sql
        ├── 05_Sequencing_Quality.sql
        ├── 06_Protein_Annotation.sql
        ├── 07_Transcript_Annotation.sql
        ├── 08_External_Variant_Annotation.sql
        ├── 09_Population_Frequency.sql
        └── 10_Sequence_Context.sql

#Data Sources
The project uses publicly available TCGA Thyroid Carcinoma (THCA) datasets.

Main datasets used:
data_mutations
data_clinical_patient
data_clinical_sample

Additional datasets such as RPPA, RNA-seq z-scores, and CNA/GISTIC data were excluded because they were outside the scope of the project.

#Execution Order
Raw TCGA Data 
→ patient_finalDataCleaning.py 
→ sample_finalDataCleaning.py 
→ mutations_finalDataCleaning.py 
→ Cleaned Data Files 
→ CreateSQL.py 
→ 00_create_tables.sql 
→ 01_Patient.sql 
→ 02_Sample.sql 
→ 03_Gene_Info.sql 
→ 04_Mutation_Info.sql 
→ 05_Sequencing_Quality.sql 
→ 06_Protein_Annotation.sql 
→ 07_Transcript_Annotation.sql 
→ 08_External_Variant_Annotation.sql 
→ 09_Population_Frequency.sql 
→ 10_Sequence_Context.sql 
→ TestSQL.sql

#Documentation and Diagrams in respectively named folders in repository
