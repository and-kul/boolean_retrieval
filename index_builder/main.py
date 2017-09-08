import argparse
import json
import string

from collections import defaultdict
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer

DEFAULT_DOCUMENTS_JSON = r"./documents.json"
DEFAULT_INDEX_JSON = r"./index.json"


def main():
    parser = argparse.ArgumentParser(description="builds an index file for documents")
    parser.add_argument("--input",
                        help='path to json with documents, default="' + DEFAULT_DOCUMENTS_JSON + '"',
                        default=DEFAULT_DOCUMENTS_JSON)
    parser.add_argument("--output",
                        help='where to store json with index, default="' + DEFAULT_INDEX_JSON + '"',
                        default=DEFAULT_INDEX_JSON)
    args = parser.parse_args()


    with open(args.input, "r") as json_file:
        documents = json.load(json_file)

    stemmer = SnowballStemmer("english")
    index = defaultdict(list)

    for document in documents:
        text = document["title"] + " " + document["body"]

        # without punctuation tokens
        raw_tokens = [token for token in word_tokenize(text) if token not in string.punctuation]

        terms = set()

        for token in raw_tokens:
            terms.add(stemmer.stem(token))

        for term in terms:
            index[term].append(document["id"])

    with open(args.output, "wt") as index_json_file:
        json.dump(index, index_json_file)
    exit(0)


if __name__ == '__main__':
    main()
