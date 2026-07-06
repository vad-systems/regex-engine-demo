from dataclasses import dataclass, field
from typing import List, Tuple, Optional, Set


@dataclass
class Transition:
    char: Optional[str]  # None for epsilon transition
    target: 'State'


class State:
    def __init__(self, name: str):
        self.name = name
        self.transitions: List[Transition] = []

    def add_transition(self, char: Optional[str], target: 'State'):
        self.transitions.append(Transition(char, target))


@dataclass
class NFA:
    start_state: State
    accept_state: State
