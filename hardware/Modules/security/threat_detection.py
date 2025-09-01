"""
Detección avanzada de amenazas en redes 5G
"""
import logging
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.cluster import DBSCAN
import json
from datetime import datetime

logger = logging.getLogger(__name__)

class ThreatDetector:
    def __init__(self, core):
        self.core = core
        self.logger = logger
        self.anomaly_detector = IsolationForest(contamination=0.1, random_state=42)
        self.cluster_detector = DBSCAN(eps=0.5, min_samples=2)
        self.threat_history = []
        
    def detect_anomalies(self, spectrum_data, threshold=0.6):
        """
        Detectar anomalías en datos espectrales usando Machine Learning
        """
        try:
            # Preparar datos para ML
            features = self.extract_features(spectrum_data)
            
            if len(features) < 10:  # Mínimo de muestras
                return []
            
            # Detectar anomalías
            predictions = self.anomaly_detector.fit_predict(features)
            anomaly_scores = self.anomaly_detector.decision_function(features)
            
            anomalies = []
            for i, (pred, score) in enumerate(zip(predictions, anomaly_scores)):
                if pred == -1 and abs(score) > threshold:
                    anomaly = {
                        'timestamp': datetime.now().isoformat(),
                        'frequency': spectrum_data['frequencies'][i],
                        'power': spectrum_data['spectrum'][i],
                        'score': float(score),
                        'type': 'spectral_anomaly'
                    }
                    anomalies.append(anomaly)
                    self.log_threat(anomaly)
            
            return anomalies
            
        except Exception as e:
            self.logger.error(f"Error en detección de anomalías: {e}")
            return []
    
    def extract_features(self, spectrum_data):
        """Extraer características para ML"""
        features = []
        
        # Características espectrales básicas
        power = np.array(spectrum_data['spectrum'])
        frequencies = np.array(spectrum_data['frequencies'])
        
        # Estadísticas
        mean_power = np.mean(power)
        std_power = np.std(power)
        max_power = np.max(power)
        min_power = np.min(power)
        
        # Características por frecuencia
        for i in range(len(power)):
            feature_vector = [
                power[i],
                frequencies[i],
                mean_power,
                std_power,
                max_power - min_power,
                (power[i] - mean_power) / std_power if std_power > 0 else 0
            ]
            features.append(feature_vector)
        
        return features
    
    def detect_jamming(self, spectrum_data, threshold=-50):
        """
        Detectar posibles ataques de jamming
        """
        jamming_signals = []
        
        for i, power in enumerate(spectrum_data['spectrum']):
            if power > threshold:  # Señal muy fuerte
                jamming_signal = {
                    'timestamp': datetime.now().isoformat(),
                    'frequency': spectrum_data['frequencies'][i],
                    'power': power,
                    'type': 'possible_jamming',
                    'confidence': min(1.0, (power + 80) / 30)  # -50dBm = 1.0, -80dBm = 0.0
                }
                
                jamming_signals.append(jamming_signal)
                self.log_threat(jamming_signal)
        
        return jamming_signals
    
    def detect_spoofing(self, signals, min_signals=3):
        """
        Detectar posibles señales de spoofing
        """
        if len(signals) < min_signals:
            return []
        
        # Agrupar señales por frecuencia similar
        frequencies = [s['frequency'] for s in signals]
        clustering = self.cluster_detector.fit_predict(np.array(frequencies).reshape(-1, 1))
        
        spoofing_clusters = []
        for cluster_id in set(clustering):
            if cluster_id != -1:  # Ignorar outliers
                cluster_signals = [s for i, s in enumerate(signals) if clustering[i] == cluster_id]
                if len(cluster_signals) >= min_signals:
                    spoofing_clusters.append({
                        'cluster_id': cluster_id,
                        'signals': cluster_signals,
                        'average_frequency': np.mean([s['frequency'] for s in cluster_signals]),
                        'type': 'possible_spoofing'
                    })
        
        return spoofing_clusters
    
    def log_threat(self, threat_data):
        """Registrar amenaza detectada"""
        threat_data['id'] = len(self.threat_history) + 1
        threat_data['timestamp'] = datetime.now().isoformat()
        
        self.threat_history.append(threat_data)
        self.core.save_results(threat_data, f"threat_{threat_data['id']}.json")
        
        self.logger.warning(f"Amenaza detectada: {threat_data['type']} en {threat_data['frequency']/1e9}GHz")
    
    def get_threat_history(self, limit=50):
        """Obtener historial de amenazas"""
        return self.threat_history[-limit:] if self.threat_history else []
    
    def generate_threat_report(self):
        """Generar reporte de amenazas"""
        report = {
            'generated_at': datetime.now().isoformat(),
            'total_threats': len(self.threat_history),
            'by_type': {},
            'recent_threats': self.get_threat_history(20)
        }
        
        # Contar amenazas por tipo
        for threat in self.threat_history:
            threat_type = threat['type']
            report['by_type'][threat_type] = report['by_type'].get(threat_type, 0) + 1
        
        return report