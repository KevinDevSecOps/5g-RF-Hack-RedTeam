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
        
        #!/usr/bin/env python3
"""
Main entry point for 5G RF RedTeam Toolkit
"""
import argparse
import logging
from src.core import FiveGRedTeamCore, get_core_instance
from src.dashboard.app import get_dashboard_instance

def setup_arg_parser():
    """Configurar argumentos de línea de comandos"""
    parser = argparse.ArgumentParser(description='5G RF RedTeam Toolkit')
    parser.add_argument('--dashboard', action='store_true', help='Start web dashboard')
    parser.add_argument('--port', type=int, default=5000, help='Dashboard port')
    parser.add_argument('--config', default='config.yaml', help='Config file')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--no-docker', action='store_true', help='Run without Docker features')
    return parser

def main():
    """Función principal"""
    parser = setup_arg_parser()
    args = parser.parse_args()
    
    # Inicializar core
    try:
        core = get_core_instance(args.config)
        core.logger.info("5G RF RedTeam Toolkit inicializado")
        
        # Registrar módulos por defecto
        from src.core.spectrum_analyzer import SpectrumAnalyzer
        spectrum_analyzer = SpectrumAnalyzer()
        core.register_module('spectrum_analyzer', spectrum_analyzer)
        
        # Iniciar dashboard si se solicita
        if args.dashboard:
            dashboard = get_dashboard_instance(port=args.port)
            core.logger.info(f"Iniciando dashboard en puerto {args.port}")
            dashboard.run_async()
        
        # Mantener el programa ejecutándose
        core.logger.info("Sistema listo. Presiona Ctrl+C para salir.")
        
        try:
            while True:
                # Aquí iría la lógica principal de procesamiento
                # Por ahora solo mantenemos el proceso vivo
                import time
                time.sleep(1)
                
        except KeyboardInterrupt:
            core.logger.info("Aplicación terminada por el usuario")
            
    except Exception as e:
        logging.error(f"Error inicializando la aplicación: {e}")
        raise

if __name__ == "__main__":
    main()