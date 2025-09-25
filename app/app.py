# Mocked Flask app entrypoint (demo only)
# Contains illustrative comments and a few insecure placeholders to trigger analyzers.

from flask import Flask

app = Flask(__name__)

# NOTE: In the demo this value is intentionally obvious to trigger HARDCODED-SECRET findings
app.config['SECRET_KEY'] = 'demo_hospital_secret'

@app.route('/')
def index():
    return {'system': 'MedSecure Demo', 'status': 'demo'}

if __name__ == '__main__':
    app.run(debug=True)
