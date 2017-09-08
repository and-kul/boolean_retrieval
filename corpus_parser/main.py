import argparse
import os
import re
import json
from typing import List

DEFAULT_PATH_TO_CORPUS_DIRECTORY = r"./Corpus"
DEFAULT_OUTPUT_FILE = r"./documents.json"
LISA_FILES = [
    "LISA0.001",
    "LISA0.501",
    "LISA1.001",
    "LISA1.501",
    "LISA2.001",
    "LISA2.501",
    "LISA3.001",
    "LISA3.501",
    "LISA4.001",
    "LISA4.501",
    "LISA5.001",
    "LISA5.501",
    "LISA5.627",
    "LISA5.850",
]


class Document:
    def __init__(self):
        self.id = 0
        self.title = None
        self.body = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "body": self.body
        }


def process_file(path: str) -> List[Document]:
    documents: List[Document] = []
    current_document_lines: List[str] = []
    with open(path, "r") as lisa_file:
        while True:
            line = lisa_file.readline()
            if not line:
                break
            if line.startswith("**********"):
                document = Document()
                document.id = int(current_document_lines[0].split()[1])
                sep_line = 0
                while not re.match(r"\s+", current_document_lines[sep_line]):
                    sep_line += 1
                document.title = " ".join([line.rstrip() for line in current_document_lines[1:sep_line]])
                document.body = " ".join([line.rstrip() for line in current_document_lines[sep_line + 1:]])
                documents.append(document)
                current_document_lines = []
            else:
                current_document_lines.append(line)
    return documents


def main():
    parser = argparse.ArgumentParser(description="parses the LISA collection of documents into one json file")
    parser.add_argument("--corpus", help='path to Corpus directory, default="' + DEFAULT_PATH_TO_CORPUS_DIRECTORY + '"',
                        default=DEFAULT_PATH_TO_CORPUS_DIRECTORY)
    parser.add_argument("--output",
                        help='where to store json with all documents, default="' + DEFAULT_OUTPUT_FILE + '"',
                        default=DEFAULT_OUTPUT_FILE)
    args = parser.parse_args()

    if not os.path.isdir(args.corpus):
        print('no directory "' + args.corpus + '" found')
        exit(1)

    documents = []
    for file in LISA_FILES:
        full_path = os.path.join(args.corpus, file)
        documents += process_file(full_path)

    documents_dict = [doc.to_dict() for doc in documents]
    with open(args.output, "wt") as output:
        json.dump(documents_dict, output)
    exit(0)


if __name__ == "__main__":
    main()
