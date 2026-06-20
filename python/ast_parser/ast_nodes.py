from dataclasses import dataclass
from typing import Union, List

@dataclass
class ASTNode:
    pass

@dataclass
class Literal(ASTNode):
    char: str

@dataclass
class Concatenation(ASTNode):
    left: ASTNode
    right: ASTNode

@dataclass
class Alternation(ASTNode):
    left: ASTNode
    right: ASTNode

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
