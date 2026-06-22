from automaton import NFAExecutor

def regex_test(pattern, str, parse_func=None, build_func=None):
    if parse_func is None:
        raise ValueError("Kein Parser übergeben")
    if build_func is None:
        raise ValueError("Keine NFA-Konstruktion übergeben")
    ast = parse_func(pattern)
    nfa = build_func(ast, [0])
    return NFAExecutor(nfa).execute(str)
