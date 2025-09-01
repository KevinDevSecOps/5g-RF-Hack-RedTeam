"""
Clasificación de señales 5G usando Deep Learning
"""
import logging
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import joblib

logger = logging.getLogger(__name__)

class SignalClassifier:
    def __init__(self, core):
        self.core = core
        self.logger = logger
        self.model = None
        self.label_encoder = LabelEncoder()
        self.classes = []
        self.is_trained = False
    
    def generate_training_data(self, num_samples=1000):
        """
        Generar datos de entrenamiento simulados para diferentes tipos de señales 5G
        """
        signals = []
        labels = []
        
        signal_types = [
            '5g_nr', 'lte', 'wifi', 'bluetooth', 'jamming', 'noise'
        ]
        
        for signal_type in signal_types:
            for _ in range(num_samples // len(signal_types)):
                iq_data = self.generate_signal(signal_type)
                features = self.extract_signal_features(iq_data)
                signals.append(features)
                labels.append(signal_type)
        
        return np.array(signals), np.array(labels)
    
    def generate_signal(self, signal_type, length=1024):
        """
        Generar diferentes tipos de señales para entrenamiento
        """
        t = np.linspace(0, 1, length)
        
        if signal_type == '5g_nr':
            # Señal 5G NR con OFDM
            carrier = np.exp(2j * np.pi * 3.5e9 * t)
            modulation = np.sin(2 * np.pi * 100e6 * t)  # Modulación
            return carrier * modulation + 0.1 * np.random.randn(length)
        
        elif signal_type == 'lte':
            # Señal LTE
            return np.exp(2j * np.pi * 2.6e9 * t) + 0.2 * np.random.randn(length)
        
        elif signal_type == 'wifi':
            # Señal WiFi (OFDM)
            return np.exp(2j * np.pi * 2.4e9 * t) * np.sin(2 * np.pi * 20e6 * t)
        
        elif signal_type == 'bluetooth':
            # Señal Bluetooth (FHSS)
            return np.exp(2j * np.pi * 2.4e9 * t) * (np.random.randn(length) > 0)
        
        elif signal_type == 'jamming':
            # Señal de jamming (ruido de banda ancha)
            return np.random.randn(length) + 1j * np.random.randn(length)
        
        else:  # noise
            # Ruido puro
            return 0.1 * (np.random.randn(length) + 1j * np.random.randn(length))
    
    def extract_signal_features(self, iq_data, num_features=20):
        """
        Extraer características de señales para clasificación
        """
        # Características en dominio de tiempo
        magnitude = np.abs(iq_data)
        phase = np.angle(iq_data)
        
        time_features = [
            np.mean(magnitude), np.std(magnitude), np.skew(magnitude), np.kurtosis(magnitude),
            np.mean(phase), np.std(phase)
        ]
        
        # Características en dominio de frecuencia
        fft = np.fft.fft(iq_data)
        fft_mag = np.abs(fft)
        fft_freq = np.fft.fftfreq(len(iq_data))
        
        spectral_features = [
            np.mean(fft_mag), np.std(fft_mag), np.max(fft_mag),
            np.sum(fft_mag**2),  # Energía
            np.argmax(fft_mag) / len(iq_data)  # Frecuencia dominante normalizada
        ]
        
        # Características estadísticas avanzadas
        spectral_centroid = np.sum(fft_freq * fft_mag) / np.sum(fft_mag)
        spectral_bandwidth = np.sqrt(np.sum((fft_freq - spectral_centroid)**2 * fft_mag) / np.sum(fft_mag))
        
        advanced_features = [spectral_centroid, spectral_bandwidth]
        
        # Combinar todas las características
        all_features = time_features + spectral_features + advanced_features
        
        # Asegurar número consistente de características
        if len(all_features) < num_features:
            all_features.extend([0] * (num_features - len(all_features)))
        else:
            all_features = all_features[:num_features]
        
        return all_features
    
    def build_model(self, input_dim, num_classes):
        """
        Construir modelo de Deep Learning para clasificación
        """
        model = keras.Sequential([
            layers.Dense(128, activation='relu', input_shape=(input_dim,)),
            layers.Dropout(0.3),
            layers.Dense(64, activation='relu'),
            layers.Dropout(0.3),
            layers.Dense(32, activation='relu'),
            layers.Dropout(0.2),
            layers.Dense(num_classes, activation='softmax')
        ])
        
        model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def train(self, X, y, test_size=0.2, epochs=100):
        """
        Entrenar el clasificador
        """
        try:
            # Codificar labels
            y_encoded = self.label_encoder.fit_transform(y)
            self.classes = self.label_encoder.classes_
            
            # Dividir datos
            X_train, X_test, y_train, y_test = train_test_split(
                X, y_encoded, test_size=test_size, random_state=42
            )
            
            # Construir y entrenar modelo
            self.model = self.build_model(X_train.shape[1], len(self.classes))
            
            history = self.model.fit(
                X_train, y_train,
                epochs=epochs,
                batch_size=32,
                validation_data=(X_test, y_test),
                verbose=1,
                callbacks=[
                    keras.callbacks.EarlyStopping(patience=10, restore_best_weights=True),
                    keras.callbacks.ReduceLROnPlateau(factor=0.5, patience=5)
                ]
            )
            
            # Evaluar modelo
            test_loss, test_acc = self.model.evaluate(X_test, y_test, verbose=0)
            self.logger.info(f"Precisión en test: {test_acc:.4f}")
            
            self.is_trained = True
            return history
            
        except Exception as e:
            self.logger.error(f"Error entrenando clasificador: {e}")
            return None
    
    def predict_signal_type(self, iq_data):
        """
        Predecir el tipo de señal
        """
        if not self.is_trained:
            self.logger.warning("Modelo no entrenado")
            return "unknown", 0.0
        
        try:
            features = self.extract_signal_features(iq_data)
            features = np.array([features])
            
            predictions = self.model.predict(features, verbose=0)
            predicted_class_idx = np.argmax(predictions[0])
            confidence = np.max(predictions[0])
            
            predicted_class = self.label_encoder.inverse_transform([predicted_class_idx])[0]
            
            return predicted_class, float(confidence)
            
        except Exception as e:
            self.logger.error(f"Error prediciendo tipo de señal: {e}")
            return "error", 0.0
    
    def save_model(self, filepath):
        """Guardar modelo entrenado"""
        try:
            self.model.save(filepath)
            joblib.dump({
                'label_encoder': self.label_encoder,
                'classes': self.classes,
                'is_trained': self.is_trained
            }, filepath.replace('.h5', '_meta.pkl'))
            
            self.logger.info(f"Modelo guardado en {filepath}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error guardando modelo: {e}")
            return False
    
    def load_model(self, filepath):
        """Cargar modelo entrenado"""
        try:
            self.model = keras.models.load_model(filepath)
            meta_data = joblib.load(filepath.replace('.h5', '_meta.pkl'))
            
            self.label_encoder = meta_data['label_encoder']
            self.classes = meta_data['classes']
            self.is_trained = meta_data['is_trained']
            
            self.logger.info("Modelo cargado exitosamente")
            return True
            
        except Exception as e:
            self.logger.error(f"Error cargando modelo: {e}")
            return False