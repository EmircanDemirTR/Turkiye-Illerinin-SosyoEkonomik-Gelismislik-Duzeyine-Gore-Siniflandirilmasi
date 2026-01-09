"""
Türkiye İlleri Sosyo-Ekonomik Kümeleme Projesi
Veri Ön İşleme Modülü

Bu modül veri temizleme, normalizasyon, eksik veri işleme ve 
aykırı değer tespiti işlemlerini içerir.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.impute import SimpleImputer, KNNImputer
from scipy import stats
from typing import Tuple, List, Optional, Union
import warnings

warnings.filterwarnings('ignore')


class DataPreprocessor:
    """
    Veri ön işleme sınıfı.
    
    Özellikler:
    - Veri yükleme ve doğrulama
    - Eksik veri analizi ve imputation
    - Aykırı değer tespiti ve işleme
    - Normalizasyon (StandardScaler, MinMaxScaler, RobustScaler)
    - Özellik seçimi
    """
    
    def __init__(self, data: pd.DataFrame = None):
        """
        DataPreprocessor sınıfını başlat.
        
        Args:
            data: İşlenecek pandas DataFrame
        """
        self.data = data
        self.original_data = data.copy() if data is not None else None
        self.scaler = None
        self.imputer = None
        self.numeric_columns = []
        self.categorical_columns = []
        self.feature_columns = []
        
    def load_data(self, filepath: str, encoding: str = 'utf-8') -> pd.DataFrame:
        """
        CSV dosyasından veri yükle.
        
        Args:
            filepath: CSV dosya yolu
            encoding: Dosya kodlaması
            
        Returns:
            Yüklenen DataFrame
        """
        try:
            self.data = pd.read_csv(filepath, encoding=encoding)
            self.original_data = self.data.copy()
            self._identify_column_types()
            print(f"✓ Veri başarıyla yüklendi: {self.data.shape[0]} satır, {self.data.shape[1]} sütun")
            return self.data
        except Exception as e:
            print(f"✗ Veri yükleme hatası: {e}")
            return None
    
    def _identify_column_types(self):
        """Sütun tiplerini tanımla."""
        self.numeric_columns = self.data.select_dtypes(include=[np.number]).columns.tolist()
        self.categorical_columns = self.data.select_dtypes(include=['object', 'category']).columns.tolist()
        
    def get_data_summary(self) -> dict:
        """
        Veri seti özet istatistiklerini döndür.
        
        Returns:
            Özet istatistikler dictionary
        """
        if self.data is None:
            return {}
        
        summary = {
            'satir_sayisi': self.data.shape[0],
            'sutun_sayisi': self.data.shape[1],
            'numerik_sutunlar': len(self.numeric_columns),
            'kategorik_sutunlar': len(self.categorical_columns),
            'eksik_deger_toplam': self.data.isnull().sum().sum(),
            'eksik_deger_orani': (self.data.isnull().sum().sum() / (self.data.shape[0] * self.data.shape[1])) * 100,
            'bellek_kullanimi_mb': self.data.memory_usage(deep=True).sum() / 1024 / 1024
        }
        
        return summary
    
    def analyze_missing_values(self) -> pd.DataFrame:
        """
        Eksik değer analizini gerçekleştir.
        
        Returns:
            Eksik değer istatistikleri DataFrame
        """
        if self.data is None:
            return pd.DataFrame()
        
        missing_stats = pd.DataFrame({
            'eksik_sayi': self.data.isnull().sum(),
            'eksik_oran': (self.data.isnull().sum() / len(self.data)) * 100,
            'veri_tipi': self.data.dtypes
        })
        
        missing_stats = missing_stats[missing_stats['eksik_sayi'] > 0].sort_values(
            'eksik_oran', ascending=False
        )
        
        return missing_stats
    
    def handle_missing_values(self, 
                             method: str = 'median',
                             columns: List[str] = None,
                             n_neighbors: int = 5) -> pd.DataFrame:
        """
        Eksik değerleri işle.
        
        Args:
            method: Imputation yöntemi ('mean', 'median', 'mode', 'knn', 'drop')
            columns: İşlenecek sütunlar (None ise tüm numerik sütunlar)
            n_neighbors: KNN imputation için komşu sayısı
            
        Returns:
            İşlenmiş DataFrame
        """
        if self.data is None:
            return None
        
        if columns is None:
            columns = self.numeric_columns
        
        if method == 'drop':
            self.data = self.data.dropna(subset=columns)
            print(f"✓ Eksik değerli satırlar silindi. Kalan: {len(self.data)} satır")
            
        elif method in ['mean', 'median', 'most_frequent']:
            strategy = method if method != 'mode' else 'most_frequent'
            self.imputer = SimpleImputer(strategy=strategy)
            self.data[columns] = self.imputer.fit_transform(self.data[columns])
            print(f"✓ Eksik değerler {method} yöntemiyle dolduruldu")
            
        elif method == 'knn':
            self.imputer = KNNImputer(n_neighbors=n_neighbors)
            self.data[columns] = self.imputer.fit_transform(self.data[columns])
            print(f"✓ Eksik değerler KNN ({n_neighbors} komşu) ile dolduruldu")
        
        return self.data
    
    def detect_outliers(self, 
                       method: str = 'iqr',
                       columns: List[str] = None,
                       threshold: float = 1.5) -> pd.DataFrame:
        """
        Aykırı değerleri tespit et.
        
        Args:
            method: Tespit yöntemi ('zscore', 'iqr', 'isolation_forest')
            columns: Kontrol edilecek sütunlar
            threshold: Eşik değeri (IQR için çarpan, zscore için z-değeri)
            
        Returns:
            Aykırı değer analizi DataFrame
        """
        if self.data is None:
            return pd.DataFrame()
        
        if columns is None:
            columns = self.numeric_columns
        
        outlier_summary = []
        
        for col in columns:
            if col in self.data.columns and pd.api.types.is_numeric_dtype(self.data[col]):
                if method == 'zscore':
                    z_scores = np.abs(stats.zscore(self.data[col].dropna()))
                    outliers = z_scores > threshold
                    n_outliers = outliers.sum()
                    
                elif method == 'iqr':
                    Q1 = self.data[col].quantile(0.25)
                    Q3 = self.data[col].quantile(0.75)
                    IQR = Q3 - Q1
                    lower_bound = Q1 - threshold * IQR
                    upper_bound = Q3 + threshold * IQR
                    outliers = (self.data[col] < lower_bound) | (self.data[col] > upper_bound)
                    n_outliers = outliers.sum()
                
                outlier_summary.append({
                    'sutun': col,
                    'aykiri_sayi': n_outliers,
                    'aykiri_oran': (n_outliers / len(self.data)) * 100,
                    'min': self.data[col].min(),
                    'max': self.data[col].max(),
                    'ortalama': self.data[col].mean(),
                    'medyan': self.data[col].median()
                })
        
        return pd.DataFrame(outlier_summary)
    
    def handle_outliers(self,
                       method: str = 'iqr',
                       action: str = 'clip',
                       columns: List[str] = None,
                       threshold: float = 1.5) -> pd.DataFrame:
        """
        Aykırı değerleri işle.
        
        Args:
            method: Tespit yöntemi ('zscore', 'iqr')
            action: İşlem ('clip', 'remove', 'winsorize')
            columns: İşlenecek sütunlar
            threshold: Eşik değeri
            
        Returns:
            İşlenmiş DataFrame
        """
        if self.data is None:
            return None
        
        if columns is None:
            columns = self.numeric_columns
        
        for col in columns:
            if col not in self.data.columns or not pd.api.types.is_numeric_dtype(self.data[col]):
                continue
                
            if method == 'iqr':
                Q1 = self.data[col].quantile(0.25)
                Q3 = self.data[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - threshold * IQR
                upper_bound = Q3 + threshold * IQR
                
            elif method == 'zscore':
                mean = self.data[col].mean()
                std = self.data[col].std()
                lower_bound = mean - threshold * std
                upper_bound = mean + threshold * std
            
            if action == 'clip':
                self.data[col] = self.data[col].clip(lower=lower_bound, upper=upper_bound)
            elif action == 'remove':
                mask = (self.data[col] >= lower_bound) & (self.data[col] <= upper_bound)
                self.data = self.data[mask]
            elif action == 'winsorize':
                self.data[col] = stats.mstats.winsorize(self.data[col], limits=[0.05, 0.05])
        
        print(f"✓ Aykırı değerler {action} yöntemiyle işlendi")
        return self.data
    
    def normalize(self,
                 method: str = 'standard',
                 columns: List[str] = None) -> Tuple[np.ndarray, object]:
        """
        Veriyi normalize et.
        
        Args:
            method: Normalizasyon yöntemi ('standard', 'minmax', 'robust')
            columns: Normalize edilecek sütunlar
            
        Returns:
            (Normalize edilmiş veri, Scaler objesi) tuple
        """
        if self.data is None:
            return None, None
        
        if columns is None:
            columns = self.numeric_columns
        
        # Meta sütunları hariç tut
        exclude_cols = ['il_kodu', 'il_adi', 'plaka', 'bolge', 'sege_kademe']
        feature_cols = [col for col in columns if col not in exclude_cols]
        self.feature_columns = feature_cols
        
        if method == 'standard':
            self.scaler = StandardScaler()
        elif method == 'minmax':
            self.scaler = MinMaxScaler()
        elif method == 'robust':
            self.scaler = RobustScaler()
        else:
            raise ValueError(f"Bilinmeyen normalizasyon yöntemi: {method}")
        
        scaled_data = self.scaler.fit_transform(self.data[feature_cols])
        
        print(f"✓ Veri {method} yöntemiyle normalize edildi ({len(feature_cols)} özellik)")
        
        return scaled_data, self.scaler
    
    def select_features(self,
                       exclude_columns: List[str] = None,
                       correlation_threshold: float = 0.95) -> List[str]:
        """
        Özellik seçimi yap.
        
        Args:
            exclude_columns: Hariç tutulacak sütunlar
            correlation_threshold: Yüksek korelasyon eşiği
            
        Returns:
            Seçilen özellik listesi
        """
        if self.data is None:
            return []
        
        if exclude_columns is None:
            exclude_columns = ['il_kodu', 'il_adi', 'plaka', 'bolge', 'sege_endeksi', 'sege_kademe']
        
        # Numerik sütunları al
        numeric_data = self.data.select_dtypes(include=[np.number])
        feature_cols = [col for col in numeric_data.columns if col not in exclude_columns]
        
        # Yüksek korelasyonlu özellikleri tespit et
        corr_matrix = numeric_data[feature_cols].corr().abs()
        upper_triangle = corr_matrix.where(
            np.triu(np.ones(corr_matrix.shape), k=1).astype(bool)
        )
        
        # Yüksek korelasyonlu sütunları bul
        high_corr_cols = [col for col in upper_triangle.columns 
                         if any(upper_triangle[col] > correlation_threshold)]
        
        # Seçilen özellikleri güncelle
        selected_features = [col for col in feature_cols if col not in high_corr_cols]
        self.feature_columns = selected_features
        
        print(f"✓ {len(selected_features)} özellik seçildi ({len(high_corr_cols)} yüksek korelasyonlu özellik çıkarıldı)")
        
        return selected_features
    
    def get_correlation_matrix(self, columns: List[str] = None) -> pd.DataFrame:
        """
        Korelasyon matrisini hesapla.
        
        Args:
            columns: Korelasyon hesaplanacak sütunlar
            
        Returns:
            Korelasyon matrisi DataFrame
        """
        if self.data is None:
            return pd.DataFrame()
        
        if columns is None:
            columns = self.feature_columns if self.feature_columns else self.numeric_columns
        
        return self.data[columns].corr()
    
    def prepare_for_clustering(self,
                              exclude_columns: List[str] = None,
                              normalize_method: str = 'standard',
                              handle_outliers_method: str = 'clip') -> Tuple[np.ndarray, pd.DataFrame, List[str]]:
        """
        Kümeleme için veriyi hazırla (tüm ön işleme adımlarını uygula).
        
        Args:
            exclude_columns: Hariç tutulacak sütunlar
            normalize_method: Normalizasyon yöntemi
            handle_outliers_method: Aykırı değer işleme yöntemi
            
        Returns:
            (Normalize veri, Orijinal DataFrame, Özellik listesi) tuple
        """
        if exclude_columns is None:
            exclude_columns = ['il_kodu', 'il_adi', 'plaka', 'bolge', 'sege_endeksi', 'sege_kademe']
        
        print("=" * 50)
        print("KÜMELEME İÇİN VERİ HAZIRLAMA")
        print("=" * 50)
        
        # 1. Eksik değer kontrolü
        print("\n1. Eksik Değer Kontrolü:")
        missing = self.analyze_missing_values()
        if len(missing) > 0:
            print(f"   {len(missing)} sütunda eksik değer tespit edildi")
            self.handle_missing_values(method='median')
        else:
            print("   ✓ Eksik değer yok")
        
        # 2. Özellik seçimi
        print("\n2. Özellik Seçimi:")
        self.select_features(exclude_columns=exclude_columns)
        
        # 3. Aykırı değer işleme
        print("\n3. Aykırı Değer İşleme:")
        outlier_stats = self.detect_outliers(columns=self.feature_columns)
        n_outliers = outlier_stats['aykiri_sayi'].sum()
        if n_outliers > 0:
            print(f"   Toplam {n_outliers} aykırı değer tespit edildi")
            self.handle_outliers(action=handle_outliers_method, columns=self.feature_columns)
        else:
            print("   ✓ Aykırı değer yok")
        
        # 4. Normalizasyon
        print("\n4. Normalizasyon:")
        scaled_data, _ = self.normalize(method=normalize_method, columns=self.feature_columns)
        
        print("\n" + "=" * 50)
        print(f"✓ Veri hazırlama tamamlandı!")
        print(f"  - Veri boyutu: {scaled_data.shape}")
        print(f"  - Özellik sayısı: {len(self.feature_columns)}")
        print("=" * 50)
        
        return scaled_data, self.data, self.feature_columns


def load_and_preprocess(filepath: str,
                       exclude_columns: List[str] = None,
                       normalize_method: str = 'standard') -> Tuple[np.ndarray, pd.DataFrame, List[str], DataPreprocessor]:
    """
    Veriyi yükle ve kümeleme için hazırla (kısayol fonksiyon).
    
    Args:
        filepath: CSV dosya yolu
        exclude_columns: Hariç tutulacak sütunlar
        normalize_method: Normalizasyon yöntemi
        
    Returns:
        (Normalize veri, DataFrame, Özellik listesi, Preprocessor) tuple
    """
    preprocessor = DataPreprocessor()
    preprocessor.load_data(filepath)
    
    scaled_data, df, features = preprocessor.prepare_for_clustering(
        exclude_columns=exclude_columns,
        normalize_method=normalize_method
    )
    
    return scaled_data, df, features, preprocessor


if __name__ == "__main__":
    # Test
    print("Veri Ön İşleme Modülü Test")
    print("-" * 40)
    
    # Örnek kullanım
    filepath = "data/processed/il_verileri.csv"
    
    try:
        preprocessor = DataPreprocessor()
        df = preprocessor.load_data(filepath)
        
        if df is not None:
            print("\nVeri Özeti:")
            summary = preprocessor.get_data_summary()
            for key, value in summary.items():
                print(f"  {key}: {value}")
            
            print("\nÖzellik Seçimi ve Normalizasyon:")
            scaled_data, _, features = preprocessor.prepare_for_clustering()
            
            print(f"\nSeçilen Özellikler ({len(features)}):")
            for i, feat in enumerate(features, 1):
                print(f"  {i}. {feat}")
                
    except FileNotFoundError:
        print("Test dosyası bulunamadı. Modül başarıyla yüklendi.")
