import ctypes
import numpy as np
from typing import List, Tuple, Optional
import json

class IQSample(ctypes.Structure):
    _fields_ = [("i", ctypes.c_float),
                ("q", ctypes.c_float),
                ("timestamp", ctypes.c_uint64)]

class Peak(ctypes.Structure):
    _fields_ = [("frequency", ctypes.c_float),
                ("power", ctypes.c_float),
                ("bandwidth", ctypes.c_float)]

class RustRFProcessor:
    def __init__(self, lib_path: str):
        self.lib = ctypes.CDLL(lib_path)
        
        # Definir tipos de funciones
        self.lib.create_spectrum_analyzer.argtypes = [ctypes.c_float, ctypes.c_size_t]
        self.lib.create_spectrum_analyzer.restype = ctypes.c_void_p
        
        self.lib.free_spectrum_analyzer.argtypes = [ctypes.c_void_p]
        self.lib.free_spectrum_analyzer.restype = None
        
        self.lib.process_iq_data.argtypes = [
            ctypes.c_void_p,  # analyzer
            ctypes.POINTER(IQSample),  # iq_samples
            ctypes.c_size_t,  # length
            ctypes.c_float  # threshold
        ]
        self.lib.process_iq_data.restype = ctypes.c_void_p
        
        self.lib.free_process_result.argtypes = [ctypes.c_void_p]
        self.lib.free_process_result.restype = None
    
    def create_analyzer(self, sample_rate: float, fft_size: int):
        return self.lib.create_spectrum_analyzer(
            ctypes.c_float(sample_rate),
            ctypes.c_size_t(fft_size)
        )
    
    def free_analyzer(self, analyzer_ptr):
        self.lib.free_spectrum_analyzer(analyzer_ptr)
    
    def process_iq_data(self, analyzer_ptr, iq_data: np.ndarray, threshold: float = -50.0):
        # Convertir numpy array a IQSample
        iq_samples = (IQSample * len(iq_data))()
        
        for i, sample in enumerate(iq_data):
            iq_samples[i].i = sample.real
            iq_samples[i].q = sample.imag
            iq_samples[i].timestamp = i
        
        # Procesar con Rust
        result_ptr = self.lib.process_iq_data(
            analyzer_ptr,
            iq_samples,
            ctypes.c_size_t(len(iq_data)),
            ctypes.c_float(threshold)
        )
        
        if not result_ptr:
            return None
        
        # Obtener resultados
        class ProcessResult(ctypes.Structure):
            _fields_ = [("spectrum", ctypes.POINTER(ctypes.c_float * 2)),
                       ("peaks", ctypes.POINTER(Peak)),
                       ("spectrum_length", ctypes.c_size_t),
                       ("peaks_length", ctypes.c_size_t)]
        
        result = ctypes.cast(result_ptr, ctypes.POINTER(ProcessResult)).contents
        
        # Convertir a Python
        spectrum = []
        for i in range(result.spectrum_length):
            freq_power = result.spectrum[i]
            spectrum.append((freq_power[0], freq_power[1]))
        
        peaks = []
        for i in range(result.peaks_length):
            peak = result.peaks[i]
            peaks.append({
                'frequency': peak.frequency,
                'power': peak.power,
                'bandwidth': peak.bandwidth
            })
        
        # Liberar memoria
        self.lib.free_process_result(result_ptr)
        
        return {'spectrum': spectrum, 'peaks': peaks}