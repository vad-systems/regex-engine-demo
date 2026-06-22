
import sys
import os

# Add the 'python' directory to sys.path so we can import modules from it
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'python')))

from ast_parser.parser import regex_parsen
from automaton.builder import NFABuilder
from automaton.executor import NFAExecutor

builder = NFABuilder()

# Example 1: Log search
print("--- Log Search (finding 'INFO') ---")
with open('data/logs.txt', 'r') as f:
    for line in f:
        ast = regex_parsen("INFO")
        nfa = builder.build(ast)
        executor = NFAExecutor(nfa)
        if executor.find(line):
            print(f"Found 'INFO' in: {line.strip()}")

# Example 2: Email Validation (simplified, checking for '@')
print("\n--- Email Validation (checking for '@') ---")
with open('data/users.csv', 'r') as f:
    next(f) # skip header
    for line in f:
        username, email = line.strip().split(',')
        ast = regex_parsen("@")
        nfa = builder.build(ast)
        executor = NFAExecutor(nfa)
        if not executor.find(email):
            print(f"Invalid email found: {email} for user {username}")

# Example 3: Data extraction (finding user1)
print("\n--- Data Extraction (finding 'user1') ---")
with open('data/logs.txt', 'r') as f:
    for line in f:
        ast = regex_parsen("user1")
        nfa = builder.build(ast)
        executor = NFAExecutor(nfa)
        if executor.find(line):
            print(f"User1 mentioned in: {line.strip()}")
