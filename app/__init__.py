from flask import Flask
from flask_cors import CORS
import os
import sys

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Add project root to the Python path to allow for absolute imports
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    app.config['PULLED_CODE_DIR'] = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'PulledCode')
    app.config['DATA_DIR'] = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    app.config['TEMPLATES_DIR'] = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
    # Exclude heavy or generated folders from Flask's file-watcher (watchdog) to avoid unnecessary reloads
    app.config['WATCHDOG_EXCLUDE_PATTERNS'] = ['*/analysis_engine/*', '*/PulledCode/*']
    
    # Register blueprints
    from app.routes.main import main_bp
    app.register_blueprint(main_bp)
    
    return app
