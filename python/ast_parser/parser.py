from typing import Callable, List, Optional, Dict
from .ast_nodes import Literal, Concatenation, Alternation, ASTNode


class RegexParser:
    def __init__(self, pattern: str):
        self.pattern = pattern
        self.pos = 0

        # Extensibility points
        self.postfix_handlers: Dict[str, Callable[[ASTNode], ASTNode]] = {}
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

    def parse(self) -> Optional[ASTNode]:
        return self.parse_expression()

    def parse_expression(self) -> Optional[ASTNode]:
        # Alternation: expression | expression
        node = self.parse_term()
        while self.peek() == '|':
            self.consume()
            right = self.parse_term()
            node = Alternation(node, right)
        return node

    def parse_term(self) -> Optional[ASTNode]:
        # Concatenation: factor factor ...
        nodes = []
        while True:
            char = self.peek()
            if char is None or char == '|' or char == ')':
                break
            node = self.parse_factor()
            if node:
                nodes.append(node)
        
        if not nodes:
            return None
            
        result = nodes[0]
        for next_node in nodes[1:]:
            result = Concatenation(result, next_node)
        return result

    def parse_factor(self) -> Optional[ASTNode]:
        # Atom followed by optional postfix operators
        node = self.parse_atom()
        if node is None:
            return None
            
        while True:
            char = self.peek()
            if char is not None and char in self.postfix_handlers:
                self.consume()
                node = self.postfix_handlers[char](node)
            else:
                break
        return node

    def parse_atom(self) -> Optional[ASTNode]:
        # Try registered atom handlers first
        for handler in self.atom_handlers:
            result = handler(self)
            if result:
                return result

        # Fallback to literal
        char = self.consume()
        if char is None or char == '|' or char == ')':
            # If we reached EOF or separator, this atom is empty
            if char: self.pos -= 1 # Put it back if it was a separator
            return None
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


def regex_parsen(pattern: str) -> Optional[ASTNode]:
    parser = RegexParser(pattern)
    return parser.parse()
