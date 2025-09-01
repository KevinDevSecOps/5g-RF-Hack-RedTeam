"""
Detección de anomalías usando Machine Learning avanzado
"""
import logging
import numpy as np
import joblib
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.svm import OneClassSVM
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import warnings
warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)

class AdvancedAnomalyDetector:
    def __init__(self, core):
        self.core = core
        self.logger = logger
        self.scaler = StandardScaler()
        self.pca = PCA(n_components=0.95)
        self.models = {}
        self.is_trained = False
        
    def extract_advanced_features(self, spectrum_data):
        """
        Extraer características avanzadas para ML
        """
        features = []
        
        power = np.array(spectrum_data['spectrum'])
        frequencies = np.array(spectrum_data['frequencies'])
        
        # Características estadísticas
        stats_features = [
            np.mean(power), np.std(power), np.min(power), np.max(power),
            np.median(power), np.percentile(power, 25), np.percentile(power, 75),
            np.skew(power), np.kurtosis(power)
        ]
        
        # Características espectrales
        fft = np.fft.fft(power)
        spectral_features = [
            np.mean(np.abs(fft)), np.std(np.abs(fft)),
            np.max(np.abs(fft)), np.sum(np.abs(fft)**2)  # Energía
        ]
        
        # Características de dominio de frecuencia
        spectral_centroid = np.sum(frequencies * np.abs(power)) / np.sum(np.abs(power))
        spectral_bandwidth = np.sqrt(np.sum((frequencies - spectral_centroid)**2 * np.abs(power)) / np.sum(np.abs(power)))
        
        # Combinar todas las características
        all_features = stats_features + spectral_features + [spectral_centroid, spectral_bandwidth]
        
        return all_features
    
    def train_models(self, training_data):
        """
        Entrenar modelos de ML con datos de entrenamiento
        """
        try:
            if not training_data or len(training_data) < 100:
                self.logger.warning("Datos de entrenamiento insuficientes")
                return False
            
            # Preparar datos
            X = np.array([self.extract_advanced_features(data) for data in training_data])
            X_scaled = self.scaler.fit_transform(X)
            X_pca = self.pca.fit_transform(X_scaled)
            
            # Entrenar Isolation Forest
            self.models['isolation_forest'] = IsolationForest(
                contamination=0.1, 
                random_state=42,
                n_estimators=100
            )
            self.models['isolation_forest'].fit(X_pca)
            
            # Entrenar One-Class SVM
            self.models['one_class_svm'] = OneClassSVM(
                nu=0.1, 
                kernel='rbf', 
                gamma='scale'
            )
            self.models['one_class_svm'].fit(X_pca)
            
            # Entrenar Autoencoder para detección de anomalías
            self.train_autoencoder(X_scaled)
            
            self.is_trained = True
            self.logger.info("Modelos de ML entrenados exitosamente")
            return True
            
        except Exception as e:
            self.logger.error(f"Error entrenando modelos: {e}")
            return False
    
    def train_autoencoder(self, X):
        """
        Entrenar autoencoder para detección de anomalías
        """
        input_dim = X.shape[1]
        
        # Arquitectura del autoencoder
        encoder = keras.Sequential([
            layers.Dense(64, activation='relu', input_shape=(input_dim,)),
            layers.Dense(32, activation='relu'),
            layers.Dense(16, activation='relu')
        ])
        
        decoder = keras.Sequential([
            layers.Dense(32, activation='relu', input_shape=(16,)),
            layers.Dense(64, activation='relu'),
            layers.Dense(input_dim, activation='linear')
        ])
        
        autoencoder = keras.Sequential([encoder, decoder])
        autoencoder.compile(optimizer='adam', loss='mse')
        
        # Entrenamiento
        autoencoder.fit(
            X, X,
            epochs=50,
            batch_size=32,
            shuffle=True,
            validation_split=0.2,
            verbose=0
        )
        
        self.models['autoencoder'] = autoencoder
        self.models['encoder'] = encoder
    
    def detect_anomalies_advanced(self, spectrum_data):
        """
        Detectar anomalías usando múltiples modelos de ML
        """
        if not self.is_trained:
            self.logger.warning("Modelos no entrenados, usando detección básica")
            return self.detect_anomalies_basic(spectrum_data)
        
        try:
            # Extraer características
            features = self.extract_advanced_features(spectrum_data)
            X_scaled = self.scaler.transform([features])
            X_pca = self.pca.transform(X_scaled)
            
            # Predecir con todos los modelos
            results = {}
            
            # Isolation Forest
            iforest_pred = self.models['isolation_forest'].predict(X_pca)[0]
            iforest_score = self.models['isolation_forest'].decision_function(X_pca)[0]
            results['isolation_forest'] = {
                'anomaly': iforest_pred == -1,
                'score': float(iforest_score)
            }
            
            # One-Class SVM
            svm_pred = self.models['one_class_svm'].predict(X_pca)[0]
            svm_score = self.models['one_class_svm'].decision_function(X_pca)[0]
            results['one_class_svm'] = {
                'anomaly': svm_pred == -1,
                'score': float(svm_score)
            }
            
            # Autoencoder (reconstruction error)
            reconstructed = self.models['autoencoder'].predict(X_scaled, verbose=0)
            reconstruction_error = np.mean(np.square(X_scaled - reconstructed))
            results['autoencoder'] = {
                'anomaly': reconstruction_error > 0.1,  # Threshold
                'score': float(reconstruction_error)
            }
            
            # Votación mayoritaria
            anomaly_votes = sum(1 for model in results.values() if model['anomaly'])
            is_anomaly = anomaly_votes >= 2  # Al menos 2 modelos detectan anomalía
            
            return {
                'is_anomaly': is_anomaly,
                'models_results': results,
                'confidence': self.calculate_confidence(results)
            }
            
        except Exception as e:
            self.logger.error(f"Error en detección avanzada: {e}")
            return {'is_anomaly': False, 'error': str(e)}
    
    def calculate_confidence(self, results):
        """Calcular confianza basada en resultados de modelos"""
        scores = []
        for model_name, result in results.items():
            if model_name == 'autoencoder':
                # Para autoencoder, score más bajo = mejor
                score = 1.0 - min(result['score'] / 0.2, 1.0)  # Normalizar
            else:
                # Para otros modelos, score más negativo = más anómalo
                score = min(max(-result['score'] / 2.0, 0.0), 1.0)
            scores.append(score)
        
        return float(np.mean(scores))
    
    def detect_anomalies_basic(self, spectrum_data):
        """Detección básica de anomalías (fallback)"""
        power = np.array(spectrum_data['spectrum'])
        
        # Detección simple basada en threshold
        mean_power = np.mean(power)
        std_power = np.std(power)
        
        anomalies = []
        for i, pwr in enumerate(power):
            if abs(pwr - mean_power) > 3 * std_power:  # 3 sigma
                anomalies.append({
                    'frequency': spectrum_data['frequencies'][i],
                    'power': pwr,
                    'deviation': abs(pwr - mean_power) / std_power
                })
        
        return {
            'is_anomaly': len(anomalies) > 0,
            'anomalies': anomalies,
            'confidence': min(len(anomalies) / 10.0, 1.0)  # Confianza basada en cantidad
        }
    
    def save_models(self, filepath):
        """Guardar modelos entrenados"""
        try:
            model_data = {
                'scaler': self.scaler,
                'pca': self.pca,
                'is_trained': self.is_trained
            }
            
            # Guardar modelos de sklearn
            for name, model in self.models.items():
                if name not in ['autoencoder', 'encoder']:  # Excluir modelos Keras
                    model_data[name] = model
            
            joblib.dump(model_data, filepath)
            
            # Guardar modelos Keras por separado
            if 'autoencoder' in self.models:
                self.models['autoencoder'].save(filepath.replace('.pkl', '_autoencoder.h5'))
            if 'encoder' in self.models:
                self.models['encoder'].save(filepath.replace('.pkl', '_encoder.h5'))
            
            self.logger.info(f"Modelos guardados en {filepath}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error guardando modelos: {e}")
            return False
    
    def load_models(self, filepath):
        """Cargar modelos entrenados"""
        try:
            model_data = joblib.load(filepath)
            
            self.scaler = model_data['scaler']
            self.pca = model_data['pca']
            self.is_trained = model_data['is_trained']
            
            # Cargar modelos de sklearn
            for name in ['isolation_forest', 'one_class_svm']:
                if name in model_data:
                    self.models[name] = model_data[name]
            
            # Cargar modelos Keras
            try:
                self.models['autoencoder'] = keras.models.load_model(
                    filepath.replace('.pkl', '_autoencoder.h5')
                )
                self.models['encoder'] = keras.models.load_model(
                    filepath.replace('.pkl', '_encoder.h5')
                )
            except:
                self.logger.warning("No se pudieron cargar modelos Keras")
            
            self.logger.info("Modelos cargados exitosamente")
            return True
            
        except Exception as e:
            self.logger.error(f"Error cargando modelos: {e}")
            return False