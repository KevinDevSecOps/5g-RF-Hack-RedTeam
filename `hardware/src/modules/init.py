# Añadir imports al inicio
from .ml.anomaly_detection import AdvancedAnomalyDetector
from .ml.signal_classification import SignalClassifier
from .analysis.signal.feature_extraction import AdvancedFeatureExtractor

# En la clase ModulesManager, actualizar initialize_modules
    def initialize_modules(self):
        """Inicializar todos los módulos"""
        try:
            # ... (módulos existentes)
            
            # Módulos de ML avanzado
            self.modules['advanced_anomaly_detector'] = AdvancedAnomalyDetector(self.core)
            self.logger.info("Detección avanzada de anomalías inicializada")
            
            self.modules['signal_classifier'] = SignalClassifier(self.core)
            self.logger.info("Clasificador de señales inicializado")
            
            self.modules['feature_extractor'] = AdvancedFeatureExtractor()
            self.logger.info("Extractor de características inicializado")
            
            # Entrenar modelos con datos simulados
            self.train_ml_models()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error inicializando módulos ML: {e}")
            return False
    
    def train_ml_models(self):
        """Entrenar modelos de ML con datos simulados"""
        try:
            # Generar datos de entrenamiento para anomalías
            training_data = []
            for _ in range(100):
                training_data.append({
                    'frequencies': np.linspace(3.4e9, 3.6e9, 1000),
                    'spectrum': np.random.randn(1000) * 10 + 50
                })
            
            self.modules['advanced_anomaly_detector'].train_models(training_data)
            
            # Entrenar clasificador de señales
            X, y = self.modules['signal_classifier'].generate_training_data(500)
            self.modules['signal_classifier'].train(X, y, epochs=50)
            
            self.logger.info("Modelos de ML entrenados con datos simulados")
            
        except Exception as e:
            self.logger.warning(f"No se pudieron entrenar modelos ML: {e}")