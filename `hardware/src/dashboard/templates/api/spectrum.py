from flask import Blueprint, jsonify, request
import logging
from src.core import get_core_instance

# Create blueprint
spectrum_bp = Blueprint('spectrum', __name__)
logger = logging.getLogger(__name__)

@spectrum_bp.route('/api/spectrum/data')
def spectrum_data():
    """Endpoint para datos del espectro en tiempo real"""
    try:
        core = get_core_instance()
        spectrum_analyzer = core.get_module('spectrum_analyzer')
        
        if spectrum_analyzer and spectrum_analyzer.spectrum_data:
            return jsonify(spectrum_analyzer.spectrum_data)
        else:
            # Datos simulados si no hay analyzer
            import numpy as np
            frequencies = np.linspace(3.4e9, 3.6e9, 1000)
            power = np.random.randn(1000) * 10 + 50
            
            return jsonify({
                "frequencies": frequencies.tolist(),
                "spectrum": power.tolist(),
                "peaks": [],
                "timestamp": "2024-01-01T00:00:00Z"
            })
            
    except Exception as e:
        logger.error(f"Error en spectrum data: {e}")
        return jsonify({"error": str(e)}), 500

@spectrum_bp.route('/api/spectrum/start', methods=['POST'])
def start_spectrum_scan():
    """Iniciar scanning de espectro"""
    try:
        core = get_core_instance()
        spectrum_analyzer = core.get_module('spectrum_analyzer')
        
        if not spectrum_analyzer:
            from src.core.spectrum_analyzer import SpectrumAnalyzer
            spectrum_analyzer = SpectrumAnalyzer()
            core.register_module('spectrum_analyzer', spectrum_analyzer)
        
        # Iniciar scanning en segundo plano
        def spectrum_callback(data):
            # Callback para procesar datos del espectro
            logger.info(f"Spectrum data received: {len(data['frequencies'])} points")
        
        spectrum_analyzer.start_continuous_scan(spectrum_callback)
        
        return jsonify({
            "status": "success",
            "message": "Spectrum scanning started"
        })
        
    except Exception as e:
        logger.error(f"Error starting spectrum scan: {e}")
        return jsonify({"error": str(e)}), 500

@spectrum_bp.route('/api/spectrum/stop', methods=['POST'])
def stop_spectrum_scan():
    """Detener scanning de espectro"""
    try:
        core = get_core_instance()
        spectrum_analyzer = core.get_module('spectrum_analyzer')
        
        if spectrum_analyzer:
            spectrum_analyzer.stop_continuous_scan()
        
        return jsonify({
            "status": "success",
            "message": "Spectrum scanning stopped"
        })
        
    except Exception as e:
        logger.error(f"Error stopping spectrum scan: {e}")
        return jsonify({"error": str(e)}), 500

@spectrum_bp.route('/spectrum')
def spectrum_view():
    """Página principal del spectrum analyzer"""
    return """
    <h1>Spectrum Analyzer</h1>
    <p>Esta será la página completa del analizador de espectro</p>
    """