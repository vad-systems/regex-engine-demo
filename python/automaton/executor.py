from typing import Set
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

    def match(self, text: str) -> bool:
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

    def execute(self, text: str) -> bool:
        # Keep execute as an alias to match for backward compatibility
        return self.match(text)

    def find(self, text: str) -> bool:
        for i in range(len(text) + 1):
            current_states = self.epsilon_closure({self.nfa.start_state})

            # Check for empty string match
            if self.nfa.accept_state in current_states:
                return True

            for j in range(i, len(text)):
                char = text[j]
                next_states = set()
                for state in current_states:
                    for transition in state.transitions:
                        if transition.char == char:
                            next_states.add(transition.target)
                current_states = self.epsilon_closure(next_states)

                if self.nfa.accept_state in current_states:
                    return True

                if not current_states:
                    break

        return False
