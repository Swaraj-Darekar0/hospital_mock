# Mocked file upload module (demo only)
# Demonstrates NamedTemporaryFile usage and insecure upload directory patterns.

import tempfile

UPLOAD_DIR = '/tmp/medsecure_uploads'

def save_demo_file(filename):
    tmp = tempfile.NamedTemporaryFile(delete=False)
    tmp.write(b'demo')
    tmp.flush()
    return tmp.name
