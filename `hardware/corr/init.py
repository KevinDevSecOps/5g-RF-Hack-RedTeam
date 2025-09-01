"""
Core framework for 5G RF RedTeam Toolkit
"""
import logging
import logging.config
import yaml
import os
from datetime import datetime
import json

class FiveGRedTeamCore:
    def __init__(self, config_file="config.yaml"):
        self.config = self.load_config(config_file)
        self.modules = {}
        self.setup_logging()
        self.setup_directories()
        self.logger.info("5G RF RedTeam Core inicializado")
        
    def load_config(self, config_file):
        """Cargar configuración desde YAML"""
        try:
            with open(config_file, 'r') as f:
                config = yaml.safe_load(f)
                self.validate_config(config)
                return config
        except FileNotFoundError:
            self.logger.warning(f"Archivo de configuración {config_file} no encontrado, usando configuración por defecto")
            return self.default_config()
        except yaml.YAMLError as e:
            self.logger.error(f"Error parsing YAML config: {e}")
            return self.default_config()
    
    def validate_config(self, config):
        """Validar configuración"""
        required_sections = ['general', 'rf', 'dashboard']
        for section in required_sections:
            if section not in config:
                raise ValueError(f"Sección requerida '{section}' no encontrada en configuración")
    
    def default_config(self):
        """Configuración por defecto"""
        return {
            'general': {
                'log_level': 'INFO',
                'output_dir': './data/output',
                'max_file_size': 10485760,
                'backup_count': 5
            },
            'rf': {
                'sample_rate': 20000000,
                'center_freq': 3500000000,
                'gain': 40,
                'bandwidth': 20000000,
                'if_gain': 20,
                'bb_gain': 20
            },
            'dashboard': {
                'host': '0.0.0.0',
                'port': 5000,
                'debug': False
            }
        }
    
    def setup_logging(self):
        """Configurar sistema de logging"""
        try:
            if 'logging' in self.config:
                logging.config.dictConfig(self.config['logging'])
            else:
                logging.basicConfig(
                    level=getattr(logging, self.config['general']['log_level']),
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler(f"5g_redteam_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
                        logging.StreamHandler()
                    ]
                )
            self.logger = logging.getLogger(__name__)
            
        except Exception as e:
            print(f"Error configuring logging: {e}")
            logging.basicConfig(level=logging.INFO)
            self.logger = logging.getLogger(__name__)
    
    def setup_directories(self):
        """Crear directorios necesarios"""
        directories = [
            self.config['general']['output_dir'],
            './data',
            './logs',
            './tmp'
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            self.logger.info(f"Directorio creado/verificado: {directory}")
    
    def register_module(self, name, module):
        """Registrar un módulo"""
        self.modules[name] = module
        self.logger.info(f"Módulo registrado: {name}")
    
    def get_module(self, name):
        """Obtener un módulo registrado"""
        return self.modules.get(name)
    
    def save_results(self, data, filename):
        """Guardar resultados en JSON"""
        output_path = os.path.join(self.config['general']['output_dir'], filename)
        try:
            with open(output_path, 'w') as f:
                json.dump(data, f, indent=2)
            self.logger.info(f"Resultados guardados en: {output_path}")
            return True
        except Exception as e:
            self.logger.error(f"Error guardando resultados: {e}")
            return False

# Singleton instance
redteam_core = None

def get_core_instance(config_file="config.yaml"):
    """Obtener instancia singleton del core"""
    global redteam_core
    if redteam_core is None:
        redteam_core = FiveGRedTeamCore(config_file)
    return redteam_core