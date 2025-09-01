from flask import Blueprint, jsonify, request
import logging
from datetime import datetime

scans_bp = Blueprint('scans', __name__)
logger = logging.getLogger(__name__)

# Almacenamiento en memoria (en producción usar DB)
scan_sessions = []
current_scan = None

@scans_bp.route('/api/scans', methods=['GET'])
def get_scans():
    """Obtener historial de scans"""
    return jsonify({
        "sessions": scan_sessions,
        "current_scan": current_scan
    })

@scans_bp.route('/api/scan/start', methods=['POST'])
def start_scan():
    """Iniciar un nuevo scan"""
    global current_scan
    
    try:
        data = request.get_json() or {}
        frequency = data.get('frequency', 3.5e9)
        bandwidth = data.get('bandwidth', 20e6)
        duration = data.get('duration', 60)
        
        scan_id = f"scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        current_scan = {
            "id": scan_id,
            "start_time": datetime.now().isoformat(),
            "frequency": frequency,
            "bandwidth": bandwidth,
            "duration": duration,
            "status": "running",
            "progress": 0
        }
        
        scan_sessions.append(current_scan)
        
        logger.info(f"Scan started: {scan_id}")
        
        return jsonify({
            "status": "success",
            "scan_id": scan_id,
            "message": "Scan started successfully"
        })
        
    except Exception as e:
        logger.error(f"Error starting scan: {e}")
        return jsonify({"error": str(e)}), 500

@scans_bp.route('/api/scan/stop', methods=['POST'])
def stop_scan():
    """Detener scan actual"""
    global current_scan
    
    try:
        if current_scan:
            current_scan["status"] = "stopped"
            current_scan["end_time"] = datetime.now().isoformat()
            
            logger.info(f"Scan stopped: {current_scan['id']}")
            
            stopped_scan = current_scan
            current_scan = None
            
            return jsonify({
                "status": "success",
                "scan": stopped_scan,
                "message": "Scan stopped successfully"
            })
        else:
            return jsonify({
                "status": "error",
                "message": "No active scan to stop"
            }), 400
            
    except Exception as e:
        logger.error(f"Error stopping scan: {e}")
        return jsonify({"error": str(e)}), 500

@scans_bp.route('/api/scan/status')
def scan_status():
    """Estado del scan actual"""
    if current_scan:
        # Simular progreso (en producción sería real)
        if current_scan["status"] == "running":
            current_scan["progress"] = min(current_scan["progress"] + 5, 100)
        
        return jsonify(current_scan)
    else:
        return jsonify({
            "status": "idle",
            "message": "No active scans"
        })

@scans_bp.route('/scans')
def scans_view():
    """Página de gestión de scans"""
    return """
    <h1>Scan Management</h1>
    <p>Gestión de escaneos y capturas</p>
    """