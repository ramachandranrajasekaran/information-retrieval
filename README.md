# Information Retrieval Mini Projects
 
Part 1
**********************

Sub-Folder: AI
Wiki File: wiki_00

Usage:
------

- Extract the Part1.zip file
- Go to Part1 folder
- Place the wiki_xx files in to the wikifiles folder
- Run the Code.py file

Output:
Before Stemming:
- Total unique n-grams
- Most frequent n-grams required to cover the 90% of the complete corpus
- Plotted graph log(rank) vs log(frequency)

After Stemming:
- Total unique n-grams
- Most frequent n-grams required to cover the 90% of the complete corpus
- Plotted graph log(rank) vs log(frequency)


The graphs will be available in the "output" directory after the script execution is completed.

Below is the sample output,
Unique 1-grams: 79122
Most frequent 1-grams required to cover the 90% of the complete corpus: 41165
After Stemming: Unique 1-grams: 64349
After Stemming: Most frequent 1-grams required to cover the 90% of the complete corpus: 28058
Unique 2-grams: 593325
Most frequent 2-grams required to cover the 90% of the complete corpus: 524385
After Stemming: Unique 2-grams: 565969
After Stemming: Most frequent 2-grams required to cover the 90% of the complete corpus: 497870
Unique 3-grams: 708385
Most frequent 3-grams required to cover the 90% of the complete corpus: 635810
After Stemming: Unique 3-grams: 705860
After Stemming: Most frequent 3-grams required to cover the 90% of the complete corpus: 633365

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Part 2:
***********************
Sub-Folder: AI
Wiki File: wiki_00

Usage:
------

Creating Inverted Indexing
==========================
- Extrace the Part2.zip
- Go to Part2 directory
- Place the wiki_xx file inside the 'wikifiles' folder
- Run the index.py file

Output:
- The data folder will be created containing
    * The "docs" folder will be created with the document content with file name as document numbers
	* The list of all documents name and inverted index serialized into "docs.pickle" and "inverted_index.pickle" files

- Once the index.py file execution is completed, run the query.py script
- That script will ask for queny input from the user
- Once the search query is provided, the result will as below (sample output)

Enter the query: football championship
----- Results ------ 
Document Title # - Score
Document Title 3436     0.250261009396306
Document Title 3043     0.23821986655156396
Document Title 3547     0.2362233017254259
Document Title 577      0.23304891874280642
Document Title 1299     0.23090395159805607
Document Title 5010     0.2266996170826005
Document Title 323      0.218869586769168
Document Title 3927     0.21242494219869185
Document Title 3045     0.20905026791642842
Document Title 3075     0.19474877225418724