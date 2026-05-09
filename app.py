from flask import Flask, render_template
from flask_login import LoginManager
from flask_cors import CORS
from config import Config
from database import db
from socketio_instance import socketio

# Initialize extensions
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    CORS(app)
    socketio.init_app(app)
    
    # Import routes here to avoid circular imports
    from routes.auth import auth_bp
    from routes.tasks import tasks_bp
    from routes.analytics import analytics_bp
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(tasks_bp, url_prefix='/api/tasks')
    app.register_blueprint(analytics_bp, url_prefix='/api/analytics')
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    return app

# Create app instance
app = create_app()

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    from models.user import User
    return User.query.get(int(user_id))

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)