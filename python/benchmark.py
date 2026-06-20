import time
import re
from python.automaton.builder import NFABuilder
from python.automaton.executor import NFAExecutor
from python.ast_parser.parser import RegexParser

def benchmark():
    # Catastrophic backtracking pattern: a*a
    pattern = "a*a" * 5
    text = "a" * 10000 
    
    # Python re
    start = time.time()
    re.match(pattern, text)
    print(f"Python re: {time.time() - start:.6f}s")
    
    # Our engine
    ast = RegexParser(pattern).parse()
    nfa = NFABuilder().build(ast)
    executor = NFAExecutor(nfa)
    start = time.time()
    executor.execute(text)
    print(f"Our engine: {time.time() - start:.6f}s")

if __name__ == "__main__":
    benchmark()
