from dataclasses import dataclass
from typing import Union, List


@dataclass
class ASTNode:
    pass


@dataclass
class Literal(ASTNode):
    char: str


@dataclass
class BinaryOp(ASTNode):
    left: ASTNode
    right: ASTNode
    pass


@dataclass
class Concatenation(BinaryOp):
    pass


@dataclass
class Alternation(BinaryOp):
    pass


@dataclass
class UnaryOp(ASTNode):
    expression: ASTNode


@dataclass
class Star(UnaryOp):
    pass


@dataclass
class Plus(UnaryOp):
    pass


@dataclass
class Optional(UnaryOp):
    pass


@dataclass
class Repetition(UnaryOp):
    min: int
    max: Union[int, None]


@dataclass
class CharacterGroup(ASTNode):
    chars: List[str]
