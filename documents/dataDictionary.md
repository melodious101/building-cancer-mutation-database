\# Data Dictionary

\#\# Patient Demographics

| Column | Recommended SQL Type | Key | Why / Description |  
|---|---|---|---|  
| PATIENT\_ID | VARCHAR(20) | PK | Unique TCGA patient identifier. |  
| AGE | INT | NA | Age at diagnosis in years. |  
| Race\_ID | VARCHAR(2) | FK | Links patient to the Race lookup table. |  
| Sex\_ID | VARCHAR(2) | FK | Links patient to the Sex lookup table. |  
| Ethnicity\_ID | VARCHAR(2) | FK | Links patient to the Ethnicity lookup table. |  
| Genetic\_Ancestry\_Label\_ID | VARCHAR(2) | FK | Links patient to the Genetic Ancestry lookup table. |

\#\# Race

| Column | Recommended SQL Type | Key | Why / Description |  
|---|---|---|---|  
| Race\_ID | VARCHAR(2) | PK | Unique identifier for each race category. |  
| RACE | VARCHAR(50) | NA | Patient-reported race. |

\#\# Sex

| Column | Recommended SQL Type | Key | Why / Description |  
|---|---|---|---|  
| Sex\_ID | VARCHAR(2) | PK | Unique identifier for each sex category. |  
| SEX | VARCHAR(10) | NA | Biological sex, such as Male or Female. |

\#\# Ethnicity

| Column | Recommended SQL Type | Key | Why / Description |  
|---|---|---|---|  
| Ethnicity\_ID | VARCHAR(2) | PK | Unique identifier for each ethnicity category. |  
| ETHNICITY | VARCHAR(50) | NA | Patient-reported ethnicity. |

\#\# Genetic Ancestry

| Column | Recommended SQL Type | Key | Why / Description |  
|---|---|---|---|  
| Genetic\_Ancestry\_Label\_ID | VARCHAR(2) | PK | Unique identifier for each genetic ancestry category. |  
| GENETIC\_ANCESTRY\_LABEL | VARCHAR(20) | NA | Inferred genetic ancestry label, such as EUR, AFR, or EAS. |

\#\# Patient Outcome

| Column | Recommended SQL Type | Key | Why / Description |  
|---|---|---|---|  
| outcome\_ID | VARCHAR(20) | PK | Unique identifier for each patient outcome record. |  
| PATIENT\_ID | VARCHAR(20) | FK | Links outcome information to the patient. |  
| PRIOR\_DX | BOOLEAN | NA | Indicates whether the patient had a prior diagnosis. |  
| NEW\_TUMOR\_EVENT\_AFTER\_INITIAL\_TREATMENT | BOOLEAN | NA | Indicates whether the patient had recurrence or a new tumor event after initial treatment. |  
| OS\_MONTHS | FLOAT(10,2) | NA | Overall survival time in months. |  
| OS\_STATUS | BOOLEAN | NA | Overall survival status, converted from living/deceased status. |  
| DSS\_STATUS | BOOLEAN | NA | Disease-specific survival status. |  
| DFS\_STATUS | BOOLEAN | NA | Disease-free survival status after treatment. |  
| DFS\_MONTHS | FLOAT(10,2) | NA | Disease-free survival time in months. |  
| PFS\_STATUS | BOOLEAN | NA | Progression-free survival status. |  
| PFS\_MONTHS | FLOAT(10,2) | NA | Progression-free survival time in months. |

\#\# Patient Treatment Info

| Column | Recommended SQL Type | Key | Why / Description |  
|---|---|---|---|  
| Treatment\_ID | VARCHAR(20) | PK | Unique identifier for each patient treatment record. |  
| PATIENT\_ID | VARCHAR(20) | FK | Links treatment information to the patient. |  
| HISTORY\_NEOADJUVANT\_TRTYN | BOOLEAN | NA | Indicates whether the patient received pre-surgical treatment. |  
| RADIATION\_THERAPY | BOOLEAN | NA | Indicates whether the patient received radiation therapy. |

\#\# Disease Stage

| Column | Recommended SQL Type | Key | Why / Description |  
|---|---|---|---|  
| Disease\_Stage\_ID | VARCHAR(2) | PK | Unique identifier for each disease stage category. |  
| AJCC\_PATHOLOGIC\_TUMOR\_STAGE | VARCHAR(20) | NA | Overall pathological cancer stage, such as Stage I–IV. |

\#\# Patient Prognosis

| Column | Recommended SQL Type | Key | Why / Description |  
|---|---|---|---|  
| Prognosis\_ID | VARCHAR(20) | PK | Unique identifier for each patient prognosis record. |  
| PATIENT\_ID | VARCHAR(20) | FK | Links prognosis information to the patient. |  
| Disease\_Stage\_ID | VARCHAR(2) | FK | Links prognosis information to the Disease Stage lookup table. |  
| ICD\_O\_3\_HISTOLOGY | VARCHAR(10) | NA | Histological tumor classification code. |

\#\# Neoplasm Assessment

