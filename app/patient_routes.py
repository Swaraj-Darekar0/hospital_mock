# Mocked patient routes (demo only)
# Demonstrates PHI handling, render_template_string usage, and logging of PHI for analyzer evidence.

from flask import Blueprint, request, jsonify, render_template_string

patient_bp = Blueprint('patient', __name__)

@patient_bp.route('/lookup/<mrn>')
def lookup(mrn):
    # demo: no access control in mocked route
    template = f"<div>Patient MRN: {mrn}</div>"
    return render_template_string(template)
