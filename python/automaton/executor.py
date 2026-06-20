from typing import Set, Optional
from .nfa import State, NFA

class NFAExecutor:
    def __init__(self, nfa: NFA):
        self.nfa = nfa

    def epsilon_closure(self, states: Set[State]) -> Set[State]:
        closure = set(states)
        stack = list(states)
        while stack:
            state = stack.pop()
            for transition in state.transitions:
                if transition.char is None and transition.target not in closure:
                    closure.add(transition.target)
                    stack.append(transition.target)
        return closure

    def execute(self, text: str) -> bool:
        current_states = self.epsilon_closure({self.nfa.start_state})
        
        for char in text:
            next_states = set()
            for state in current_states:
                for transition in state.transitions:
                    if transition.char == char:
                        next_states.add(transition.target)
            current_states = self.epsilon_closure(next_states)
            if not current_states:
                return False
        
        return self.nfa.accept_state in current_states
