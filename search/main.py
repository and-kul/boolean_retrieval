import argparse
import json
from typing import List
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
from shunting_yard import ShuntingYard
from shunting_yard import is_term
from operators import operators

DEFAULT_DOCUMENTS_JSON = r"../index_builder/documents.json"
DEFAULT_INDEX_JSON = r"./index.json"


def perform_AND(left: List[int], right: List[int]) -> List[int]:
    l_pos = 0
    r_pos = 0
    result = []

    while l_pos < len(left) and r_pos < len(right):
        if left[l_pos] == right[r_pos]:
            result.append(left[l_pos])
            l_pos += 1
            r_pos += 1
        elif left[l_pos] < right[r_pos]:
            l_pos += 1
        else:
            r_pos += 1

    return result


def perform_OR(left: List[int], right: List[int]) -> List[int]:
    l_pos = 0
    r_pos = 0
    result = []

    while l_pos < len(left) or r_pos < len(right):
        if l_pos == len(left):
            result += right[r_pos:]
            break
        elif r_pos == len(right):
            result += left[l_pos:]
            break

        elif left[l_pos] == right[r_pos]:
            result.append(left[l_pos])
            l_pos += 1
            r_pos += 1
        elif left[l_pos] < right[r_pos]:
            result.append(left[l_pos])
            l_pos += 1
        else:
            result.append(right[r_pos])
            r_pos += 1

    return result


def perform_NOT(exclude: List[int], all_document_ids) -> List[int]:
    result = list(all_document_ids.difference(set(exclude)))
    result.sort()
    return result



def main():
    parser = argparse.ArgumentParser(description="search documents for specified queries")
    parser.add_argument("--documents",
                        help='path to json with documents, default="' + DEFAULT_DOCUMENTS_JSON + '"',
                        default=DEFAULT_DOCUMENTS_JSON)
    parser.add_argument("--index",
                        help='path to json with index, default="' + DEFAULT_INDEX_JSON + '"',
                        default=DEFAULT_INDEX_JSON)
    parser.add_argument("-v", "--verbose", help="show full text of LIMIT documents",
                        action="store_true")
    parser.add_argument("-l", "--limit", help="specify, how many documents to show with full text, default=5",
                        type=int,
                        default=5)
    args = parser.parse_args()


    with open(args.index, "r") as json_file:
        index = json.load(json_file)

    with open(args.documents, "r") as json_file:
        documents_list = json.load(json_file)

    all_document_ids = set([document["id"] for document in documents_list])
    all_documents = {
        document["id"]:
            {
                "title": document["title"],
                "body": document["body"]
            }
        for document in documents_list}

    stemmer = SnowballStemmer("english")

    print("Enter the search query, to exit type 'exit'")

    while True:
        query = input("> ")
        if query.lower() == "exit":
            break

        tokens = word_tokenize(query)

        i = 0
        while i < len(tokens) - 1:
            if is_term(tokens[i]) and is_term(tokens[i+1]):
                tokens.insert(i+1, "AND")
            i += 1

        # convert to Reverse Polish notation
        rpn = ShuntingYard(tokens).get_RPN()

        stack = []

        for token in rpn:
            if token not in operators:
                term = stemmer.stem(token)

                # get documents for term using index (or [] if term not found)
                documents = index[term] if term in index else []
                stack.append(documents)
            else:
                if token == "AND":
                    right_operand = stack.pop()
                    left_operand = stack.pop()
                    stack.append(perform_AND(left_operand, right_operand))
                elif token == "OR":
                    right_operand = stack.pop()
                    left_operand = stack.pop()
                    stack.append(perform_OR(left_operand, right_operand))
                elif token == "NOT":
                    operand = stack.pop()
                    stack.append(perform_NOT(operand, all_document_ids))

        print("Found", len(stack[0]), "documents:", stack[0])
        print("-" * 40)
        if args.verbose:
            limit = args.limit
            for document_id in stack[0]:
                if limit <= 0:
                    break
                document = all_documents[document_id]
                print("Document", document_id)
                print(document["title"])
                print()
                print(document["body"])
                print("-" * 40)
                limit -= 1


if __name__ == '__main__':
    main()
