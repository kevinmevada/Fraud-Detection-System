import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

class FraudDetector:
    def __init__(self, contamination=0.001):
        self.model = IsolationForest(contamination=contamination, random_state=42)
        self.contamination = contamination
        self.scaler = StandardScaler()

    def detect_fraud(self, data, threshold=None, fit=True):
        """
        Detect fraudulent transactions using IsolationForest.
        
        Args:
            data (pd.DataFrame): Input transaction data.
            threshold (float, optional): Contamination threshold for IsolationForest.
            fit (bool): Whether to fit the model (default: True).
        
        Returns:
            pd.DataFrame: DataFrame containing detected frauds.
        """
        required_columns = ['Time', 'Amount']
        if not all(col in data.columns for col in required_columns):
            raise ValueError(f"Data must contain columns: {required_columns}")
        if data[required_columns].isna().any().any():
            raise ValueError("Data contains NaN values in required columns")
        
        if threshold and threshold != self.contamination:
            self.model = IsolationForest(contamination=threshold, random_state=42)
            self.contamination = threshold
        
        features = data[required_columns]
        features_scaled = self.scaler.fit_transform(features) if fit else self.scaler.transform(features)
        
        if fit:
            self.model.fit(features_scaled)
        data['anomaly_score'] = self.model.predict(features_scaled)
        return data[data['anomaly_score'] == -1]

    def analyze_behavior_deep(self, data):
        """
        Analyze behavioral patterns in transaction data.
        
        Args:
            data (pd.DataFrame): Input transaction data.
        
        Returns:
            pd.DataFrame: Behavioral insights.
        """
        required_columns = ['Time', 'Amount', 'Class']
        if not all(col in data.columns for col in required_columns):
            raise ValueError(f"Data must contain columns: {required_columns}")
        
        normal = data[data['Class'] == 0]
        fraud = data[data['Class'] == 1]
        n_clusters = min(3, len(fraud)) if len(fraud) > 0 else 1
        
        fraud_clusters = {}
        if n_clusters > 1:
            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            fraud_features = self.scaler.fit_transform(fraud[['Time', 'Amount']])
            fraud['cluster'] = kmeans.fit_predict(fraud_features)
            fraud_clusters = fraud.groupby('cluster')['Amount'].mean().to_dict()
        
        behavior = {
            'avg_normal_amount': normal['Amount'].mean() if not normal.empty else 0,
            'avg_fraud_amount': fraud['Amount'].mean() if not fraud.empty else 0,
            'transaction_freq': len(data) / (data['Time'].max() / 3600) if data['Time'].max() > 0 else 0,
            'fraud_clusters': fraud_clusters
        }
        return pd.DataFrame([behavior])

    def update_model(self, new_threshold):
        """
        Update the model with a new contamination threshold.
        
        Args:
            new_threshold (float): New contamination value.
        """
        self.__init__(contamination=new_threshold)

detector = FraudDetector()

def detect_fraud(data, threshold=None):
    return detector.detect_fraud(data, threshold)

def analyze_behavior_deep(data):
    return detector.analyze_behavior_deep(data)

def update_model(new_threshold):
    global detector
    detector.update_model(new_threshold)