Choosing limited data:

Under the constraints of time and memory, the reward of incorporating all data from all TCGA files would not be worth it. Therefore, I chose to keep the database conservative and only include columns with specific values to the goal of determining which mutations paired with the worst survival outcomes or most aggressive tumors. What data was excluded is in excludesDataRational.md

Normal form deviations:

Some of my tables are technically not in the 5th normal form as it combines many concepts. However, this data is guaranteed not to have multiple stagings per patient, as it's a database created from existing data and not continuously gathered data. Therefore, it is simpler to just make 1 table. 

Database structure:

The structure also prioritizes querying speed and simplicity over versatility for adding new information. I could’ve made more lookup tables and left some data as strings rather than binary for ease of understanding, but this database is intended for querying mutations and not adding more data. 