| Column | Recommended SQL Type | Key | Why / Description |  
|---|---|---|---|  
| Neoplasm\_Assessment\_ID | VARCHAR(20) | PK | Unique identifier for each neoplasm assessment record. |  
| PATIENT\_ID | VARCHAR(20) | FK | Links neoplasm assessment information to the patient. |  
| PERSON\_NEOPLASM\_CANCER\_STATUS | VARCHAR(20) | NA | Tumor status, such as Tumor Free or With Tumor. |  
| PATH\_M\_STAGE | VARCHAR(5) | NA | Metastasis stage, such as M0, M1, or MX. |  
| PATH\_N\_STAGE | VARCHAR(5) | NA | Lymph node involvement stage, such as N0 or N1. |  
| PATH\_T\_STAGE | VARCHAR(5) | NA | Primary tumor stage, such as T1–T4. |  
| PRIMARY\_LYMPH\_NODE\_PRESENTATION\_ASSESSMENT | BOOLEAN | NA | Indicates whether lymph node involvement was present at diagnosis. |

\#\# Sample

| Column | Recommended SQL Type | Key | Why / Description |  
|---|---|---|---|  
| SAMPLE\_ID | VARCHAR(25) | PK | Unique TCGA tumor sample identifier. |  
| PATIENT\_ID | VARCHAR(20) | FK | Links sample to the patient it came from. |  
| Matched\_Norm\_Sample\_Barcode | VARCHAR(25) | NA | TCGA barcode for the matched normal sample. |  
| TUMOR\_TYPE | VARCHAR(100) | NA | Thyroid cancer histological subtype, such as classical/usual, follicular, tall cell, or other. |  
| TISSUE\_PROSPECTIVE\_COLLECTION\_INDICATOR | BOOLEAN | NA | Indicates whether tissue was collected prospectively. |  
| TISSUE\_RETROSPECTIVE\_COLLECTION\_INDICATOR | BOOLEAN | NA | Indicates whether tissue was collected retrospectively. |  
| TISSUE\_SOURCE\_SITE\_CODE | VARCHAR(5) | NA | TCGA tissue source site code. |  
| ANEUPLOIDY\_SCORE | INT | NA | Numeric score representing chromosomal copy-number imbalance. |  
| MSI\_SCORE\_MANTIS | FLOAT(10,2) | NA | Microsatellite instability score calculated using MANTIS. |  
| MSI\_SENSOR\_SCORE | FLOAT(10,2) | NA | Microsatellite instability score calculated using MSISensor. |  
| TMB\_NONSYNONYMOUS | FLOAT(10,2) | NA | Tumor mutational burden based on nonsynonymous mutations. |  
| TBL\_SCORE | INT | NA | Tumor break load score representing unbalanced somatic chromosomal breaks. |

\#\# Gene Info

| Column | Recommended SQL Type | Key | Why / Description |  
|---|---|---|---|  
| gene\_ID | VARCHAR(20) | PK | Unique identifier for each gene record. |  
| Hugo\_Symbol | VARCHAR(25) | NA | Gene symbol. |  
| Entrez\_Gene\_Id | INT | NA | NCBI Entrez gene identifier. |  
| HGNC\_ID | INT | NA | HGNC gene identifier. |  
| SYMBOL | VARCHAR(25) | NA | Gene symbol from annotation source; kept because it appears in the schema, though it may overlap with Hugo\_Symbol. |  
| SYMBOL\_SOURCE | VARCHAR(30) | NA | Source database or authority for the gene symbol. |  
| BIOTYPE | VARCHAR(50) | NA | Gene or transcript biotype, such as protein coding. |

\#\# Mutation Info

| Column | Recommended SQL Type | Key | Why / Description |  
|---|---|---|---|  
| mutation\_id | VARCHAR(20) | PK | Unique identifier for each mutation record. |  
| SAMPLE\_ID | VARCHAR(25) | FK | Links mutation to the tumor sample. |  
| gene\_ID | VARCHAR(20) | FK | Links mutation to the associated gene record. |  
| Chromosome | VARCHAR(2) | NA | Chromosome where the mutation is located. |  
| Start\_Position | INT | NA | Genomic start coordinate of the mutation. |  
| End\_Position | INT | NA | Genomic end coordinate of the mutation. |  
| Reference\_Allele | VARCHAR(100) | NA | Reference allele at the mutation site. |  
| Tumor\_Seq\_Allele1 | VARCHAR(100) | NA | First tumor sequencing allele. |  
| Tumor\_Seq\_Allele2 | VARCHAR(100) | NA | Second tumor sequencing allele, usually the alternate allele. |  
| Match\_Norm\_Seq\_Allele1 | VARCHAR(100) | NA | First matched normal sequencing allele. |  
| Match\_Norm\_Seq\_Allele2 | VARCHAR(100) | NA | Second matched normal sequencing allele. |  
| Variant\_Classification | VARCHAR(30) | NA | Mutation category, such as Missense\_Mutation. |  
| Variant\_Type | VARCHAR(10) | NA | Variant type, such as SNP, DEL, or INS. |  
| Consequence | VARCHAR(100) | NA | Detailed predicted consequence of the variant. |  
| IMPACT | VARCHAR(10) | NA | Predicted functional impact, such as HIGH, MODERATE, LOW, or MODIFIER. |  
| SOMATIC | VARCHAR(25) | NA | Somatic mutation flag or status. |

