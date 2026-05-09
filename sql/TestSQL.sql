--Check whether every sample connects to a patient
SELECT
    s.SAMPLE_ID,
    s.PATIENT_ID
FROM Sample s
LEFT JOIN Patient p
    ON s.PATIENT_ID = p.PATIENT_ID
WHERE p.PATIENT_ID IS NULL;

--should return null

--Check whether every mutation connects to a sample
SELECT
    m.mutation_id,
    m.sample_id
FROM Mutation_Info m
LEFT JOIN Sample s
    ON m.sample_id = s.SAMPLE_ID
WHERE s.SAMPLE_ID IS NULL;

--should return null

-- Show first 25 mutations with gene names and sample IDs
SELECT
    m.mutation_id,
    m.sample_id,
    g.Hugo_Symbol,
    m.Chromosome,
    m.Start_Position,
    m.Variant_Classification,
    m.IMPACT
FROM Mutation_Info m
JOIN Gene_Info g
    ON m.gene_ID = g.gene_ID
LIMIT 25;

-- Count mutations per gene
SELECT
    g.Hugo_Symbol,
    COUNT(m.mutation_id) AS mutation_count
FROM Gene_Info g
JOIN Mutation_Info m
    ON g.gene_ID = m.gene_ID
GROUP BY g.Hugo_Symbol
ORDER BY mutation_count DESC
LIMIT 20;

-- More complex: patient outcomes linked to sample mutation burden
SELECT
    p.PATIENT_ID,
    p.OS_STATUS,
    p.OS_MONTHS,
    COUNT(DISTINCT s.SAMPLE_ID) AS sample_count,
    COUNT(m.mutation_id) AS mutation_count
FROM Patient p
JOIN Sample s
    ON p.PATIENT_ID = s.PATIENT_ID
LEFT JOIN Mutation_Info m
    ON s.SAMPLE_ID = m.sample_id
GROUP BY
    p.PATIENT_ID,
    p.OS_STATUS,
    p.OS_MONTHS
ORDER BY mutation_count DESC
LIMIT 25;

--now to test what mutations have poor outcomes
-- Mutations linked to worst overall survival
SELECT
    m.mutation_id,
    g.Hugo_Symbol,
    m.Variant_Classification,
    m.IMPACT,
    m.sample_id,
    s.PATIENT_ID,
    p.OS_STATUS,
    p.OS_MONTHS,
    p.DSS_STATUS,
    p.DFS_STATUS,
    p.PFS_STATUS
FROM Mutation_Info m
JOIN Sample s
    ON m.sample_id = s.SAMPLE_ID
JOIN Patient p
    ON s.PATIENT_ID = p.PATIENT_ID
LEFT JOIN Gene_Info g
    ON m.gene_ID = g.gene_ID
WHERE p.OS_STATUS = 1
ORDER BY p.OS_MONTHS ASC;

-- High-impact mutations in patients with poor survival
SELECT
    m.mutation_id,
    g.Hugo_Symbol,
    m.IMPACT,
    m.Consequence,
    m.Variant_Classification,
    s.PATIENT_ID,
    p.OS_STATUS,
    p.OS_MONTHS
FROM Mutation_Info m
JOIN Sample s
    ON m.sample_id = s.SAMPLE_ID
JOIN Patient p
    ON s.PATIENT_ID = p.PATIENT_ID
LEFT JOIN Gene_Info g
    ON m.gene_ID = g.gene_ID
WHERE p.OS_STATUS = 1
  AND p.OS_MONTHS <= 24
  AND m.IMPACT IN ('HIGH', 'MODERATE')
ORDER BY p.OS_MONTHS ASC;

-- Genes whose mutations appear most often in poor-outcome patients
SELECT
    g.Hugo_Symbol,
    COUNT(DISTINCT m.mutation_id) AS mutation_count,
    COUNT(DISTINCT p.PATIENT_ID) AS affected_patient_count,
    AVG(p.OS_MONTHS) AS avg_os_months,

    GROUP_CONCAT(DISTINCT m.mutation_id ORDER BY m.mutation_id SEPARATOR ', ') AS mutation_ids

FROM Mutation_Info m
JOIN Sample s
    ON m.sample_id = s.SAMPLE_ID
JOIN Patient p
    ON s.PATIENT_ID = p.PATIENT_ID
LEFT JOIN Gene_Info g
    ON m.gene_ID = g.gene_ID

WHERE p.OS_STATUS = 1

GROUP BY g.Hugo_Symbol

ORDER BY affected_patient_count DESC, avg_os_months ASC;