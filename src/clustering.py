"""
Türkiye İlleri Sosyo-Ekonomik Kümeleme Projesi
Kümeleme Modülü

Bu modül K-Means, Hiyerarşik Kümeleme ve diğer kümeleme algoritmalarını,
optimal küme sayısı belirleme ve değerlendirme metriklerini içerir.
"""

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.mixture import GaussianMixture
from sklearn.metrics import (
    silhouette_score, 
    calinski_harabasz_score, 
    davies_bouldin_score,
    silhouette_samples
)
from sklearn.decomposition import PCA
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from scipy.spatial.distance import cdist
from typing import Tuple, List, Dict, Optional, Union
import warnings

warnings.filterwarnings('ignore')


class ClusteringAnalyzer:
    """
    Kümeleme analizi sınıfı.
    
    Özellikler:
    - K-Means kümeleme
    - Hiyerarşik kümeleme (Agglomerative)
    - DBSCAN kümeleme
    - Gaussian Mixture Model
    - Optimal küme sayısı belirleme
    - Kümeleme değerlendirme metrikleri
    - PCA ile boyut indirgeme
    """
    
    def __init__(self, data: np.ndarray = None, random_state: int = 42):
        """
        ClusteringAnalyzer sınıfını başlat.
        
        Args:
            data: Normalize edilmiş veri matrisi
            random_state: Rastgelelik kontrolü için seed
        """
        self.data = data
        self.random_state = random_state
        self.labels = None
        self.model = None
        self.n_clusters = None
        self.cluster_centers = None
        self.evaluation_results = {}
        
    def set_data(self, data: np.ndarray):
        """Veri setini ayarla."""
        self.data = data
        
    def find_optimal_k(self, 
                      k_range: range = range(2, 11),
                      method: str = 'all') -> pd.DataFrame:
        """
        Optimal küme sayısını bul.
        
        Args:
            k_range: Denenecek k değerleri aralığı
            method: Değerlendirme yöntemi ('elbow', 'silhouette', 'all')
            
        Returns:
            K değerleri ve metrikleri içeren DataFrame
        """
        if self.data is None:
            raise ValueError("Veri seti yüklenmedi!")
        
        results = []
        
        print("Optimal K Değeri Aranıyor...")
        print("-" * 50)
        
        for k in k_range:
            kmeans = KMeans(n_clusters=k, random_state=self.random_state, n_init=10)
            labels = kmeans.fit_predict(self.data)
            
            # Metrikler
            inertia = kmeans.inertia_
            silhouette = silhouette_score(self.data, labels)
            calinski = calinski_harabasz_score(self.data, labels)
            davies = davies_bouldin_score(self.data, labels)
            
            results.append({
                'k': k,
                'inertia': inertia,
                'silhouette': silhouette,
                'calinski_harabasz': calinski,
                'davies_bouldin': davies
            })
            
            print(f"K={k}: Silhouette={silhouette:.4f}, CH={calinski:.2f}, DB={davies:.4f}")
        
        results_df = pd.DataFrame(results)
        
        # En iyi k değerlerini bul
        best_silhouette_k = results_df.loc[results_df['silhouette'].idxmax(), 'k']
        best_calinski_k = results_df.loc[results_df['calinski_harabasz'].idxmax(), 'k']
        best_davies_k = results_df.loc[results_df['davies_bouldin'].idxmin(), 'k']
        
        print("-" * 50)
        print(f"Önerilen K Değerleri:")
        print(f"  - Silhouette'e göre: K={int(best_silhouette_k)}")
        print(f"  - Calinski-Harabasz'a göre: K={int(best_calinski_k)}")
        print(f"  - Davies-Bouldin'e göre: K={int(best_davies_k)}")
        
        return results_df
    
    def fit_kmeans(self, n_clusters: int, n_init: int = 10) -> np.ndarray:
        """
        K-Means kümeleme uygula.
        
        Args:
            n_clusters: Küme sayısı
            n_init: Farklı başlangıç merkez sayısı
            
        Returns:
            Küme etiketleri
        """
        if self.data is None:
            raise ValueError("Veri seti yüklenmedi!")
        
        self.n_clusters = n_clusters
        self.model = KMeans(
            n_clusters=n_clusters, 
            random_state=self.random_state,
            n_init=n_init,
            max_iter=300
        )
        self.labels = self.model.fit_predict(self.data)
        self.cluster_centers = self.model.cluster_centers_
        
        print(f"✓ K-Means kümeleme tamamlandı (K={n_clusters})")
        self._print_cluster_distribution()
        
        return self.labels
    
    def fit_hierarchical(self, 
                        n_clusters: int,
                        linkage_method: str = 'ward',
                        distance_metric: str = 'euclidean') -> np.ndarray:
        """
        Hiyerarşik (Agglomerative) kümeleme uygula.
        
        Args:
            n_clusters: Küme sayısı
            linkage_method: Bağlantı yöntemi ('ward', 'complete', 'average', 'single')
            distance_metric: Uzaklık metriği
            
        Returns:
            Küme etiketleri
        """
        if self.data is None:
            raise ValueError("Veri seti yüklenmedi!")
        
        self.n_clusters = n_clusters
        
        # Ward linkage sadece Euclidean ile çalışır
        if linkage_method == 'ward':
            self.model = AgglomerativeClustering(
                n_clusters=n_clusters,
                linkage=linkage_method
            )
        else:
            self.model = AgglomerativeClustering(
                n_clusters=n_clusters,
                linkage=linkage_method,
                metric=distance_metric
            )
        self.labels = self.model.fit_predict(self.data)
        
        print(f"✓ Hiyerarşik kümeleme tamamlandı (K={n_clusters}, {linkage_method})")
        self._print_cluster_distribution()
        
        return self.labels
    
    def fit_dbscan(self, eps: float = 0.5, min_samples: int = 5) -> np.ndarray:
        """
        DBSCAN kümeleme uygula.
        
        Args:
            eps: Komşuluk yarıçapı
            min_samples: Minimum nokta sayısı
            
        Returns:
            Küme etiketleri
        """
        if self.data is None:
            raise ValueError("Veri seti yüklenmedi!")
        
        self.model = DBSCAN(eps=eps, min_samples=min_samples)
        self.labels = self.model.fit_predict(self.data)
        
        n_clusters = len(set(self.labels)) - (1 if -1 in self.labels else 0)
        n_noise = list(self.labels).count(-1)
        
        self.n_clusters = n_clusters
        
        print(f"✓ DBSCAN kümeleme tamamlandı")
        print(f"  - Küme sayısı: {n_clusters}")
        print(f"  - Gürültü noktası: {n_noise}")
        
        return self.labels
    
    def fit_gaussian_mixture(self, n_components: int) -> np.ndarray:
        """
        Gaussian Mixture Model (GMM) uygula.
        
        Args:
            n_components: Bileşen sayısı
            
        Returns:
            Küme etiketleri
        """
        if self.data is None:
            raise ValueError("Veri seti yüklenmedi!")
        
        self.n_clusters = n_components
        self.model = GaussianMixture(
            n_components=n_components,
            random_state=self.random_state,
            n_init=5
        )
        self.labels = self.model.fit_predict(self.data)
        
        print(f"✓ GMM kümeleme tamamlandı (K={n_components})")
        self._print_cluster_distribution()
        
        return self.labels
    
    def _print_cluster_distribution(self):
        """Küme dağılımını yazdır."""
        if self.labels is None:
            return
        
        unique, counts = np.unique(self.labels, return_counts=True)
        print("  Küme Dağılımı:")
        for cluster, count in zip(unique, counts):
            print(f"    Küme {cluster}: {count} il ({count/len(self.labels)*100:.1f}%)")
    
    def get_linkage_matrix(self, method: str = 'ward') -> np.ndarray:
        """
        Dendrogram için linkage matrisini hesapla.
        
        Args:
            method: Linkage yöntemi
            
        Returns:
            Linkage matrisi
        """
        if self.data is None:
            raise ValueError("Veri seti yüklenmedi!")
        
        return linkage(self.data, method=method)
    
    def cut_dendrogram(self, 
                      linkage_matrix: np.ndarray,
                      n_clusters: int = None,
                      height: float = None) -> np.ndarray:
        """
        Dendrogramı kes ve küme etiketlerini al.
        
        Args:
            linkage_matrix: Linkage matrisi
            n_clusters: Küme sayısı (öncelikli)
            height: Kesim yüksekliği
            
        Returns:
            Küme etiketleri
        """
        if n_clusters is not None:
            self.labels = fcluster(linkage_matrix, n_clusters, criterion='maxclust')
        elif height is not None:
            self.labels = fcluster(linkage_matrix, height, criterion='distance')
        else:
            raise ValueError("n_clusters veya height belirtilmeli!")
        
        # 1-indexed'den 0-indexed'e çevir
        self.labels = self.labels - 1
        self.n_clusters = len(np.unique(self.labels))
        
        return self.labels
    
    def evaluate(self, labels: np.ndarray = None) -> Dict:
        """
        Kümeleme performansını değerlendir.
        
        Args:
            labels: Değerlendirilecek etiketler (None ise self.labels kullanılır)
            
        Returns:
            Değerlendirme metrikleri dictionary
        """
        if labels is None:
            labels = self.labels
        
        if labels is None or self.data is None:
            raise ValueError("Etiketler veya veri eksik!")
        
        # Gürültü noktalarını (-1) filtrele
        mask = labels != -1
        if mask.sum() < len(labels):
            filtered_data = self.data[mask]
            filtered_labels = labels[mask]
        else:
            filtered_data = self.data
            filtered_labels = labels
        
        metrics = {}
        
        # Silhouette Score
        if len(np.unique(filtered_labels)) > 1:
            metrics['silhouette_score'] = silhouette_score(filtered_data, filtered_labels)
            metrics['calinski_harabasz'] = calinski_harabasz_score(filtered_data, filtered_labels)
            metrics['davies_bouldin'] = davies_bouldin_score(filtered_data, filtered_labels)
        else:
            metrics['silhouette_score'] = 0
            metrics['calinski_harabasz'] = 0
            metrics['davies_bouldin'] = float('inf')
        
        # Küme başına metrikler
        sample_silhouettes = silhouette_samples(filtered_data, filtered_labels)
        cluster_silhouettes = {}
        for cluster in np.unique(filtered_labels):
            cluster_mask = filtered_labels == cluster
            cluster_silhouettes[f'cluster_{cluster}_silhouette'] = sample_silhouettes[cluster_mask].mean()
        
        metrics.update(cluster_silhouettes)
        
        # Inertia (sadece K-Means için)
        if hasattr(self.model, 'inertia_'):
            metrics['inertia'] = self.model.inertia_
        
        self.evaluation_results = metrics
        
        return metrics
    
    def get_cluster_profiles(self, 
                            df: pd.DataFrame,
                            feature_columns: List[str],
                            labels: np.ndarray = None) -> pd.DataFrame:
        """
        Her küme için profil oluştur (ortalama değerler).
        
        Args:
            df: Orijinal DataFrame
            feature_columns: Özellik sütunları
            labels: Küme etiketleri
            
        Returns:
            Küme profilleri DataFrame
        """
        if labels is None:
            labels = self.labels
        
        df_with_clusters = df.copy()
        df_with_clusters['kume'] = labels
        
        # Küme ortalamaları
        profiles = df_with_clusters.groupby('kume')[feature_columns].mean()
        
        # Küme boyutları
        cluster_sizes = df_with_clusters['kume'].value_counts().sort_index()
        profiles['il_sayisi'] = cluster_sizes
        
        return profiles
    
    def get_cluster_members(self,
                           df: pd.DataFrame,
                           labels: np.ndarray = None,
                           id_column: str = 'il_adi') -> Dict[int, List]:
        """
        Her kümedeki üyeleri listele.
        
        Args:
            df: Orijinal DataFrame
            labels: Küme etiketleri
            id_column: Tanımlayıcı sütun
            
        Returns:
            Küme: Üyeler dictionary
        """
        if labels is None:
            labels = self.labels
        
        df_with_clusters = df.copy()
        df_with_clusters['kume'] = labels
        
        members = {}
        for cluster in sorted(df_with_clusters['kume'].unique()):
            mask = df_with_clusters['kume'] == cluster
            members[cluster] = df_with_clusters.loc[mask, id_column].tolist()
        
        return members
    
    def apply_pca(self, n_components: int = 2) -> np.ndarray:
        """
        PCA ile boyut indirgeme uygula.
        
        Args:
            n_components: Hedef boyut sayısı
            
        Returns:
            Dönüştürülmüş veri
        """
        if self.data is None:
            raise ValueError("Veri seti yüklenmedi!")
        
        pca = PCA(n_components=n_components)
        transformed = pca.fit_transform(self.data)
        
        explained_variance = pca.explained_variance_ratio_
        print(f"✓ PCA uygulandı ({n_components} bileşen)")
        print(f"  Açıklanan varyans: {explained_variance.sum()*100:.2f}%")
        for i, var in enumerate(explained_variance):
            print(f"    PC{i+1}: {var*100:.2f}%")
        
        return transformed, pca
    
    def compare_algorithms(self, n_clusters: int) -> pd.DataFrame:
        """
        Farklı kümeleme algoritmalarını karşılaştır.
        
        Args:
            n_clusters: Küme sayısı
            
        Returns:
            Karşılaştırma sonuçları DataFrame
        """
        if self.data is None:
            raise ValueError("Veri seti yüklenmedi!")
        
        results = []
        
        # K-Means
        kmeans = KMeans(n_clusters=n_clusters, random_state=self.random_state, n_init=10)
        kmeans_labels = kmeans.fit_predict(self.data)
        results.append({
            'algoritma': 'K-Means',
            'silhouette': silhouette_score(self.data, kmeans_labels),
            'calinski_harabasz': calinski_harabasz_score(self.data, kmeans_labels),
            'davies_bouldin': davies_bouldin_score(self.data, kmeans_labels)
        })
        
        # Hierarchical (Ward)
        hier_ward = AgglomerativeClustering(n_clusters=n_clusters, linkage='ward')
        hier_ward_labels = hier_ward.fit_predict(self.data)
        results.append({
            'algoritma': 'Hierarchical (Ward)',
            'silhouette': silhouette_score(self.data, hier_ward_labels),
            'calinski_harabasz': calinski_harabasz_score(self.data, hier_ward_labels),
            'davies_bouldin': davies_bouldin_score(self.data, hier_ward_labels)
        })
        
        # Hierarchical (Complete)
        hier_complete = AgglomerativeClustering(n_clusters=n_clusters, linkage='complete')
        hier_complete_labels = hier_complete.fit_predict(self.data)
        results.append({
            'algoritma': 'Hierarchical (Complete)',
            'silhouette': silhouette_score(self.data, hier_complete_labels),
            'calinski_harabasz': calinski_harabasz_score(self.data, hier_complete_labels),
            'davies_bouldin': davies_bouldin_score(self.data, hier_complete_labels)
        })
        
        # GMM
        gmm = GaussianMixture(n_components=n_clusters, random_state=self.random_state)
        gmm_labels = gmm.fit_predict(self.data)
        results.append({
            'algoritma': 'Gaussian Mixture',
            'silhouette': silhouette_score(self.data, gmm_labels),
            'calinski_harabasz': calinski_harabasz_score(self.data, gmm_labels),
            'davies_bouldin': davies_bouldin_score(self.data, gmm_labels)
        })
        
        comparison_df = pd.DataFrame(results)
        
        print("\nAlgoritma Karşılaştırması:")
        print("=" * 70)
        print(comparison_df.to_string(index=False))
        print("=" * 70)
        print("Not: Silhouette ve CH yüksek, DB düşük olması iyidir.")
        
        return comparison_df


