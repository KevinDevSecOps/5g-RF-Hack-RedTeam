"""
Analizador de paquetes para protocolos 5G
"""
import logging
import dpkt
import numpy as np
from collections import defaultdict
from datetime import datetime

logger = logging.getLogger(__name__)

class FiveGPacketAnalyzer:
    def __init__(self, core):
        self.core = core
        self.logger = logger
        self.packet_count = 0
        self.protocol_stats = defaultdict(int)
        self.anomalies_detected = 0
        
    def analyze_pcap(self, pcap_file):
        """Analizar archivo pcap de tráfico 5G"""
        results = {
            'total_packets': 0,
            'protocols': {},
            'timeline': [],
            'anomalies': []
        }
        
        try:
            with open(pcap_file, 'rb') as f:
                pcap = dpkt.pcap.Reader(f)
                
                for timestamp, buf in pcap:
                    results['total_packets'] += 1
                    self.packet_count += 1
                    
                    # Analizar paquete
                    packet_info = self.analyze_packet(buf, timestamp)
                    results['timeline'].append(packet_info)
                    
                    # Estadísticas por protocolo
                    protocol = packet_info.get('protocol', 'unknown')
                    results['protocols'][protocol] = results['protocols'].get(protocol, 0) + 1
                    
                    # Detectar anomalías
                    if self.detect_packet_anomaly(packet_info):
                        results['anomalies'].append(packet_info)
                        self.anomalies_detected += 1
            
            self.logger.info(f"Análisis completado: {results['total_packets']} paquetes procesados")
            return results
            
        except Exception as e:
            self.logger.error(f"Error analizando pcap: {e}")
            return results
    
    def analyze_packet(self, packet_data, timestamp):
        """Analizar paquete individual"""
        try:
            eth = dpkt.ethernet.Ethernet(packet_data)
            
            packet_info = {
                'timestamp': datetime.fromtimestamp(timestamp).isoformat(),
                'length': len(packet_data),
                'source': '',
                'destination': '',
                'protocol': 'unknown'
            }
            
            # IP packet
            if isinstance(eth.data, dpkt.ip.IP):
                ip = eth.data
                packet_info['source'] = self.inet_to_str(ip.src)
                packet_info['destination'] = self.inet_to_str(ip.dst)
                
                # TCP
                if isinstance(ip.data, dpkt.tcp.TCP):
                    packet_info['protocol'] = 'TCP'
                    packet_info['src_port'] = ip.data.sport
                    packet_info['dst_port'] = ip.data.dport
                
                # UDP
                elif isinstance(ip.data, dpkt.udp.UDP):
                    packet_info['protocol'] = 'UDP'
                    packet_info['src_port'] = ip.data.sport
                    packet_info['dst_port'] = ip.data.dport
                    
                    # Posible protocolo 5G (GTP-U, etc.)
                    if ip.data.dport in [2152, 2123]:  # Puertos comunes 5G
                        packet_info['protocol'] = 'GTP-U'
            
            return packet_info
            
        except Exception as e:
            self.logger.debug(f"Error analizando paquete: {e}")
            return {
                'timestamp': datetime.fromtimestamp(timestamp).isoformat(),
                'length': len(packet_data),
                'protocol': 'unknown',
                'error': str(e)
            }
    
    def inet_to_str(self, inet):
        """Convertir dirección de red a string"""
        try:
            return '.'.join(str(b) for b in inet)
        except:
            return 'unknown'
    
    def detect_packet_anomaly(self, packet_info):
        """Detectar anomalías en paquetes"""
        anomalies = []
        
        # Paquetes muy grandes
        if packet_info['length'] > 1500:
            anomalies.append('oversized_packet')
        
        # Puertos sospechosos
        if packet_info.get('dst_port', 0) in [12345, 31337, 4444]:
            anomalies.append('suspicious_port')
        
        # Protocolo desconocido con mucho tráfico
        if packet_info['protocol'] == 'unknown' and packet_info['length'] > 100:
            anomalies.append('unknown_protocol_large')
        
        return len(anomalies) > 0
    
    def real_time_analysis(self, packet_callback):
        """Análisis en tiempo real (simulado)"""
        self.logger.info("Iniciando análisis en tiempo real")
        
        # Simular captura de paquetes
        while True:
            try:
                # Simular paquete (en producción sería captura real)
                simulated_packet = self.generate_simulated_packet()
                analysis = self.analyze_packet(simulated_packet, time.time())
                
                if packet_callback:
                    packet_callback(analysis)
                
                time.sleep(0.1)
                
            except Exception as e:
                self.logger.error(f"Error en análisis tiempo real: {e}")
                break
    
    def generate_simulated_packet(self):
        """Generar paquete simulado para testing"""
        # Simular paquete Ethernet/IP/UDP
        # En producción, esto vendría de una captura real
        return b'\x00' * 100  # Paquete simulado