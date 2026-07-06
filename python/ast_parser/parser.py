from typing import Callable, List, Optional, Type
from .ast_nodes import Literal, Concatenation, Alternation, ASTNode


class RegexParser:
    def __init__(self, pattern: str):
        self.pattern = pattern
        self.pos = 0

        # Extensibility points
        self.postfix_handlers = {}
        self.atom_handlers: List[Callable[['RegexParser'], Optional[ASTNode]]] = [
            lambda p: p._handle_escape(),
            lambda p: p._handle_parentheses()
        ]

    def peek(self) -> Optional[str]:
        return self.pattern[self.pos] if self.pos < len(self.pattern) else None

    def consume(self) -> Optional[str]:
        char = self.peek()
        if char:
            self.pos += 1
        return char

    def parse(self) -> ASTNode:
        return self.parse_expression()

    def parse_expression(self) -> ASTNode:
        node = self.parse_term()
        while self.peek() == '|':
            self.consume()
            right = self.parse_term()
            node = Alternation(node, right)
        return node

    def parse_term(self) -> ASTNode:
        node = self.parse_factor()
        while self.peek() and self.peek() != ')' and self.peek() != '|':
            right = self.parse_factor()
            node = Concatenation(node, right)
        return node

    def parse_factor(self) -> ASTNode:
        node = self.parse_atom()
        while True:
            char = self.peek()
            if char and char in self.postfix_handlers:
                self.consume()
                node = self.postfix_handlers[char](node)
            else:
                break
        return node

    def parse_atom(self) -> ASTNode:
        # Try registered atom handlers first
        for handler in self.atom_handlers:
            result = handler(self)
            if result:
                return result

        # Fallback to literal
        char = self.consume()
        if char is None:
            raise ValueError("Unexpected end of pattern")
        return Literal(char)

    def _handle_parentheses(self) -> Optional[ASTNode]:
        if self.peek() == '(':
            self.consume()
            node = self.parse_expression()
            if self.consume() != ')':
                raise ValueError("Expected ')'")
            return node
        return None

    def _handle_escape(self) -> Optional[ASTNode]:
        if self.peek() == '\\':
            self.consume()  # consume '\'
            char = self.consume()
            if char is None:
                raise ValueError("Trailing backslash at end of pattern")
            return Literal(char)
        return None


def regex_parsen(pattern: str) -> ASTNode:
    parser = RegexParser(pattern)
    return parser.parse()