\#\# Sequencing Quality

| Column | Recommended SQL Type | Key | Why / Description |  
|---|---|---|---|  
| sequencing\_evidence\_id | VARCHAR(20) | PK | Unique identifier for sequencing support evidence. |  
| mutation\_id | VARCHAR(20) | FK | Links sequencing evidence to the mutation. |  
| t\_depth | INT | NA | Total tumor read depth. |  
| t\_alt\_count | INT | NA | Tumor alternate read count. |  
| n\_depth | INT | NA | Total normal read depth. |  
| n\_alt\_count | INT | NA | Normal alternate read count. |  
| NCALLERS | TINYINT | NA | Number of variant callers supporting the mutation. |

\#\# Protein Annotation

| Column | Recommended SQL Type | Key | Why / Description |  
|---|---|---|---|  
| protein\_annotation\_id | VARCHAR(20) | PK | Unique identifier for each protein annotation record. |  
| mutation\_id | VARCHAR(20) | FK | Links protein annotation to the mutation. |  
| HGVSp | VARCHAR(50) | NA | Protein-level HGVS notation. |  
| Protein\_position | INT | NA | Amino acid position affected by the mutation. |  
| Amino\_acids | VARCHAR(30) | NA | Amino acid change caused by the mutation. |  
| Codons | VARCHAR(75) | NA | Codon change associated with the mutation. |  
| PolyPhen | VARCHAR(40) | NA | PolyPhen prediction for functional effect. |  
| SIFT | VARCHAR(40) | NA | SIFT prediction for functional effect. |  
| DOMAINS | TEXT | NA | Protein domain annotations. |

\#\# Transcript Annotation

| Column | Recommended SQL Type | Key | Why / Description |  
|---|---|---|---|  
| transcript\_annotation\_id | VARCHAR(20) | PK | Unique identifier for each transcript annotation record. |  
| mutation\_id | VARCHAR(20) | FK | Links transcript annotation to the mutation. |  
| Transcript\_ID | VARCHAR(20) | NA | Ensembl transcript identifier. |  
| RefSeq | VARCHAR(25) | NA | RefSeq transcript identifier. |  
| Feature | VARCHAR(20) | NA | Feature or transcript ID from the annotation file. |  
| EXON | VARCHAR(25) | NA | Exon number or exon range. |  
| INTRON | VARCHAR(25) | NA | Intron number or intron range. |  
| CDS\_position | VARCHAR(20) | NA | Coding sequence position; stored as text because ranges can occur. |  
| cDNA\_position | VARCHAR(25) | NA | cDNA coordinate; stored as text because ranges can occur. |  
| CANONICAL | VARCHAR(5) | NA | Indicates whether the transcript is canonical. |  
| CCDS | VARCHAR(20) | NA | Consensus coding sequence identifier. |  
| ENSP | VARCHAR(20) | NA | Ensembl protein identifier. |  
| SWISSPROT | VARCHAR(100) | NA | UniProt Swiss-Prot identifier. |  
| TREMBL | TEXT | NA | UniProt TrEMBL identifiers, which may be long. |  
| UNIPARC | VARCHAR(20) | NA | UniParc protein identifier. |  
| HGVS\_OFFSET | VARCHAR(5) | NA | HGVS offset value. |

\#\# External Variant Annotation

| Column | Recommended SQL Type | Key | Why / Description |  
|---|---|---|---|  
| external\_annotation\_id | VARCHAR(20) | PK | Unique identifier for each external annotation record. |  
| mutation\_id | VARCHAR(20) | FK | Links external annotation to the mutation. |  
| dbSNP\_RS | VARCHAR(50) | NA | dbSNP reference SNP identifier. |  
| COSMIC | TEXT | NA | COSMIC mutation identifiers. |  
| Existing\_variation | VARCHAR(200) | NA | Known variant IDs from external databases. |  
| CLIN\_SIG | VARCHAR(50) | NA | Clinical significance annotation. |  
| PUBMED | VARCHAR(25) | NA | PubMed IDs associated with the variant. |

\#\# Population Frequency

| Column | Recommended SQL Type | Key | Why / Description |  
|---|---|---|---|  
| population\_frequency\_id | VARCHAR(20) | PK | Unique identifier for each population frequency record. |  
| mutation\_id | VARCHAR(20) | FK | Links population frequency information to the mutation. |  
| GMAF | VARCHAR(25) | NA | Global minor allele frequency; stored as text because values may require later parsing. |  
| SAS\_MAF | VARCHAR(25) | NA | South Asian minor allele frequency; stored as text because values may require later parsing. |

\#\# Sequence Context

| Column | Recommended SQL Type | Key | Why / Description |  
|---|---|---|---|  
| sequence\_context\_id | VARCHAR(20) | PK | Unique identifier for each sequence context record. |  
| mutation\_id | VARCHAR(20) | FK | Links sequence context to the mutation. |  
| CONTEXT | VARCHAR(80) | NA | Local nucleotide sequence context around the mutation. |  
