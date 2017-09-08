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
It creates an inverted index for documents in **documents.json** and stores it in **index.json** (default name, could be changed). The structure of result:
```json
{
  "situat": [1, 3, 104  ],
  "serious": [1, 32, 88  ]

}
```
It uses SnowballStemmer from nltk for stemming.

## search


