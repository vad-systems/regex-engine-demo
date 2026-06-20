from python.ast_parser.parser import RegexParser
from python.automaton.builder import NFABuilder
from python.automaton.executor import NFAExecutor

def test_engine():
    # Test cases: (pattern, text, expected_match)
    test_cases = [
        ("a", "a", True),
        ("a", "b", False),
        ("ab", "ab", True),
        ("a|b", "a", True),
        ("a|b", "b", True),
        ("a*", "", True),
        ("a*", "aaa", True),
        ("a?b", "b", True),
        ("a?b", "ab", True),
        ("[a-c]d", "ad", True),
        ("[a-c]d", "bd", True),
        ("[a-c]d", "cd", True),
        ("[a-c]d", "dd", False),
    ]
    
    for pattern, text, expected in test_cases:
        try:
            ast = RegexParser(pattern).parse()
            nfa = NFABuilder().build(ast)
            executor = NFAExecutor(nfa)
            result = executor.execute(text)
            assert result == expected, f"Failed for {pattern} on {text}: expected {expected}, got {result}"
            print(f"Passed: {pattern} on {text}")
        except Exception as e:
            print(f"Failed with exception for {pattern} on {text}: {e}")

if __name__ == "__main__":
    test_engine()
