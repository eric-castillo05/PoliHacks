from flask import Flask, jsonify, request
from flask_cors import CORS
import time
import random
import logging

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "vitals-api"}), 200

@app.route('/metrics', methods=['GET'])
def get_metrics():
    time.sleep(3)
    
    mock_data = {
        "status": "success",
        "timestamp": int(time.time()),
        "duration_seconds": 30,
        "heart_rate": {
            "value": random.randint(60, 85),
            "unit": "bpm",
            "confidence": round(random.uniform(0.85, 0.98), 2)
        },
        "breathing_rate": {
            "value": random.randint(12, 18),
            "unit": "breaths/min",
            "confidence": round(random.uniform(0.80, 0.95), 2)
        },
        "hrv": {
            "value": random.randint(30, 80),
            "unit": "ms",
            "confidence": round(random.uniform(0.75, 0.90), 2)
        }
    }
    
    logger.info("Retornando metricas simuladas")
    return jsonify(mock_data), 200

if __name__ == '__main__':
    logger.info("Iniciando API MOCK de vitales")
    logger.info("Esta es una version SIMULADA para desarrollo")
    app.run(host='0.0.0.0', port=5000, debug=True)
