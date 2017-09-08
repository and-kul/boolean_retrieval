# Information Retrieval. Assignment 1

I’ve decided to use Python 3.6 as a programming language. 
If you only have interpreter for Python 2.7, please install the [Python 3.6](https://www.python.org/downloads/release/python-362/)
because I could not guarantee backward compatibility. Please note that I will use `python3` and `pip3` to emphasize used version,
but if Python 3 is your default, you should use just `python` and `pip` instead.

## NLTK installation
Skip this section if you already have *NLTK* installed and *NLTK Data* downloaded

You need to install [nltk](http://www.nltk.org/) for tokenization and stemming. You can do it via pip:
```
sudo pip3 install -U nltk
```
Then you have to download *NLTK Data*, the easiest way to do it is using interactive installer:
```
python3
```
```python
>>> import nltk
>>> nltk.download()
```

## Document collection
I use suggested LISA document collection, but there was one issue with this Corpus. The problem was inside **LISA1.501** file:
After *Document 1992* and until the late *Document 1998* there was a mess: repetition of previous documents, missed document ids...
So I’ve decided to remove everything in-between. In the **corpus_parser/Corpus** directory there is a fixed version.

## Structure
There are 3 subprojects in this repository, each responsible for different thing:
1. **corpus_parser**
2. **index_builder**
3. **search**

You can run each through `python3 main.py` and see nice help using `python3 main.py -h` (there you can discover, for example, what arguments to use for changing default filenames)

## corpus_parser
This subproject parses raw LISA collection of documents into one **documents.json** (default name, could be changed) with the following structure:
```json
[
{ "id": 1, "title": "...", "body": "..."},
{ "id": 2, "title": "...", "body": "..."},

]
```

## index_builer
It creates an inverted index for documents from **documents.json** and stores it in **index.json** (default name, could be changed). The structure of result:
```json
{
  "situat": [1, 3, 104  ],
  "serious": [1, 32, 88  ],

}
```
It uses *SnowballStemmer* from *nltk* for stemming.

## search
The most interesting part. This simple search engine performs boolean retrieval of documents from **documents.json** using **index.json**. Use `AND`, `OR` and `NOT`(case sensitive) for corresponding boolean operations. Examples will help you understand how to use it:
```
PS C:\workspace\boolean_retrieval\search> python3 main.py
Enter the search query, to exit type 'exit'
> information AND boolean AND retrieval
Found 6 documents: [1399, 2903, 3398, 3400, 3445, 4899]
----------------------------------------
> science AND (article OR paper) AND NOT history
Found 93 documents: [15, 96, 251, 257, 304, 332, 494, 498, 502, 503, 632, 730, 733, 734, 745, 772, 773, 1010, 1033, 1042, 1193, 1241, 1412, 1594, 1623, 1645, 1697, 1734, 1739, 2015, 2016, 2020, 2022, 2039, 2049, 2207, 2226, 2247, 2269, 2270, 2300, 2358, 2365, 2517, 2519, 2522, 2745, 2757, 2891, 3093, 3379, 3387, 3442, 3498, 3519, 3527, 3528, 3762, 3883, 3971, 3995, 4278, 4289, 4316, 4350, 4352, 4357, 4419, 4470, 4650, 4664, 4719, 4778, 4803, 4824, 4829, 4984, 4990, 4994, 5025, 5206, 5304, 5305, 5306, 5430, 5505, 5507, 5510, 5527, 5530, 5641, 5798, 6000]
----------------------------------------
> exit
```
You can add `--verbose` argument to actually show found documents. Argument `--limit` limits results shown in full text (default is 5):
```
PS C:\workspace\boolean_retrieval\search> python3 main.py --verbose --limit=3
Enter the search query, to exit type 'exit'
> information AND boolean AND retrieval
Found 6 documents: [1399, 2903, 3398, 3400, 3445, 4899]
----------------------------------------
Document 1399
THEORETICAL APPROACHES TO INFORMATION RETRIEVAL.

PRESENTS THE RESULTS OF RESEARCH CONDUCTED DURING A VISITING FELLOWSHIP, MAR 80-MAR 81, ON THE FOLLOWING TOPICS' RETRIEVAL METHODS OF DOCUMENTS INDEXED BY WEIGHTED INDEX TERMS; SIMILARITY MEASURES FOR BOOLEAN SEARCH REQUEST FORMULATIONS AND THEIR APPLICATIONS; DOCUMENT-CLUSTERING-BASED INFORMATION RETRIEVAL AND DOCUMENT CLUSTERING UTILISING PREVIOUSLY FORMED QUERY CLUSTERS; AND A PROBABILISTIC APPROACH TO INFORMATION RETRIEVAL IN SYSTEMS WITH BOOLEAN SEARCH REQUEST FORMULATIONS. A NUMBER OF INFORMATION RETRIEVAL TECHNIQUES APPLICABLE IN SYSTEMS BASED ON BOOLEAN SEARCHES HAVE BEEN INTRODUCED. SPECIAL ATTENTION HAS BEEN PAID TO INCORPORATE INTO THE STANDARD BOOLEAN RETRIEVAL SCHEMES A WEIGHTING MECHANISM TO PRODUCE RANKED LISTS OF DOCUMENTS. SEVERAL ALTERNATIVE APPROACHES HAVE BEEN OFFERED WHICH ARE BASED ON RESULTS OF FUZZY SET THEORY AND FUZZY LOGIC, PROBABILITY THEORY AND DECISION ANALYSIS, AND THE THEORY OF BOOLEAN FUNCTIONS.
----------------------------------------
Document 2903
A GENERAL MODEL OF QUERY PROCESSING IN INFORMATION RETRIEVAL SYSTEMS.

MOST CURRENT DOCUMENT RETRIEVAL SYSTEMS REQUIRE THAT USER QUERIES BE SPECIFIED IN THE FORM OF BOOLEAN EXPRESSIONS. ALTHOUGH BOOLEAN QUERIES WORK, THEY HAVE FLAWS. SOME OF THE ATTEMPTS TO OVERCOME THESE FLAWS HAVE INVOLVED 'PARTIAL-MATCH' RETRIEVAL OR THE USE OF FUZZY-SUBSET THEORY. RECENTLY, SOME GENERALISATIONS OF FUZZY-SUBSET THEORY HAVE BEEN SUGGESTED THAT WOULD ALLOW THE USER TO SPECIFY QUERIES WITH RELEVANCE WEIGHTS OR THRESHOLDS ATTACHED TO TERMS. THE VARIOUS QUERY-PROCESSING METHODS ARE DISCUSSED AND COMPARED.
----------------------------------------
Document 3398
A MODEL OF A DOCUMENT-CLUSTERING-BASED INFORMATION RETRIEVAL SYSTEM WITH A BOOLEAN SEARCH REQUEST FORMULATION.

PRESENTS AN INFORMATION RETRIEVAL METHOD WHICH CLUSTERS DOCUMENTS ON THE BASIS OF PREVIOUSLY DETERMINED CLUSTERS OF BOOLEAN SEARCH REQUEST FORMULATIONS. SUGGESTS WAYS OF SELECTING THESE FORMULATIONS AND DISCUSSES THE INFLUENCE OF SELECTION METHOD ON RETRIEVAL EFFECTIVENESS. SPECIAL ATTENTION IS PAID TO THE METHOD WHICH PROVIDES RETRIEVAL EFFECTIVENESS COMPARABLE TO THAT OBTAINED WITH A SEQUENTIAL FILE. THEORETICAL CONSIDERATIONS ARE ILLUSTRATED BY A NUMERICAL EXAMPLE.
----------------------------------------
> exit
```
Please, note that if you don't separate search terms, by default the `AND` operation will be applied on them. So the query `information boolean retrieval` is the same as `information AND boolean AND retrieval`.

For stemming again *SnowballStemmer* is used. To parse boolean query Shunting Yard algorithm is used to convert the expression into Reverse Polish notation. The complexity of `AND` and `OR` operations is *O(X + Y)* where *X*, *Y* - lengths of found document lists. For `NOT` operation complexity is *O(N)* where *N* - total number of documents.

## Screenshots
To see working functionality, check out **Screenshots** directory
