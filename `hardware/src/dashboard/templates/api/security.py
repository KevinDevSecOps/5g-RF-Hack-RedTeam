from flask import Blueprint, jsonify, request
import logging
from datetime import datetime

security_bp = Blueprint('security', __name__)
logger = logging.getLogger(__name__)

# Almacenamiento de detecciones
security_events = []
threat_stats = {
    "total_detections": 0,
    "high_severity": 0,
    "medium_severity": 0,
    "low_severity": 0
}

@security_bp.route('/api/security/events')
def get_security_events():
    """Obtener eventos de seguridad"""
    return jsonify({
        "events": security_events[-50:],  # Últimos 50 eventos
        "stats": threat_stats
    })

@security_bp.route('/api/security/detect', methods=['POST'])
def detect_threat():
    """Endpoint para detección de amenazas"""
    try:
        data = request.get_json()
        
        # Simular detección (en producción sería análisis real)
        event = {
            "id": len(security_events) + 1,
            "timestamp": datetime.now().isoformat(),
            "type": "suspicious_activity",
            "severity": "medium",
            "description": "Suspicious RF pattern detected",
            "frequency": 3.5e9,
            "power": -45.2,
            "confidence": 0.85
        }
        
        security_events.append(event)
        
        # Actualizar estadísticas
        threat_stats["total_detections"] += 1
        if event["severity"] == "high":
            threat_stats["high_severity"] += 1
        elif event["severity"] == "medium":
            threat_stats["medium_severity"] += 1
        else:
            threat_stats["low_severity"] += 1
        
        logger.warning(f"Security event detected: {event}")
        
        return jsonify({
            "status": "success",
            "event": event,
            "message": "Threat detected and logged"
        })
        
    except Exception as e:
        logger.error(f"Error in threat detection: {e}")
        return jsonify({"error": str(e)}), 500

@security_bp.route('/api/security/stats')
def security_stats():
    """Estadísticas de seguridad"""
    return jsonify(threat_stats)

@security_bp.route('/security')
def security_view():
    """Página de seguridad"""
    return """
    <h1>Security Monitoring</h1>
    <p>Monitoreo de amenazas y eventos de seguridad</p>
    """