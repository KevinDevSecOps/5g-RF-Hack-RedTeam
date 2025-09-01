"""
Extracción avanzada de características de señales 5G
"""
import numpy as np
from scipy import signal, stats
import pywt

class AdvancedFeatureExtractor:
    def __init__(self):
        self.features_cache = {}
    
    def extract_comprehensive_features(self, iq_data, sample_rate=20e6):
        """
        Extraer características comprehensivas de señales IQ
        """
        features = {}
        
        # Dominio de tiempo
        features.update(self._extract_time_domain_features(iq_data))
        
        # Dominio de frecuencia
        features.update(self._extract_frequency_domain_features(iq_data, sample_rate))
        
        # Estadísticas avanzadas
        features.update(self._extract_statistical_features(iq_data))
        
        # Características espectrales
        features.update(self._extract_spectral_features(iq_data, sample_rate))
        
        # Transformada wavelet
        features.update(self._extract_wavelet_features(iq_data))
        
        return features
    
    def _extract_time_domain_features(self, iq_data):
        """Características en dominio de tiempo"""
        magnitude = np.abs(iq_data)
        phase = np.unwrap(np.angle(iq_data))
        
        return {
            'mean_magnitude': np.mean(magnitude),
            'std_magnitude': np.std(magnitude),
            'skew_magnitude': stats.skew(magnitude),
            'kurtosis_magnitude': stats.kurtosis(magnitude),
            'rms': np.sqrt(np.mean(magnitude**2)),
            'crest_factor': np.max(magnitude) / np.sqrt(np.mean(magnitude**2)) if np.mean(magnitude**2) > 0 else 0,
            'mean_phase': np.mean(phase),
            'phase_std': np.std(phase)
        }
    
    def _extract_frequency_domain_features(self, iq_data, sample_rate):
        """Características en dominio de frecuencia"""
        fft = np.fft.fft(iq_data)
        fft_mag = np.abs(fft)
        freqs = np.fft.fftfreq(len(iq_data), 1/sample_rate)
        
        # Tomar solo frecuencias positivas
        positive_freqs = freqs[:len(freqs)//2]
        positive_fft = fft_mag[:len(fft_mag)//2]
        
        return {
            'spectral_centroid': np.sum(positive_freqs * positive_fft) / np.sum(positive_fft) if np.sum(positive_fft) > 0 else 0,
            'spectral_bandwidth': np.sqrt(np.sum((positive_freqs - np.sum(positive_freqs * positive_fft)/np.sum(positive_fft))**2 * positive_fft) / np.sum(positive_fft)) if np.sum(positive_fft) > 0 else 0,
            'spectral_flatness': stats.gmean(positive_fft) / np.mean(positive_fft) if np.mean(positive_fft) > 0 else 0,
            'spectral_rolloff': self._calculate_spectral_rolloff(positive_freqs, positive_fft, 0.85)
        }
    
    def _calculate_spectral_rolloff(self, freqs, magnitudes, percentile=0.85):
        """Calcular spectral rolloff"""
        total_energy = np.sum(magnitudes**2)
        cumulative_energy = np.cumsum(magnitudes**2)
        rolloff_index = np.where(cumulative_energy >= percentile * total_energy)[0]
        
        if len(rolloff_index) > 0:
            return freqs[rolloff_index[0]]
        return 0
    
    def _extract_statistical_features(self, iq_data):
        """Características estadísticas"""
        real_part = np.real(iq_data)
        imag_part = np.imag(iq_data)
        
        return {
            'real_mean': np.mean(real_part),
            'real_std': np.std(real_part),
            'imag_mean': np.mean(imag_part),
            'imag_std': np.std(imag_part),
            'iq_correlation': np.corrcoef(real_part, imag_part)[0, 1] if len(real_part) > 1 else 0
        }
    
    def _extract_spectral_features(self, iq_data, sample_rate):
        """Características espectrales avanzadas"""
        f, Pxx = signal.welch(iq_data, sample_rate, nperseg=1024)
        
        return {
            'psd_mean': np.mean(Pxx),
            'psd_std': np.std(Pxx),
            'psd_max': np.max(Pxx),
            'psd_peak_freq': f[np.argmax(Pxx)]
        }
    
    def _extract_wavelet_features(self, iq_data):
        """Características wavelet"""
        try:
            # Usar wavelet Daubechies 4
            coeffs = pywt.wavedec(np.abs(iq_data), 'db4', level=3)
            
            wavelet_features = {}
            for i, coeff in enumerate(coeffs):
                if len(coeff) > 0:
                    wavelet_features[f'wavelet_l{i}_mean'] = np.mean(coeff)
                    wavelet_features[f'wavelet_l{i}_std'] = np.std(coeff)
                    wavelet_features[f'wavelet_l{i}_energy'] = np.sum(coeff**2)
            
            return wavelet_features
            
        except Exception as e:
            return {'wavelet_error': str(e)}