def run_clustering_pipeline(data: np.ndarray,
                           df: pd.DataFrame,
                           feature_columns: List[str],
                           n_clusters: int = 5,
                           algorithm: str = 'kmeans') -> Tuple[np.ndarray, Dict, pd.DataFrame]:
    """
    Tam kümeleme pipeline'ı çalıştır.
    
    Args:
        data: Normalize edilmiş veri
        df: Orijinal DataFrame
        feature_columns: Özellik sütunları
        n_clusters: Küme sayısı
        algorithm: Kümeleme algoritması ('kmeans', 'hierarchical', 'gmm')
        
    Returns:
        (Etiketler, Metrikler, Profiller) tuple
    """
    analyzer = ClusteringAnalyzer(data)
    
    # Kümeleme uygula
    if algorithm == 'kmeans':
        labels = analyzer.fit_kmeans(n_clusters)
    elif algorithm == 'hierarchical':
        labels = analyzer.fit_hierarchical(n_clusters)
    elif algorithm == 'gmm':
        labels = analyzer.fit_gaussian_mixture(n_clusters)
    else:
        raise ValueError(f"Bilinmeyen algoritma: {algorithm}")
    
    # Değerlendir
    metrics = analyzer.evaluate()
    
    # Profiller
    profiles = analyzer.get_cluster_profiles(df, feature_columns)
    
    return labels, metrics, profiles


if __name__ == "__main__":
    # Test
    print("Kümeleme Modülü Test")
    print("-" * 40)
    
    # Örnek veri oluştur
    np.random.seed(42)
    n_samples = 81
    n_features = 10
    test_data = np.random.randn(n_samples, n_features)
    
    analyzer = ClusteringAnalyzer(test_data)
    
    print("\n1. Optimal K Değeri Analizi:")
    optimal_k_results = analyzer.find_optimal_k(k_range=range(2, 8))
    
    print("\n2. K-Means Kümeleme (K=5):")
    labels = analyzer.fit_kmeans(n_clusters=5)
    
    print("\n3. Değerlendirme Metrikleri:")
    metrics = analyzer.evaluate()
    for metric, value in metrics.items():
        if 'cluster' not in metric:
            print(f"  {metric}: {value:.4f}")
    
    print("\n4. Algoritma Karşılaştırması:")
    comparison = analyzer.compare_algorithms(n_clusters=5)
    
    print("\n✓ Kümeleme modülü test başarılı!")
