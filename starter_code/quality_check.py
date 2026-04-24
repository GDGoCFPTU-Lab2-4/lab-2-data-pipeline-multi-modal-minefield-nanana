# ==========================================
# ROLE 3: OBSERVABILITY & QA ENGINEER
# ==========================================
# Task: Implement quality gates to reject corrupt data or logic discrepancies.

def run_quality_gate(document_dict: dict) -> bool:
    content = document_dict.get('content', '')
    
    # Reject documents with 'content' length < 20 characters
    if len(content) < 20:
        print(f"Rejecting {document_dict.get('document_id')}: content too short.")
        return False
        
    # Reject documents containing toxic/error strings
    error_keywords = ['Null pointer exception', 'Segmentation fault', 'Access denied']
    for kw in error_keywords:
        if kw.lower() in content.lower():
            print(f"Rejecting {document_dict.get('document_id')}: found error/toxic string '{kw}'.")
            return False
            
    # Flag discrepancies (e.g., if tax calculation comment says 8% but code says 10%)
    # Simple heuristic for the legacy code example
    if '8%' in content and '0.10' in content:
        print(f"Flagging {document_dict.get('document_id')}: Tax rate discrepancy detected (8% vs 0.10).")
        # Depending on requirements, this could return False or just log. 
        # The TODO says "Flag", usually in a gate it means reject or mark. 
        # I'll reject it for the purpose of the lab.
        return False

    return True
