"""
FitProof - Фитнес дасгалын бүртгэлийн систем
QR код ашиглан дасгалаа бүртгэх, ахиц дэвшлээ хянах
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "main.login"


def create_app(config_name="default"):
    """Application Factory Pattern"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Extensions эхлүүлэх
    db.init_app(app)
    login_manager.init_app(app)

    # Blueprints бүртгүүлэх
    from app.routes import main_bp

    app.register_blueprint(main_bp)

    # Database үүсгэх
    with app.app_context():
        db.create_all()

    return app
