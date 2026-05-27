import os
from flask import Flask, render_template, jsonify
from flask_cors import CORS
from jinja2 import ChoiceLoader, FileSystemLoader

from backend.config import config_by_name
from backend.routes import api_bp
from backend.database.db import init_db

def create_app(config_name=None):
    """
    Application factory pattern to configure and initialize the Flask instance.
    Sets up CORS, Jinja templates choice loaders, database path schemas, and blueprints.
    """
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
        
    # Setup custom paths for template and static asset rendering
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_dir = os.path.join(BASE_DIR, 'frontend', 'templates')
    static_dir = os.path.join(BASE_DIR, 'frontend', 'static')
    
    app = Flask(
        __name__,
        template_folder=template_dir,
        static_folder=static_dir
    )
    
    # Load configuration
    app.config.from_object(config_by_name[config_name])
    
    # Configure multiple template locations for Jinja2 (templates and components)
    app.jinja_loader = ChoiceLoader([
        FileSystemLoader(template_dir),
        FileSystemLoader(os.path.join(BASE_DIR, 'frontend'))
    ])
    
    # Enable Cross-Origin Resource Sharing (CORS)
    CORS(app, resources={r"/*": {"origins": "*"}})
    
    # Initialize SQL database
    init_db(app.config['DB_PATH'])
    
    # Register blueprints
    app.register_blueprint(api_bp)
    
    # Register HTML page routing
    @app.route('/')
    def index():
        """Renders the main cyber spam detector dashboard application page."""
        return render_template('index.html')
        
    @app.route('/about')
    def about():
        """Renders the technical educational panel page."""
        return render_template('about.html')
        
    @app.route('/dashboard')
    def dashboard():
        """Renders the high-fidelity analytics table and graphics page."""
        return render_template('dashboard.html')
        
    # Error Handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('index.html'), 404
        
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "An internal system error has occurred."}), 500
        
    return app

# Instantiate the default application object for WSGI runners like Gunicorn
app = create_app()
