import json

def add_find_exercise(notebook_path):
    with open(notebook_path, 'r') as f:
        data = json.load(f)

    new_cells = []
    
    # Define exercises to inject
    exercises = [
        ("a", "Find 'a' in 'banana'", "banana"),
        ("ab", "Find 'ab' in 'cabana'", "cabana"),
        ("a|b", "Find 'a' or 'b' in 'xyzb'", "xyzb"),
        ("a*", "Find 'a*' in 'baac'", "baac")
    ]
    
    exercise_idx = 0
    
    # Iterate and inject
    i = 0
    while i < len(data['cells']):
        new_cells.append(data['cells'][i])
        
        # Check if this cell is a "Teste dein Ergebnis" cell
        if data['cells'][i].get('cell_type') == 'code':
            source = data['cells'][i].get('source', [])
            source_text = "".join(source)
            if "regex_visualisieren" in source_text and exercise_idx < len(exercises):
                regex, comment, test_text = exercises[exercise_idx]
                
                # Create new cell
                new_cell = {
                    "cell_type": "code",
                    "metadata": {},
                    "source": [
                        f"# Teste dein Ergebnis mit find:\n",
                        f"nfa = nfa_bauen(regex_parsen(\"{regex}\"), [0])\n",
                        f"executor = NFAExecutor(nfa)\n",
                        f"print(f\"{comment}: {{executor.find('{test_text}')}}\")"
                    ],
                    "outputs": [],
                    "execution_count": None
                }
                new_cells.append(new_cell)
                exercise_idx += 1
        i += 1
        
    data['cells'] = new_cells
    
    with open(notebook_path, 'w') as f:
        json.dump(data, f, indent=1)

if __name__ == "__main__":
    add_find_exercise('python/thompson_construction.ipynb')
