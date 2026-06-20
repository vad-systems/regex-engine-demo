from .nfa import NFA, State

def nfa_to_dot(nfa: NFA) -> str:
    dot = ["digraph NFA {", '  rankdir="LR";', '  node [shape=circle, fontname="Arial"];']
    
    visited = set()
    stack = [nfa.start_state]
    
    # Mark start and accept states
    dot.append(f'  "{nfa.start_state.name}" [label="{nfa.start_state.name}", color=blue];')
    dot.append(f'  "{nfa.accept_state.name}" [shape=doublecircle, label="{nfa.accept_state.name}", color=red];')

    while stack:
        state = stack.pop()
        if state in visited:
            continue
        visited.add(state)
        
        for transition in state.transitions:
            label = transition.char if transition.char is not None else "ε"
            dot.append(f'  "{state.name}" -> "{transition.target.name}" [label="{label}"];')
            if transition.target not in visited:
                stack.append(transition.target)
                
    dot.append("}")
    return "\n".join(dot)

def nfa_to_ascii(nfa: NFA) -> str:
    visited = set()
    stack = [nfa.start_state]
    lines = [f"Start: {nfa.start_state.name}", f"Accept: {nfa.accept_state.name}", "Transitions:"]
    
    while stack:
        state = stack.pop()
        if state in visited:
            continue
        visited.add(state)
        for transition in state.transitions:
            char = transition.char if transition.char is not None else "ε"
            lines.append(f"  {state.name} --{char}--> {transition.target.name}")
            if transition.target not in visited:
                stack.append(transition.target)
                
    return "\n".join(lines)
