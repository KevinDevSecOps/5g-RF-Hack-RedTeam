import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import logging
from datetime import datetime
import threading
import time

class SpectrumAnalyzer:
    def __init__(self, sample_rate=20e6, fft_size=1024, averaging=10):
        self.sample_rate = sample_rate
        self.fft_size = fft_size
        self.averaging = averaging
        self.spectrum_data = None
        self.is_scanning = False
        self.logger = logging.getLogger(__name__)
        self.lock = threading.Lock()
        
    def start_continuous_scan(self, callback=None):
        """Iniciar scanning continuo en segundo plano"""
        self.is_scanning = True
        self.logger.info("Iniciando scanning continuo de espectro")
        
        def scan_loop():
            while self.is_scanning:
                try:
                    # Simular datos IQ (en producción, leer de SDR)
                    iq_data = self.simulate_iq_data()
                    analysis = self.analyze_spectrum(iq_data)
                    
                    with self.lock:
                        self.spectrum_data = analysis
                    
                    if callback and analysis:
                        callback(analysis)
                        
                    time.sleep(0.1)  # 10 FPS
                    
                except Exception as e:
                    self.logger.error(f"Error en scanning: {e}")
                    time.sleep(1)
        
        thread = threading.Thread(target=scan_loop, daemon=True)
        thread.start()
        return thread
    
    def stop_continuous_scan(self):
        """Detener scanning continuo"""
        self.is_scanning = False
        self.logger.info("Scanning continuo detenido")
    
    def simulate_iq_data(self):
        """Simular datos IQ para testing (reemplazar con SDR real)"""
        # Simular señal 5G alrededor de 3.5GHz
        t = np.linspace(0, 1, self.fft_size)
        carrier_freq = 3.5e9
        
        # Señal principal + interferencia + ruido
        signal_iq = np.exp(2j * np.pi * carrier_freq * t)
        interference = 0.3 * np.exp(2j * np.pi * (carrier_freq + 10e6) * t)
        noise = 0.1 * (np.random.randn(self.fft_size) + 1j * np.random.randn(self.fft_size))
        
        return signal_iq + interference + noise
    
    def analyze_spectrum(self, iq_data):
        """Analizar espectro de datos IQ"""
        try:
            if len(iq_data) < self.fft_size:
                self.logger.warning(f"Datos IQ insuficientes: {len(iq_data)} < {self.fft_size}")
                return None
            
            # Calcular FFT
            fft_data = np.fft.fftshift(np.fft.fft(iq_data, self.fft_size))
            freq_axis = np.fft.fftshift(np.fft.fftfreq(self.fft_size, 1/self.sample_rate))
            
            # Calcular densidad espectral de potencia
            f, Pxx = signal.welch(iq_data, self.sample_rate, nperseg=self.fft_size)
            
            # Detectar picos
            peaks = self.detect_peaks(fft_data, freq_axis)
            
            return {
                'timestamp': datetime.now().isoformat(),
                'frequencies': freq_axis.tolist(),
                'spectrum': (20 * np.log10(np.abs(fft_data) + 1e-10)).tolist(),
                'psd_freq': f.tolist(),
                'psd': (10 * np.log10(Pxx + 1e-10)).tolist(),
                'peaks': peaks,
                'sample_rate': self.sample_rate,
                'fft_size': self.fft_size
            }
        except Exception as e:
            self.logger.error(f"Error en análisis de espectro: {e}")
            return None
    
    def detect_peaks(self, spectrum_data, frequencies, threshold=-50):
        """Detectar picos en el espectro"""
        from scipy.signal import find_peaks
        
        power_dB = 20 * np.log10(np.abs(spectrum_data) + 1e-10)
        peaks, properties = find_peaks(power_dB, height=threshold, distance=10)
        
        detected_peaks = []
        for peak in peaks:
            detected_peaks.append({
                'frequency': float(frequencies[peak]),
                'power': float(power_dB[peak]),
                'bandwidth': self.estimate_bandwidth(power_dB, peak)
            })
        
        return detected_peaks
    
    def estimate_bandwidth(self, power_dB, peak_index, threshold_db=3):
        """Estimar ancho de banda alrededor del pico"""
        peak_power = power_dB[peak_index]
        threshold = peak_power - threshold_db
        
        # Buscar hacia la izquierda
        left_idx = peak_index
        while left_idx > 0 and power_dB[left_idx] > threshold:
            left_idx -= 1
        
        # Buscar hacia la derecha
        right_idx = peak_index
        while right_idx < len(power_dB) - 1 and power_dB[right_idx] > threshold:
            right_idx += 1
        
        bandwidth = (right_idx - left_idx) * (self.sample_rate / self.fft_size)
        return float(bandwidth)
    
    def plot_spectrum(self, analysis_result, save_path=None):
        """Generar gráfico del espectro"""
        try:
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
            
            # Espectro FFT
            ax1.plot(analysis_result['frequencies'], analysis_result['spectrum'])
            ax1.set_title('Espectro de Frecuencia - 5G RF Analysis')
            ax1.set_xlabel('Frecuencia (Hz)')
            ax1.set_ylabel('Potencia (dB)')
            ax1.grid(True)
            
            # Marcar picos
            for peak in analysis_result['peaks']:
                ax1.axvline(x=peak['frequency'], color='r', linestyle='--', alpha=0.7)
                ax1.text(peak['frequency'], peak['power'], f"{peak['frequency']/1e9:.2f}GHz", 
                        rotation=90, verticalalignment='bottom')
            
            # Densidad espectral de potencia
            ax2.plot(analysis_result['psd_freq'], analysis_result['psd'])
            ax2.set_title('Densidad Espectral de Potencia (PSD)')
            ax2.set_xlabel('Frecuencia (Hz)')
            ax2.set_ylabel('PSD (dB/Hz)')
            ax2.grid(True)
            
            plt.tight_layout()
            
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
                self.logger.info(f"Gráfico guardado en: {save_path}")
            
            return fig
        except Exception as e:
            self.logger.error(f"Error generando gráfico: {e}")
            return None