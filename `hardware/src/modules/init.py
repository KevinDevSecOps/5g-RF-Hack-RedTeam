# Añadir imports al inicio
from .reporting.report_generator import AdvancedReportGenerator
from .automation.workflow_engine import WorkflowEngine

# En la clase ModulesManager, actualizar initialize_modules
    def initialize_modules(self):
        """Inicializar todos los módulos"""
        try:
            # ... (módulos existentes)
            
            # Módulos de reporting y automatización
            self.modules['report_generator'] = AdvancedReportGenerator(self.core)
            self.logger.info("Sistema de reporting inicializado")
            
            self.modules['workflow_engine'] = WorkflowEngine(self.core)
            self.logger.info("Motor de workflows inicializado")
            
            # Cargar workflows por defecto
            self._load_default_workflows()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error inicializando módulos de reporting: {e}")
            return False
    
    def _load_default_workflows(self):
        """Cargar workflows por defecto"""
        try:
            default_workflows = {
                'basic_scan': {
                    'steps': {
                        'initialize_scan': {
                            'type': 'scan',
                            'frequency': 3.5e9,
                            'duration': 60
                        },
                        'analyze_results': {
                            'type': 'analysis',
                            'analysis_type': 'basic',
                            'dependencies': ['initialize_scan']
                        },
                        'generate_report': {
                            'type': 'report',
                            'report_type': 'executive',
                            'dependencies': ['analyze_results']
                        }
                    }
                },
                'comprehensive_audit': {
                    'steps': {
                        'initial_scan': {
                            'type': 'scan',
                            'frequency': 3.4e9,
                            'duration': 120
                        },
                        'deep_analysis': {
                            'type': 'analysis',
                            'analysis_type': 'advanced',
                            'dependencies': ['initial_scan']
                        },
                        'threat_assessment': {
                            'type': 'analysis',
                            'analysis_type': 'threat',
                            'dependencies': ['deep_analysis']
                        },
                        'final_report': {
                            'type': 'report',
                            'report_type': 'technical',
                            'dependencies': ['threat_assessment']
                        }
                    }
                }
            }
            
            for name, config in default_workflows.items():
                self.modules['workflow_engine'].load_workflow(name, config)
            
            self.logger.info("Workflows por defecto cargados")
            
        except Exception as e:
            self.logger.warning(f"No se pudieron cargar workflows por defecto: {e}")
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