1. Remove excluded files and columns from raw data as described in excludedData\_Rational.md file  
2. Clean data using scripts in the data cleaning folder, labeled according to corresponding file. CheckSimilarities.py and CheckUniqueInfo.py was part of determining what columns to exclude, no need to run.   
3. [CreateSQL.py](http://CreateSQL.py) run to create our DB\_upload folder in SQL. Can be skipped and go straight to import each file in DB\_upload in numerical order.  
4. TestSQL.sql is used to check the function of our database and ensure that everything joins correctly. 