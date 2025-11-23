from flask import Flask
from flask_cors import CORS

from flaskr.routes.GeminiRoute import gemini_bp
from flaskr.utils import Config


def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": Config.ROUTE}})
    app.register_blueprint(gemini_bp, url_prefix="/gemini")
    return app