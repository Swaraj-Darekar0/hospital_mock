# Mocked DB access layer (demo only)
# Includes examples of raw SQL concatenation to trigger SQL injection heuristics.

def get_patient_query(mrn):
    return f"SELECT * FROM patients WHERE mrn = '{mrn}'"

# ...additional demo helpers...