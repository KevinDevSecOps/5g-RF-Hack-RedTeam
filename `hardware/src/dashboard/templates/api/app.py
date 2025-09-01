from flask import Flask, render_template, jsonify, request
import logging
from datetime import datetime
import threading
import time

# Import blueprints
from .api.spectrum import spectrum_bp
from .api.scans import scans_bp
from .api.security import security_bp

class Dashboard:
    def __init__(self, host='0.0.0.0', port=5000):
        self.host = host
        self.port = port
        self.app = Flask(__name__)
        self.logger = logging.getLogger(__name__)
        
        # Configurar Flask
        self.app.secret_key = '5g-redteam-secret-2024'
        
        # Registrar blueprints
        self.app.register_blueprint(spectrum_bp)
        self.app.register_blueprint(scans_bp)
        self.app.register_blueprint(security_bp)
        
        # Configurar rutas
        self.setup_routes()
        
        # Datos de ejemplo para el dashboard
        self.dashboard_stats = {
            "signal_strength": -65.3,
            "frequency": 3.5e9,
            "threats_detected": 0,
            "packets_captured": 0,
            "system_status": "online",
            "cpu_usage": 25.7,
            "memory_usage": 45.2
        }
        
        self.logger.info("Dashboard inicializado")

    def setup_routes(self):
        """Configurar todas las rutas del dashboard"""
        
        @self.app.route('/')
        def index():
            """Página principal del dashboard"""
            return render_template('dashboard.html')
        
        @self.app.route('/api/dashboard/stats')
        def dashboard_stats():
            """API para estadísticas del dashboard"""
            # Actualizar stats (simulado)
            self.update_stats()
            return jsonify(self.dashboard_stats)
        
        @self.app.route('/api/system/status')
        def system_status():
            """Estado del sistema"""
            return jsonify({
                "status": "online",
                "timestamp": datetime.now().isoformat(),
                "version": "1.0.0",
                "uptime": "2 hours"
            })
        
        @self.app.errorhandler(404)
        def not_found(error):
            return jsonify({"error": "Endpoint not found"}), 404
        
        @self.app.errorhandler(500)
        def internal_error(error):
            return jsonify({"error": "Internal server error"}), 500

    def update_stats(self):
        """Actualizar estadísticas (simulado)"""
        # En producción, estos vendrían de monitoreo real
        self.dashboard_stats["threats_detected"] += 1
        self.dashboard_stats["packets_captured"] += 100
        self.dashboard_stats["signal_strength"] = -65 + (