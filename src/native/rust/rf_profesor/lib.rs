use num_complex::Complex32;
use rustfft::FftPlanner;
use std::f32::consts::PI;
use std::os::raw::c_float;

#[repr(C)]
pub struct IQSample {
    pub i: c_float,
    pub q: c_float,
    pub timestamp: u64,
}

#[repr(C)]
pub struct SpectrumResult {
    pub frequencies: *mut c_float,
    pub spectrum: *mut c_float,
    pub length: usize,
    pub sample_rate: c_float,
}

#[no_mangle]
pub extern "C" fn create_spectrum_analyzer(sample_rate: c_float, fft_size: usize) -> *mut SpectrumAnalyzer {
    let analyzer = SpectrumAnalyzer::new(sample_rate, fft_size);
    Box::into_raw(Box::new(analyzer))
}

#[no_mangle]
pub extern "C" fn free_spectrum_analyzer(analyzer: *mut SpectrumAnalyzer) {
    if !analyzer.is_null() {
        unsafe { Box::from_raw(analyzer) };
    }
}

pub struct SpectrumAnalyzer {
    sample_rate: f32,
    fft_size: usize,
    fft_planner: FftPlanner<f32>,
}

impl SpectrumAnalyzer {
    pub fn new(sample_rate: f32, fft_size: usize) -> Self {
        Self {
            sample_rate,
            fft_size,
            fft_planner: FftPlanner::new(),
        }
    }

    pub fn process_iq_data(&mut self, iq_data: &[IQSample]) -> Vec<(f32, f32)> {
        if iq_data.len() < self.fft_size {
            return Vec::new();
        }

        // Convertir a complejos
        let mut complex_data: Vec<Complex32> = iq_data[..self.fft_size]
            .iter()
            .map(|s| Complex32::new(s.i, s.q))
            .collect();

        // Aplicar ventana de Hanning
        self.apply_hann_window(&mut complex_data);

        // Calcular FFT
        let fft = self.fft_planner.plan_fft_forward(self.fft_size);
        fft.process(&mut complex_data);

        // Calcular espectro de potencia
        let spectrum: Vec<f32> = complex_data
            .iter()
            .map(|c| 10.0 * c.norm().log10())
            .collect();

        // Calcular frecuencias
        let frequencies: Vec<f32> = (0..self.fft_size)
            .map(|i| {
                let freq = i as f32 * self.sample_rate / self.fft_size as f32;
                if i > self.fft_size / 2 {
                    freq - self.sample_rate
                } else {
                    freq
                }
            })
            .collect();

        frequencies.into_iter().zip(spectrum).collect()
    }

    fn apply_hann_window(&self, data: &mut [Complex32]) {
        for (i, sample) in data.iter_mut().enumerate() {
            let window = 0.5 * (1.0 - (2.0 * PI * i as f32 / (self.fft_size as f32 - 1.0)).cos());
            *sample = *sample * window;
        }
    }

    pub fn detect_peaks(&self, spectrum: &[(f32, f32)], threshold: f32) -> Vec<Peak> {
        let mut peaks = Vec::new();
        
        for i in 1..spectrum.len() - 1 {
            let (freq, power) = spectrum[i];
            let (prev_freq, prev_power) = spectrum[i - 1];
            let (next_freq, next_power) = spectrum[i + 1];
            
            if power > threshold && power > prev_power && power > next_power {
                peaks.push(Peak {
                    frequency: freq,
                    power,
                    bandwidth: self.estimate_bandwidth(spectrum, i),
                });
            }
        }
        
        peaks
    }

    fn estimate_bandwidth(&self, spectrum: &[(f32, f32)], peak_index: usize) -> f32 {
        let (center_freq, center_power) = spectrum[peak_index];
        let threshold = center_power - 3.0; // -3 dB points
        
        let mut left_idx = peak_index;
        while left_idx > 0 && spectrum[left_idx].1 > threshold {
            left_idx -= 1;
        }
        
        let mut right_idx = peak_index;
        while right_idx < spectrum.len() - 1 && spectrum[right_idx].1 > threshold {
            right_idx += 1;
        }
        
        spectrum[right_idx].0 - spectrum[left_idx].0
    }
}

#[repr(C)]
pub struct Peak {
    pub frequency: c_float,
    pub power: c_float,
    pub bandwidth: c_float,
}

#[no_mangle]
pub extern "C" fn process_iq_data(
    analyzer: *mut SpectrumAnalyzer,
    iq_samples: *const IQSample,
    length: usize,
    threshold: c_float,
) -> *mut ProcessResult {
    if analyzer.is_null() || iq_samples.is_null() {
        return std::ptr::null_mut();
    }

    unsafe {
        let analyzer = &mut *analyzer;
        let iq_slice = std::slice::from_raw_parts(iq_samples, length);
        
        let spectrum = analyzer.process_iq_data(iq_slice);
        let peaks = analyzer.detect_peaks(&spectrum, threshold);
        
        Box::into_raw(Box::new(ProcessResult { spectrum, peaks }))
    }
}

#[repr(C)]
pub struct ProcessResult {
    pub spectrum: Vec<(f32, f32)>,
    pub peaks: Vec<Peak>,
}

#[no_mangle]
pub extern "C" fn free_process_result(result: *mut ProcessResult) {
    if !result.is_null() {
        unsafe { Box::from_raw(result) };
    }
}