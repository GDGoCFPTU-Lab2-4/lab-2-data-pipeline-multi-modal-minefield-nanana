import ast
import re

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Extract docstrings and comments from legacy Python code.

def extract_logic_from_code(file_path):
    # --- FILE READING (Handled for students) ---
    with open(file_path, 'r', encoding='utf-8') as f:
        source_code = f.read()
    # ------------------------------------------
    
    tree = ast.parse(source_code)
    docstrings = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            ds = ast.get_docstring(node)
            if ds:
                docstrings.append(f"Function {node.name}: {ds.strip()}")
    
    # Find business rules in comments and docstrings
    rules = re.findall(r"(?:# )?Business Logic Rule \d+.*", source_code)
    
    content = "extracted_docstrings: " + " | ".join(docstrings)
    content += "\n\nextracted_rules: " + " | ".join(rules)
    content += "\n\nraw_source_for_qa: " + source_code
    
    return {
        "document_id": "code-legacy-pipeline",
        "content": content,
        "source_type": "Code",
        "author": "Senior Dev (retired)",
        "timestamp": None,
        "source_metadata": {
            "file_path": file_path,
            "function_count": len([n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]),
            "rules_found": rules
        }
    }

