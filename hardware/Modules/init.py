"""
Módulos principales del sistema 5G RF RedTeam
"""
from .pentesting.fiveg_attacks import FiveGAttacks
from .rf.sdr_controller import SDRController, SDRType
from .security.threat_detection import ThreatDetector
from .analysis.packet_analyzer import FiveGPacketAnalyzer

class ModulesManager:
    def __init__(self, core):
        self.core = core
        self.logger = core.logger
        self.modules = {}
        
    def initialize_modules(self):
        """Inicializar todos los módulos"""
        try:
            # Módulo de ataques
            self.modules['attacks'] = FiveGAttacks(self.core)
            self.logger.info("Módulo de ataques inicializado")
            
            # Controlador SDR
            self.modules['sdr'] = SDRController(SDRType.HACKRF)
            if self.modules['sdr'].initialize():
                self.logger.info("Controlador SDR inicializado")
            
            # Detección de amenazas
            self.modules['threat_detection'] = ThreatDetector(self.core)
            self.logger.info("Detección de amenazas inicializada")
            
            # Analizador de paquetes
            self.modules['packet_analyzer'] = FiveGPacketAnalyzer(self.core)
            self.logger.info("Analizador de paquetes inicializado")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error inicializando módulos: {e}")
            return False
    
    def get_module(self, module_name):
        """Obtener módulo por nombre"""
        return self.modules.get(module_name)
    
    def get_all_modules(self):
        """Obtener todos los módulos"""
        return self.modules
    
    def shutdown(self):
        """Apagar todos los módulos"""
        for name, module in self.modules.items():
            if hasattr(module, 'stop_all_attacks'):
                module.stop_all_attacks()
            if hasattr(module, 'stop_streaming'):
                module.stop_streaming()
        
        self.logger.info("Todos los módulos apagados")