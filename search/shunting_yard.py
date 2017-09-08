from typing import List
from operators import operators

class ParseError(Exception):
    def __init__(self, message=""):
        super().__init__(message)

for key in operators:
    operators[key]['symbol'] = key


def is_term(token: str):
    return token != "(" and token != ")" and token not in operators


class ShuntingYard:
    def __init__(self, tokens):
        self.tokens = tokens
        self.opstack: List[str] = []
        self.output: List[str] = []

    def get_RPN(self) -> List[str]:
        for token in self.tokens:
            self.handle_token(token)

        while self.opstack:
            token = self.opstack.pop()
            if token == "(":
                raise ParseError("Unbalanced parenthesis")
            self.output.append(token)

        return self.output


    def handle_token(self, token):
        if is_term(token):
            self.output.append(token)
            return
        if token in operators:
            op1 = operators[token]

            while len(self.opstack) > 0 and self.opstack[-1] in operators:
                op2 = operators[self.opstack[-1]]
                if (op1["assoc"] == "left" and op1["prec"] <= op2["prec"]) \
                        or (op1["assoc"] == "right" and op1["prec"] < op2["prec"]):
                    self.output.append(self.opstack.pop())
                else:
                    break
            self.opstack.append(token)
            return

        if token == "(":
            self.opstack.append(token)
            return

        if token == ")":
            try:
                while self.opstack[-1] != "(":
                    self.output.append(self.opstack.pop())
            except IndexError:
                raise ParseError("Unbalanced parenthesis")
            self.opstack.pop()
        pass
