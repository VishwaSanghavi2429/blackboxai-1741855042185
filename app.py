from flask import Flask, render_template, redirect, url_for
from config import Config
import logging
import os
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Add current datetime to all templates
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# Root route
@app.route('/')
def index():
    return redirect(url_for('auth.login'))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize the application
Config.init_app(app)

# Import routes after app initialization to avoid circular imports
from routes.auth import auth_bp
from routes.appointments import appointments_bp
from routes.events import events_bp

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(appointments_bp)
app.register_blueprint(events_bp)

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', error_code=404, message="Page not found"), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', error_code=500, message="Internal server error"), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
