from flask import Flask, jsonify, request
from flask_cors import CORS
import subprocess
import json
import os
import logging
import time

app = Flask(__name__)
CORS(app)

# Configurar logging más detallado
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

BINARY_PATH = "/app/hello_vitals"
API_KEY = os.getenv("SMARTSPECTRA_API_KEY", "")

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint para verificar que el servicio está activo"""
    return jsonify({"status": "healthy", "service": "vitals-api"}), 200

@app.route('/metrics', methods=['GET'])
def get_metrics():
    """
    Ejecuta el binario hello_vitals y retorna las métricas en JSON
    """
    try:
        # Verificar que el binario existe
        if not os.path.exists(BINARY_PATH):
            logger.error(f"Binario no encontrado en {BINARY_PATH}")
            return jsonify({"error": "Binary not found"}), 500
        
        # Verificar permisos de ejecución
        if not os.access(BINARY_PATH, os.X_OK):
            logger.error(f"Binario no tiene permisos de ejecución")
            return jsonify({"error": "Binary not executable"}), 500
        
        # Verificar que tenemos API key
        if not API_KEY:
            logger.error("API key no configurada")
            return jsonify({"error": "API key not configured"}), 500
        
        logger.info(f"Iniciando ejecución del binario...")
        logger.info(f"Ruta: {BINARY_PATH}")
        logger.info(f"API Key presente: {bool(API_KEY)}")
        
        # Variables de entorno para deshabilitar GUI
        env = os.environ.copy()
        env['DISPLAY'] = ''
        env['QT_QPA_PLATFORM'] = 'offscreen'
        
        # Medir tiempo de ejecución
        start_time = time.time()
        
        result = subprocess.run(
            [BINARY_PATH, API_KEY],
            capture_output=True,
            text=True,
            timeout=60,
            env=env
        )
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        logger.info(f"Tiempo de ejecución: {execution_time:.2f} segundos")
        logger.info(f"Código de retorno: {result.returncode}")
        logger.info(f"stdout length: {len(result.stdout)} bytes")
        logger.info(f"stderr length: {len(result.stderr)} bytes")
        
        # Log completo de la salida
        if result.stdout:
            logger.debug(f"STDOUT completo:\n{result.stdout}")
        if result.stderr:
            logger.debug(f"STDERR completo:\n{result.stderr}")
        
        # Verificar el código de salida
        if result.returncode != 0:
            logger.error(f"Binario falló con código {result.returncode}")
            return jsonify({
                "error": "Binary execution failed",
                "return_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "execution_time": execution_time
            }), 500
        
        # Verificar si terminó muy rápido (menos de 5 segundos = probablemente no detectó rostro)
        if execution_time < 5:
            logger.warning(f"Ejecución muy rápida ({execution_time:.2f}s). Posible falta de detección de rostro")
            return jsonify({
                "error": "No face detected",
                "message": "The measurement ended too quickly. Make sure someone is positioned in front of the camera.",
                "execution_time": execution_time,
                "raw_output": result.stdout,
                "hint": "The binary requires face detection to start measurement. Execution took less than 5 seconds."
            }), 400
        
        # Intentar parsear la salida JSON
        try:
            metrics_data = json.loads(result.stdout)
            logger.info("Métricas obtenidas exitosamente")
            return jsonify(metrics_data), 200
        except json.JSONDecodeError as e:
            logger.error(f"Error parseando JSON: {e}")
            
            # Si no es JSON pero ejecutó correctamente, puede ser el mensaje de status
            if "Status: No issues detected" in result.stdout:
                return jsonify({
                    "error": "No face detected or measurement incomplete",
                    "message": "Binary executed but didn't produce vital signs data. Ensure a person is positioned correctly in front of the camera.",
                    "execution_time": execution_time,
                    "raw_output": result.stdout,
                    "stderr_preview": result.stderr[-500:] if len(result.stderr) > 500 else result.stderr
                }), 400
            
            # Otro error de parseo
            return jsonify({
                "error": "Invalid JSON from binary",
                "raw_output": result.stdout,
                "stderr": result.stderr,
                "execution_time": execution_time,
                "parse_error": str(e)
            }), 500
            
    except subprocess.TimeoutExpired:
        logger.error("Timeout ejecutando el binario")
        return jsonify({"error": "Binary execution timeout"}), 504
    except Exception as e:
        logger.exception(f"Error inesperado: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/test-binary', methods=['GET'])
def test_binary():
    """
    Endpoint de diagnóstico para probar el binario con diferentes configuraciones
    """
    try:
        diagnostics = {
            "binary_exists": os.path.exists(BINARY_PATH),
            "binary_executable": os.access(BINARY_PATH, os.X_OK) if os.path.exists(BINARY_PATH) else False,
            "api_key_configured": bool(API_KEY),
            "api_key_length": len(API_KEY) if API_KEY else 0,
        }
        
        # Intentar obtener información del archivo
        if os.path.exists(BINARY_PATH):
            stat_info = os.stat(BINARY_PATH)
            diagnostics["binary_size"] = stat_info.st_size
            diagnostics["binary_permissions"] = oct(stat_info.st_mode)
        
        # Probar ejecución con --help o --version
        if diagnostics["binary_exists"] and diagnostics["binary_executable"]:
            test_flags = ["--help", "-h", "--version", "-v", "help"]
            for flag in test_flags:
                try:
                    result = subprocess.run(
                        [BINARY_PATH, flag],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    if result.stdout or result.stderr:
                        diagnostics[f"flag_{flag}"] = {
                            "stdout": result.stdout,
                            "stderr": result.stderr,
                            "return_code": result.returncode
                        }
                except Exception as e:
                    diagnostics[f"flag_{flag}"] = f"Error: {str(e)}"
        
        return jsonify(diagnostics), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/metrics/verbose', methods=['GET'])
def get_metrics_verbose():
    """
    Versión verbose que muestra toda la salida del binario
    """
    try:
        if not os.path.exists(BINARY_PATH):
            return jsonify({"error": "Binary not found"}), 500
        
        if not API_KEY:
            return jsonify({"error": "API key not configured"}), 500
        
        env = os.environ.copy()
        env['DISPLAY'] = ''
        env['QT_QPA_PLATFORM'] = 'offscreen'
        
        result = subprocess.run(
            [BINARY_PATH, API_KEY],
            capture_output=True,
            text=True,
            timeout=60,
            env=env
        )
        
        return jsonify({
            "return_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "success": result.returncode == 0
        }), 200
        
    except subprocess.TimeoutExpired:
        return jsonify({"error": "Timeout"}), 504
    except Exception as e:
        return jsonify({"error": str(e)}), 500

import threading
import asyncio

async def websocket_handler(websocket):
    logger.info("WebSocket client connected")
    import io
    from PIL import Image
    import random
    try:
        async for message in websocket:
            logger.debug(f"Received frame of size {len(message)} bytes")
            # Decode JPEG frame
            try:
                img = Image.open(io.BytesIO(message))
                logger.info(f"Frame decoded: {img.size}, mode: {img.mode}")
            except Exception as e:
                logger.error(f"Error decoding frame: {e}")
                continue
            # Generate mock metrics (simulate ML)
            mock_metrics = {
                "status": "success",
                "timestamp": int(time.time()),
                "duration_seconds": 1,
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
            # Log full metrics JSON for inspection
            logger.info(f"Sending metrics: {json.dumps(mock_metrics, indent=2)}")
            # Send metrics back to client
            await websocket.send(json.dumps(mock_metrics))
    except Exception as e:
        logger.error(f"WebSocket error: {e}")

def start_websocket_server():
    import websockets
    async def run_server():
        logger.info("Starting WebSocket server on port 5000...")
        async with websockets.serve(websocket_handler, '0.0.0.0', 5000):
            await asyncio.Future()  # run forever
    asyncio.run(run_server())

if __name__ == '__main__':
    # Verificar al inicio que el binario existe
    if os.path.exists(BINARY_PATH):
        logger.info(f"✓ Binario encontrado en {BINARY_PATH}")
        logger.info(f"✓ Permisos: {oct(os.stat(BINARY_PATH).st_mode)}")
        logger.info(f"✓ Ejecutable: {os.access(BINARY_PATH, os.X_OK)}")
    else:
        logger.warning(f"⚠ Binario NO encontrado en {BINARY_PATH}")
    
    if API_KEY:
        logger.info(f"✓ API Key configurada (longitud: {len(API_KEY)})")
    else:
        logger.warning("⚠ API Key NO configurada")

    # Start Flask and WebSocket server in parallel
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=5001, debug=False), daemon=True).start()
    start_websocket_server()