import json

def restore_and_order_notebook(notebook_path):
    with open(notebook_path, 'r') as f:
        data = json.load(f)
        
    # Manually re-order key components and inject exercises
    
    # Let's extract cells into a new ordered list
    ordered_cells = []
    
    # 1. Header/Imports/Setup
    for i in range(0, 4):
        ordered_cells.append(data['cells'][i])
    
    # 2. Add nfa_bauen definition early (so it's available for all find tests)
    # Looking at the original read, the nfa_bauen definition was around cell 188
    # Let's find it.
    
    # Find all code cells that define nfa_bauen or helper functions
    # Based on previous inspection, I need to find the cells that defined
    # neuer_zustand, nfa_bauen, literal_transformieren, etc.
    
    # To keep it simple and safe, I will just reconstruct the sequence of cells
    # from the content I have access to.
    
    # Re-reading the file, I see the cells are already there, just in a confusing order
    # I will just write a new JSON with the cells reordered.
    
    # Actually, I have the full content in the previous 'read' output.
    # I will construct the correct order in memory.
    
    print("Notebook structure looks complete, but order is wrong.")
    
    # I will just fix the imports/definitions issue.
    # The error 'NameError: name 'nfa_bauen' is not defined' confirms 
    # it's defined too late.
    
    # I will re-create the notebook with the correct order.
    
    # This is better done by just manually editing the file with write.
    # Given the size, I'll write a new file and then move it.

restore_and_order_notebook('python/thompson_construction.ipynb')
