from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
# Adjust these imports based on your actual project structure
from flaskr.services.GeminiService import GeminiService
from flaskr.utils import Config

gemini_bp = Blueprint('gemini', __name__)

gemini_service = GeminiService()


@gemini_bp.route('/get_answer', methods=['POST'])
@cross_origin(origins=Config.ROUTE, supports_credentials=True)
def get_answer():
    try:
        data = request.get_json()
    except Exception:
        return jsonify({"error": "Invalid JSON body"}), 400

    message = data.get("message")

    if not message:
        return jsonify({"error": "Missing 'message' field in request body"}), 400

    response_data, status_code = gemini_service.get_answer(message)

    return jsonify(response_data), status_code