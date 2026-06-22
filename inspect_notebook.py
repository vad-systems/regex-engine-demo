import json

def repair_notebook(notebook_path):
    with open(notebook_path, 'r') as f:
        data = json.load(f)

    # 1. Extract all code cells
    code_cells = [cell for cell in data['cells'] if cell.get('cell_type') == 'code']
    
    # 2. Re-organize content
    # Setup cell (imports + helper functions)
    # The actual implementation steps + exercise cells
    
    # This is a bit complex for a script. 
    # Let's just read and print the cells to see the current broken structure
    for i, cell in enumerate(data['cells']):
        if cell.get('cell_type') == 'code':
            source = "".join(cell.get('source', []))
            print(f"Cell {i} (code):")
            print(source[:50] + "...")
            print("-" * 20)

repair_notebook('python/thompson_construction.ipynb')
