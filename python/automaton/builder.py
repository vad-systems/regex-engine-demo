from typing import Dict, List, Set, Optional
from python.ast_parser.ast_nodes import ASTNode, Literal, Concatenation, Alternation, Star, CharacterGroup
from python.automaton.nfa import State, NFA

class NFABuilder:
    def __init__(self):
        self.state_counter = 0

    def _new_state(self) -> State:
        state = State(f"s{self.state_counter}")
        self.state_counter += 1
        return state

    def build(self, node: ASTNode) -> NFA:
        self.state_counter = 0
        return self._transform(node)

    def _transform(self, node: ASTNode) -> NFA:
        if isinstance(node, Literal):
            start = self._new_state()
            accept = self._new_state()
            start.add_transition(node.char, accept)
            return NFA(start, accept)
        elif isinstance(node, Concatenation):
            left = self._transform(node.left)
            right = self._transform(node.right)
            left.accept_state.add_transition(None, right.start_state)
            return NFA(left.start_state, right.accept_state)
        elif isinstance(node, Alternation):
            start = self._new_state()
            accept = self._new_state()
            left = self._transform(node.left)
            right = self._transform(node.right)
            start.add_transition(None, left.start_state)
            start.add_transition(None, right.start_state)
            left.accept_state.add_transition(None, accept)
            right.accept_state.add_transition(None, accept)
            return NFA(start, accept)
        elif isinstance(node, Star):
            start = self._new_state()
            accept = self._new_state()
            inner = self._transform(node.expression)
            start.add_transition(None, inner.start_state)
            start.add_transition(None, accept)
            inner.accept_state.add_transition(None, inner.start_state)
            inner.accept_state.add_transition(None, accept)
            return NFA(start, accept)
        elif isinstance(node, CharacterGroup):
            start = self._new_state()
            accept = self._new_state()
            for char in node.chars:
                start.add_transition(char, accept)
            return NFA(start, accept)
        
        raise ValueError(f"Unknown node type: {type(node)}")
