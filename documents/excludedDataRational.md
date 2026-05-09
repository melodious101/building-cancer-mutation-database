**What data wasn’t included in the database:**

Overall files:  
data\_rppa → Reverse-Phase Protein Array data would be useful for quantifying the protein-level consequences of genetic mutations, but too complicated for the scope of our database’s goal  
data\_rppa\_zscores → same reason as above  
data\_gene\_panel\_matrix → includes Genomic Identification of Significant Targets in Cancer (GISTIC) data, but shows the same answer for all samples, making it \#repetitive  
data\_mrna\_seq\_v2\_rsem → records z-score for RNA Seq V2 RSEM compared to the expression, the distribution of each gene tumors that are diploid for this gene, too complicated for the scope of our database’s goal  
data\_mrna\_seq\_v2\_rsem\_zscores\_ref\_normal\_samples → same as above  
data\_mrna\_seq\_v2\_rsem\_zscores\_ref\_all\_samples → same as above   
data\_timeline\_sample\_aquisition → unnecessary for mutation analysis \#superfluous  
data\_resource\_definition → doesn’t store any information  
data\_cna → copy number alteration would be useful, but too complicated for the scope of our database

data\_mutations file:

SYMBOL → same data as ENTREZ\_SYMBOL \#redundant  
GENE → same data as ENSEMBL ID \#redundant  
EXON\_NUMBER → same data as EXON \#redundant  
VARIANT\_CLASS → same data as VARIANT\_TYPE \#redundant  
HGVSc → same data as transcript id \+ position \+ HGVSp \#redundant  
HGVSp\_Short → same data as HGVSc \#redundant  
DBVS → unclear meaning, unnecessary data \#vague  
Distance → unclear meaning, unnecessary data, more than 95% data is unknown \#vague  
CENTER→ shows where the mutation was pulled from, unnecessary for purpose of DB \#superfluous  
FILTER → all failed mutations were already filtered out so we don’t need to know why it passed \#superfluous  
All population genetic information other than global → not needed for our analysis \#superfluous  
Center → duplicate of CENTERS \#redundant  
NCBI\_Build → all data the same or unknown \#repetitive  
Strand → all data the same or unknown \#repetitive  
dbSNP\_Val\_Status → all data the same or unknown \#repetitive  
Tumor\_Validation\_Allele1 → all data the same or unknown \#repetitive  
Tumor\_Validation\_Allele2 → all data the same or unknown \#repetitive  
Match\_Norm\_Validation\_Allele1 → all data the same or unknown \#repetitive  
Match\_Norm\_Validation\_Allele2 → all data the same or unknown \#repetitive  
Verification\_Statusn→ all data the same or unknown \#repetitive  
Validation\_Status → all data the same or unknown \#repetitive  
Mutation\_Status → all data the same or unknown \#repetitive  
Sequencing\_Phase → all data the same or unknown \#repetitive  
Sequence\_Source → all data the same or unknown \#repetitive  
Validation\_Method → all data the same or unknown \#repetitive  
Score → all data the same or unknown \#repetitive  
BAM\_File → all data the same or unknown \#repetitive  
Sequencer → all data the same or unknown \#repetitive  
MOTIF\_NAME → all data the same or unknown \#repetitive   
MOTIF\_POS → all data the same or unknown \#repetitive  
MOTIF\_SCORE\_CHANGE → all data the same or unknown \#repetitive  
T\_ref\_count → can be inferred from t\_depth \- t\_alt\_count \#redundant  
N\_ref\_count → can be inferred from n\_depth \- n\_alt\_count \#redundant

data\_clinical\_sample file:

Tissue Source Site → not needed for our analysis \#superfluous

data\_clinical\_patient\_file:

OTHER\_PATIENT\_ID → duplicate patient identifier, same data as PATIENT\_ID \#redundant  
FORM\_COMPLETION\_DATE → administrative metadata, not relevant to mutation–outcome analysis \#superfluous  
INFORMED\_CONSENT\_VERIFIED → administrative field, no impact on biological or clinical outcomes \#superfluous  
IN\_PANCANPATHWAYS\_FREEZE → dataset-specific flag, not relevant to analysis \#superfluous  
ICD\_10 → same disease information as cancer subtype/staging fields \#redundant  
ICD\_O\_3\_HISTOLOGY → same tumor classification as subtype/staging fields \#redundant  
ICD\_O\_3\_SITE → same tumor site information as subtype/acronym \#redundant  
CANCER\_TYPE\_ACRONYM → all rows have same value (THCA) \#repetitive  
SUBTYPE → all rows have same value (THCA) \#repetitive  
AJCC\_STAGING\_EDITION → version metadata, staging already captured in T/N/M fields \#superfluous  
DAYS\_TO\_INITIAL\_PATHOLOGIC\_DIAGNOSIS → redundant with derived clinical time variables \#redundant  
DAYS\_TO\_BIRTH → redundant with AGE \#redundant  
DAYS\_LAST\_FOLLOWUP → redundant with OS/PFS/DSS time variables \#redundant  
DSS\_MONTHS → same data as DSF\_MONTHS \#redundant  
