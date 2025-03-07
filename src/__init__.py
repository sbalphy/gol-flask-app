from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.environ.get("DB_PATH", "/app/data/database.db")}'

    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Você precisa estar logado para acessar esta página.'
    login_manager.init_app(app)

    from .auth import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    from .auth import auth as auth_bp
    app.register_blueprint(auth_bp)
    
    from .dash import dash as dash_bp
    app.register_blueprint(dash_bp)
    
    return app