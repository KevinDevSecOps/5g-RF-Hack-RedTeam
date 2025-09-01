from flask import Blueprint, jsonify, request
import logging
import numpy as np
from src.core import get_core_instance

analysis_bp = Blueprint('analysis', __name__)
logger = logging.getLogger(__name__)

@analysis_bp.route('/api/analysis/detect_advanced', methods=['POST'])
def detect_advanced_anomalies():
    """Detección avanzada de anomalías con ML"""
    try:
        data = request.get_json()
        spectrum_data = data.get('spectrum_data', {})
        
        core = get_core_instance()
        ml_module = core.get_modules_manager().get_module('advanced_anomaly_detector')
        
        if not ml_module:
            return jsonify({"error": "ML module not initialized"}), 500
        
        results = ml_module.detect_anomalies_advanced(spectrum_data)
        
        return jsonify({
            "status": "success",
            "results": results
        })
        
    except Exception as e:
        logger.error(f"Error in advanced anomaly detection: {e}")
        return jsonify({"error": str(e)}), 500

@analysis_bp.route('/api/analysis/classify_signal', methods=['POST'])
def classify_signal():
    """Clasificar tipo de señal"""
    try:
        data = request.get_json()
        iq_data = np.array(data.get('iq_data', []))
        
        if len(iq_data) == 0:
            return jsonify({"error": "No IQ data provided"}), 400
        
        core = get_core_instance()
        classifier = core.get_modules_manager().get_module('signal_classifier')
        
        if not classifier or not classifier.is_trained:
            return jsonify({"error": "Classifier not trained"}), 500
        
        signal_type, confidence = classifier.predict_signal_type(iq_data)
        
        return jsonify({
            "status": "success",
            "signal_type": signal_type,
            "confidence": confidence,
            "is_anomalous": signal_type in ['jamming', 'unknown']
        })
        
    except Exception as e:
        logger.error(f"Error classifying signal: {e}")
        return jsonify({"error": str(e)}), 500

@analysis_bp.route('/api/analysis/extract_features', methods=['POST'])
def extract_features():
    """Extraer características avanzadas de señal"""
    try:
        data = request.get_json()
        iq_data = np.array(data.get('iq_data', []))
        sample_rate = data.get('sample_rate', 20e6)
        
        if len(iq_data) == 0:
            return jsonify({"error": "No IQ data provided"}), 400
        
        core = get_core_instance()
        extractor = core.get_modules_manager().get_module('feature_extractor')
        
        features = extractor.extract_comprehensive_features(iq_data, sample_rate)
        
        return jsonify({
            "status": "success",
            "features": features
        })
        
    except Exception as e:
        logger.error(f"Error extracting features: {e}")
        return jsonify({"error": str(e)}), 500

@analysis_bp.route('/api/analysis/train_models', methods=['POST'])
def train_models():
    """Entrenar modelos de ML"""
    try:
        core = get_core_instance()
        ml_module = core.get_modules_manager().get_module('advanced_anomaly_detector')
        classifier = core.get_modules_manager().get_module('signal_classifier')
        
        # Entrenar detector de anomalías
        training_data = []  # En producción, esto vendría de datos reales
        for _ in range(100):
            training_data.append({
                'frequencies': np.linspace(3.4e9, 3.6e9, 1000),
                'spectrum': np.random.randn(1000) * 10 + 50
            })
        
        ml_success = ml_module.train_models(training_data)
        
        # Entrenar clasificador
        X, y = classifier.generate_training_data(500)
        classifier.train(X, y, epochs=50)
        
        return jsonify({
            "status": "success",
            "anomaly_detector_trained": ml_success,
            "classifier_trained": classifier.is_trained
        })
        
    except Exception as e:
        logger.error(f"Error training models: {e}")
        return jsonify({"error": str(e)}), 500