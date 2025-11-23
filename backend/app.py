from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sock import Sock
import subprocess
import json
import os
import logging
import time
import threading

app = Flask(__name__)
CORS(app)
sock = Sock(app)

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


@sock.route('/metrics')
def metrics_websocket(ws):
    """
    WebSocket endpoint para streaming de métricas en tiempo real
    """
    try:
        # Enviar mensaje de conexión
        ws.send(json.dumps({
            "type": "connected",
            "message": "WebSocket connection established",
            "timestamp": time.time()
        }))

        # Verificar que el binario existe
        if not os.path.exists(BINARY_PATH):
            logger.error(f"Binario no encontrado en {BINARY_PATH}")
            ws.send(json.dumps({
                "type": "error",
                "error": "Binary not found",
                "timestamp": time.time()
            }))
            return

        # Verificar permisos de ejecución
        if not os.access(BINARY_PATH, os.X_OK):
            logger.error(f"Binario no tiene permisos de ejecución")
            ws.send(json.dumps({
                "type": "error",
                "error": "Binary not executable",
                "timestamp": time.time()
            }))
            return

        # Verificar que tenemos API key
        if not API_KEY:
            logger.error("API key no configurada")
            ws.send(json.dumps({
                "type": "error",
                "error": "API key not configured",
                "timestamp": time.time()
            }))
            return

        logger.info(f"Iniciando ejecución del binario...")
        ws.send(json.dumps({
            "type": "status",
            "message": "Starting binary execution...",
            "timestamp": time.time()
        }))

        # Variables de entorno para deshabilitar GUI
        env = os.environ.copy()
        env['DISPLAY'] = ''
        env['QT_QPA_PLATFORM'] = 'offscreen'

        start_time = time.time()

        # Ejecutar el binario en un proceso separado
        process = subprocess.Popen(
            [BINARY_PATH, API_KEY],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env,
            bufsize=1,
            universal_newlines=True
        )

        # Función para leer stderr en un thread separado
        stderr_lines = []

        def read_stderr():
            for line in process.stderr:
                stderr_lines.append(line)
                logger.debug(f"STDERR: {line.strip()}")
                ws.send(json.dumps({
                    "type": "stderr",
                    "message": line.strip(),
                    "timestamp": time.time()
                }))

        stderr_thread = threading.Thread(target=read_stderr)
        stderr_thread.daemon = True
        stderr_thread.start()

        # Leer stdout línea por línea y enviar actualizaciones
        stdout_lines = []
        for line in process.stdout:
            stdout_lines.append(line)
            logger.debug(f"STDOUT: {line.strip()}")

            # Enviar cada línea como actualización
            ws.send(json.dumps({
                "type": "stdout",
                "message": line.strip(),
                "timestamp": time.time()
            }))

        # Esperar a que el proceso termine
        return_code = process.wait(timeout=60)
        end_time = time.time()
        execution_time = end_time - start_time

        logger.info(f"Tiempo de ejecución: {execution_time:.2f} segundos")
        logger.info(f"Código de retorno: {return_code}")

        # Combinar toda la salida
        full_stdout = ''.join(stdout_lines)
        full_stderr = ''.join(stderr_lines)

        # Verificar el código de salida
        if return_code != 0:
            logger.error(f"Binario falló con código {return_code}")
            ws.send(json.dumps({
                "type": "error",
                "error": "Binary execution failed",
                "return_code": return_code,
                "execution_time": execution_time,
                "timestamp": time.time()
            }))
            return

        # Verificar si terminó muy rápido
        if execution_time < 5:
            logger.warning(f"Ejecución muy rápida ({execution_time:.2f}s)")
            ws.send(json.dumps({
                "type": "error",
                "error": "No face detected",
                "message": "The measurement ended too quickly. Make sure someone is positioned in front of the camera.",
                "execution_time": execution_time,
                "timestamp": time.time()
            }))
            return

        # Intentar parsear la salida JSON
        try:
            metrics_data = json.loads(full_stdout)
            logger.info("Métricas obtenidas exitosamente")
            ws.send(json.dumps({
                "type": "metrics",
                "data": metrics_data,
                "execution_time": execution_time,
                "timestamp": time.time()
            }))

            ws.send(json.dumps({
                "type": "complete",
                "message": "Measurement completed successfully",
                "timestamp": time.time()
            }))

        except json.JSONDecodeError as e:
            logger.error(f"Error parseando JSON: {e}")

            if "Status: No issues detected" in full_stdout:
                ws.send(json.dumps({
                    "type": "error",
                    "error": "No face detected or measurement incomplete",
                    "message": "Binary executed but didn't produce vital signs data.",
                    "execution_time": execution_time,
                    "timestamp": time.time()
                }))
            else:
                ws.send(json.dumps({
                    "type": "error",
                    "error": "Invalid JSON from binary",
                    "parse_error": str(e),
                    "execution_time": execution_time,
                    "timestamp": time.time()
                }))

    except subprocess.TimeoutExpired:
        logger.error("Timeout ejecutando el binario")
        ws.send(json.dumps({
            "type": "error",
            "error": "Binary execution timeout",
            "timestamp": time.time()
        }))
    except Exception as e:
        logger.exception(f"Error inesperado: {str(e)}")
        ws.send(json.dumps({
            "type": "error",
            "error": str(e),
            "timestamp": time.time()
        }))


@app.route('/metrics', methods=['GET'])
def get_metrics():
    """
    Endpoint HTTP legacy para compatibilidad
    """
    try:
        if not os.path.exists(BINARY_PATH):
            return jsonify({"error": "Binary not found"}), 500

        if not os.access(BINARY_PATH, os.X_OK):
            return jsonify({"error": "Binary not executable"}), 500

        if not API_KEY:
            return jsonify({"error": "API key not configured"}), 500

        env = os.environ.copy()
        env['DISPLAY'] = ''
        env['QT_QPA_PLATFORM'] = 'offscreen'

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

        if result.returncode != 0:
            return jsonify({
                "error": "Binary execution failed",
                "return_code": result.returncode,
                "execution_time": execution_time
            }), 500

        if execution_time < 5:
            return jsonify({
                "error": "No face detected",
                "message": "The measurement ended too quickly.",
                "execution_time": execution_time
            }), 400

        try:
            metrics_data = json.loads(result.stdout)
            return jsonify(metrics_data), 200
        except json.JSONDecodeError as e:
            return jsonify({
                "error": "Invalid JSON from binary",
                "parse_error": str(e)
            }), 500

    except subprocess.TimeoutExpired:
        return jsonify({"error": "Binary execution timeout"}), 504
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/test-binary', methods=['GET'])
def test_binary():
    """
    Endpoint de diagnóstico para probar el binario
    """
    try:
        diagnostics = {
            "binary_exists": os.path.exists(BINARY_PATH),
            "binary_executable": os.access(BINARY_PATH, os.X_OK) if os.path.exists(BINARY_PATH) else False,
            "api_key_configured": bool(API_KEY),
            "api_key_length": len(API_KEY) if API_KEY else 0,
        }

        if os.path.exists(BINARY_PATH):
            stat_info = os.stat(BINARY_PATH)
            diagnostics["binary_size"] = stat_info.st_size
            diagnostics["binary_permissions"] = oct(stat_info.st_mode)

        return jsonify(diagnostics), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    # Verificar al inicio
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

    app.run(host='0.0.0.0', port=5000, debug=False)