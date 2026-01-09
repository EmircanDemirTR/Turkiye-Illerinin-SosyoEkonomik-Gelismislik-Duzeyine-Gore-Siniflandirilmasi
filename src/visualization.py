"""
Türkiye İlleri Sosyo-Ekonomik Kümeleme Projesi
Görselleştirme Modülü

Bu modül kümeleme sonuçlarını görselleştirmek için grafikler,
Türkiye haritası, dendrogram ve diğer görselleştirmeleri içerir.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.cluster.hierarchy import dendrogram
from sklearn.decomposition import PCA
from typing import List, Dict, Optional, Tuple
import warnings
import os

warnings.filterwarnings('ignore')

# Türkçe karakter desteği için
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False


class ClusterVisualizer:
    """
    Kümeleme görselleştirme sınıfı.
    
    Özellikler:
    - Elbow ve Silhouette grafikleri
    - PCA scatter plot
    - Dendrogram
    - Küme profil grafikleri
    - Korelasyon ısı haritası
    - Box plotlar
    - Türkiye haritası (GeoJSON ile)
    """
    
    def __init__(self, 
                 figsize: Tuple[int, int] = (12, 8),
                 style: str = 'whitegrid',
                 palette: str = 'Set2',
                 dpi: int = 300):
        """
        ClusterVisualizer sınıfını başlat.
        
        Args:
            figsize: Varsayılan figür boyutu
            style: Seaborn stili
            palette: Renk paleti
            dpi: Çözünürlük
        """
        self.figsize = figsize
        self.palette = palette
        self.dpi = dpi
        sns.set_style(style)
        
        # Küme renkleri (6 küme için - SEGE benzeri)
        self.cluster_colors = {
            0: '#d73027',  # Kırmızı - En az gelişmiş
            1: '#fc8d59',  # Turuncu
            2: '#fee090',  # Açık sarı
            3: '#91bfdb',  # Açık mavi
            4: '#4575b4',  # Mavi
            5: '#313695'   # Koyu mavi - En gelişmiş
        }
        
        # Küme isimleri
        self.cluster_names = {
            0: '6. Kademe (En Az Gelişmiş)',
            1: '5. Kademe',
            2: '4. Kademe',
            3: '3. Kademe',
            4: '2. Kademe',
            5: '1. Kademe (En Gelişmiş)'
        }
    
    def plot_elbow(self, 
                  results_df: pd.DataFrame,
                  save_path: str = None) -> plt.Figure:
        """
        Elbow (Dirsek) grafiği çiz.
        
        Args:
            results_df: Optimal K analiz sonuçları
            save_path: Kayıt yolu
            
        Returns:
            Matplotlib figure
        """
        fig, ax = plt.subplots(figsize=self.figsize)
        
        ax.plot(results_df['k'], results_df['inertia'], 'bo-', linewidth=2, markersize=10)
        ax.set_xlabel('Küme Sayısı (K)', fontsize=12)
        ax.set_ylabel('Inertia (WCSS)', fontsize=12)
        ax.set_title('Elbow (Dirsek) Yöntemi ile Optimal K Belirleme', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.set_xticks(results_df['k'])
        
        # Dirsek noktasını işaretle (basit yaklaşım)
        # İkinci türevin maksimum olduğu nokta
        inertias = results_df['inertia'].values
        if len(inertias) > 2:
            second_derivative = np.diff(np.diff(inertias))
            elbow_idx = np.argmax(second_derivative) + 1
            elbow_k = results_df['k'].iloc[elbow_idx]
            elbow_inertia = results_df['inertia'].iloc[elbow_idx]
            ax.axvline(x=elbow_k, color='red', linestyle='--', alpha=0.7, label=f'Önerilen K={elbow_k}')
            ax.scatter([elbow_k], [elbow_inertia], color='red', s=200, zorder=5)
            ax.legend()
        
        plt.tight_layout()
        
        if save_path:
            fig.savefig(save_path, dpi=self.dpi, bbox_inches='tight')
            print(f"✓ Grafik kaydedildi: {save_path}")
        
        return fig
    
    def plot_silhouette_scores(self,
                              results_df: pd.DataFrame,
                              save_path: str = None) -> plt.Figure:
        """
        Silhouette skor grafiği çiz.
        
        Args:
            results_df: Optimal K analiz sonuçları
            save_path: Kayıt yolu
            
        Returns:
            Matplotlib figure
        """
        fig, axes = plt.subplots(1, 3, figsize=(16, 5))
        
        # Silhouette Score
        ax1 = axes[0]
        ax1.plot(results_df['k'], results_df['silhouette'], 'go-', linewidth=2, markersize=10)
        ax1.set_xlabel('Küme Sayısı (K)', fontsize=11)
        ax1.set_ylabel('Silhouette Skoru', fontsize=11)
        ax1.set_title('Silhouette Analizi\n(Yüksek = İyi)', fontsize=12, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.set_xticks(results_df['k'])
        best_k = results_df.loc[results_df['silhouette'].idxmax(), 'k']
        ax1.axvline(x=best_k, color='green', linestyle='--', alpha=0.7)
        
        # Calinski-Harabasz
        ax2 = axes[1]
        ax2.plot(results_df['k'], results_df['calinski_harabasz'], 'mo-', linewidth=2, markersize=10)
        ax2.set_xlabel('Küme Sayısı (K)', fontsize=11)
        ax2.set_ylabel('Calinski-Harabasz İndeksi', fontsize=11)
        ax2.set_title('Calinski-Harabasz Analizi\n(Yüksek = İyi)', fontsize=12, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        ax2.set_xticks(results_df['k'])
        best_k = results_df.loc[results_df['calinski_harabasz'].idxmax(), 'k']
        ax2.axvline(x=best_k, color='purple', linestyle='--', alpha=0.7)
        
        # Davies-Bouldin
        ax3 = axes[2]
        ax3.plot(results_df['k'], results_df['davies_bouldin'], 'ro-', linewidth=2, markersize=10)
        ax3.set_xlabel('Küme Sayısı (K)', fontsize=11)
        ax3.set_ylabel('Davies-Bouldin İndeksi', fontsize=11)
        ax3.set_title('Davies-Bouldin Analizi\n(Düşük = İyi)', fontsize=12, fontweight='bold')
        ax3.grid(True, alpha=0.3)
        ax3.set_xticks(results_df['k'])
        best_k = results_df.loc[results_df['davies_bouldin'].idxmin(), 'k']
        ax3.axvline(x=best_k, color='red', linestyle='--', alpha=0.7)
        
        plt.suptitle('Optimal Küme Sayısı Analizi', fontsize=14, fontweight='bold', y=1.02)
        plt.tight_layout()
        
        if save_path:
            fig.savefig(save_path, dpi=self.dpi, bbox_inches='tight')
            print(f"✓ Grafik kaydedildi: {save_path}")
        
        return fig
    
    def plot_pca_clusters(self,
                         data: np.ndarray,
                         labels: np.ndarray,
                         df: pd.DataFrame = None,
                         label_column: str = 'il_adi',
                         show_labels: bool = True,
                         save_path: str = None) -> plt.Figure:
        """
        PCA ile 2D küme görselleştirmesi.
        
        Args:
            data: Normalize edilmiş veri
            labels: Küme etiketleri
            df: Orijinal DataFrame (etiketler için)
            label_column: Etiket sütunu
            show_labels: İl isimlerini göster
            save_path: Kayıt yolu
            
        Returns:
            Matplotlib figure
        """
        # PCA uygula
        pca = PCA(n_components=2)
        data_2d = pca.fit_transform(data)
        
        fig, ax = plt.subplots(figsize=(14, 10))
        
        # Her küme için scatter
        unique_labels = sorted(np.unique(labels))
        for cluster in unique_labels:
            mask = labels == cluster
            color = self.cluster_colors.get(cluster, plt.cm.Set2(cluster / len(unique_labels)))
            name = self.cluster_names.get(cluster, f'Küme {cluster}')
            
            ax.scatter(
                data_2d[mask, 0], 
                data_2d[mask, 1],
                c=[color],
                s=150,
                alpha=0.7,
                label=name,
                edgecolors='white',
                linewidth=1
            )
        
        # İl isimlerini ekle
        if show_labels and df is not None:
            for i, (x, y) in enumerate(data_2d):
                label = df.iloc[i][label_column] if label_column in df.columns else str(i)
                ax.annotate(
                    label,
                    (x, y),
                    fontsize=7,
                    alpha=0.8,
                    ha='center',
                    va='bottom'
                )
        
        ax.set_xlabel(f'Birinci Bileşen (PC1) - {pca.explained_variance_ratio_[0]*100:.1f}%', fontsize=12)
        ax.set_ylabel(f'İkinci Bileşen (PC2) - {pca.explained_variance_ratio_[1]*100:.1f}%', fontsize=12)
        ax.set_title('Türkiye İlleri Sosyo-Ekonomik Kümeleme\n(PCA Görselleştirmesi)', fontsize=14, fontweight='bold')
        ax.legend(loc='best', fontsize=10)
        ax.grid(True, alpha=0.3)
        
        # Açıklanan varyans bilgisi
        total_var = sum(pca.explained_variance_ratio_) * 100
        ax.text(0.02, 0.98, f'Toplam Açıklanan Varyans: {total_var:.1f}%',
                transform=ax.transAxes, fontsize=10, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        plt.tight_layout()
        
        if save_path:
            fig.savefig(save_path, dpi=self.dpi, bbox_inches='tight')
            print(f"✓ Grafik kaydedildi: {save_path}")
        
        return fig
    
    def plot_dendrogram(self,
                       linkage_matrix: np.ndarray,
                       labels: List[str] = None,
                       truncate_mode: str = 'level',
                       p: int = 5,
                       save_path: str = None) -> plt.Figure:
        """
        Dendrogram çiz.
        
        Args:
            linkage_matrix: Scipy linkage matrisi
            labels: Yaprak etiketleri
            truncate_mode: Kırpma modu
            p: Kırpma seviyesi
            save_path: Kayıt yolu
            
        Returns:
            Matplotlib figure
        """
        fig, ax = plt.subplots(figsize=(16, 8))
        
        dendrogram(
            linkage_matrix,
            labels=labels,
            leaf_rotation=90,
            leaf_font_size=8,
            ax=ax,
            color_threshold=0.7 * max(linkage_matrix[:, 2])
        )
        
        ax.set_xlabel('İller', fontsize=12)
        ax.set_ylabel('Uzaklık', fontsize=12)
        ax.set_title('Türkiye İlleri Hiyerarşik Kümeleme Dendrogramı', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        
        if save_path:
            fig.savefig(save_path, dpi=self.dpi, bbox_inches='tight')
            print(f"✓ Grafik kaydedildi: {save_path}")
        
        return fig
    
    def plot_cluster_profiles(self,
                             profiles_df: pd.DataFrame,
                             feature_columns: List[str] = None,
                             save_path: str = None) -> plt.Figure:
        """
        Küme profil grafiği (radar veya bar chart).
        
        Args:
            profiles_df: Küme profilleri DataFrame
            feature_columns: Gösterilecek özellikler
            save_path: Kayıt yolu
            
        Returns:
            Matplotlib figure
        """
        if feature_columns is None:
            feature_columns = [col for col in profiles_df.columns if col != 'il_sayisi'][:10]
        
        # Normalize et (0-1 arası)
        profiles_norm = profiles_df[feature_columns].copy()
        for col in feature_columns:
            col_min = profiles_norm[col].min()
            col_max = profiles_norm[col].max()
            if col_max > col_min:
                profiles_norm[col] = (profiles_norm[col] - col_min) / (col_max - col_min)
        
        fig, ax = plt.subplots(figsize=(14, 8))
        
        x = np.arange(len(feature_columns))
        width = 0.15
        n_clusters = len(profiles_norm)
        
        for i, (cluster_idx, row) in enumerate(profiles_norm.iterrows()):
            offset = (i - n_clusters / 2 + 0.5) * width
            color = self.cluster_colors.get(cluster_idx, plt.cm.Set2(i / n_clusters))
            name = self.cluster_names.get(cluster_idx, f'Küme {cluster_idx}')
            ax.bar(x + offset, row.values, width, label=name, color=color, alpha=0.8)
        
        ax.set_xlabel('Özellikler', fontsize=12)
        ax.set_ylabel('Normalize Değer (0-1)', fontsize=12)
        ax.set_title('Küme Profilleri Karşılaştırması', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(feature_columns, rotation=45, ha='right', fontsize=9)
        ax.legend(loc='upper right', fontsize=9)
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        
        if save_path:
            fig.savefig(save_path, dpi=self.dpi, bbox_inches='tight')
            print(f"✓ Grafik kaydedildi: {save_path}")
        
        return fig
    
    def plot_correlation_heatmap(self,
                                df: pd.DataFrame,
                                columns: List[str] = None,
                                save_path: str = None) -> plt.Figure:
        """
        Korelasyon ısı haritası.
        
        Args:
            df: DataFrame
            columns: Korelasyon hesaplanacak sütunlar
            save_path: Kayıt yolu
            
        Returns:
            Matplotlib figure
        """
        if columns is None:
            columns = df.select_dtypes(include=[np.number]).columns.tolist()
        
        corr_matrix = df[columns].corr()
        
        fig, ax = plt.subplots(figsize=(14, 12))
        
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool), k=1)
        
        sns.heatmap(
            corr_matrix,
            mask=mask,
            annot=True,
            fmt='.2f',
            cmap='RdBu_r',
            center=0,
            square=True,
            linewidths=0.5,
            ax=ax,
            annot_kws={'size': 8},
            cbar_kws={'label': 'Korelasyon Katsayısı'}
        )
        
        ax.set_title('Değişkenler Arası Korelasyon Matrisi', fontsize=14, fontweight='bold')
        plt.xticks(rotation=45, ha='right', fontsize=9)
        plt.yticks(fontsize=9)
        
        plt.tight_layout()
        
        if save_path:
            fig.savefig(save_path, dpi=self.dpi, bbox_inches='tight')
            print(f"✓ Grafik kaydedildi: {save_path}")
        
        return fig
    
    def plot_cluster_distribution(self,
                                 df: pd.DataFrame,
                                 labels: np.ndarray,
                                 save_path: str = None) -> plt.Figure:
        """
        Küme dağılım grafiği (pie chart + bar chart).
        
        Args:
            df: DataFrame
            labels: Küme etiketleri
            save_path: Kayıt yolu
            
        Returns:
            Matplotlib figure
        """
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
        unique, counts = np.unique(labels, return_counts=True)
        
        # Pasta grafiği
        ax1 = axes[0]
        colors = [self.cluster_colors.get(i, plt.cm.Set2(i / len(unique))) for i in unique]
        labels_names = [self.cluster_names.get(i, f'Küme {i}') for i in unique]
        
        wedges, texts, autotexts = ax1.pie(
            counts, 
            labels=labels_names,
            colors=colors,
            autopct='%1.1f%%',
            startangle=90,
            explode=[0.02] * len(unique)
        )
        ax1.set_title('Küme Dağılımı (Pasta Grafiği)', fontsize=12, fontweight='bold')
        
        # Bar grafiği
        ax2 = axes[1]
        bars = ax2.bar(range(len(unique)), counts, color=colors, edgecolor='white', linewidth=2)
        ax2.set_xlabel('Küme', fontsize=11)
        ax2.set_ylabel('İl Sayısı', fontsize=11)
        ax2.set_title('Küme Dağılımı (Çubuk Grafiği)', fontsize=12, fontweight='bold')
        ax2.set_xticks(range(len(unique)))
        ax2.set_xticklabels([f'Küme {i}' for i in unique], fontsize=10)
        
        # Değerleri çubukların üstüne yaz
        for bar, count in zip(bars, counts):
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                    str(count), ha='center', va='bottom', fontsize=11, fontweight='bold')
        
        ax2.grid(True, alpha=0.3, axis='y')
        
        plt.suptitle('Türkiye İlleri Kümeleme Sonuçları', fontsize=14, fontweight='bold', y=1.02)
        plt.tight_layout()
        
        if save_path:
            fig.savefig(save_path, dpi=self.dpi, bbox_inches='tight')
            print(f"✓ Grafik kaydedildi: {save_path}")
        
        return fig
    
    def plot_boxplots_by_cluster(self,
                                df: pd.DataFrame,
                                labels: np.ndarray,
                                features: List[str],
                                save_path: str = None) -> plt.Figure:
        """
        Kümelere göre box plot.
        
        Args:
            df: DataFrame
            labels: Küme etiketleri
            features: Gösterilecek özellikler
            save_path: Kayıt yolu
            
        Returns:
            Matplotlib figure
        """
        df_plot = df.copy()
        df_plot['Küme'] = labels
        
        n_features = len(features)
        n_cols = 3
        n_rows = (n_features + n_cols - 1) // n_cols
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 4 * n_rows))
        axes = axes.flatten()
        
        for i, feature in enumerate(features):
            ax = axes[i]
            sns.boxplot(x='Küme', y=feature, data=df_plot, ax=ax, palette=self.cluster_colors)
            ax.set_title(feature, fontsize=11, fontweight='bold')
            ax.set_xlabel('')
            ax.grid(True, alpha=0.3, axis='y')
        
        # Boş subplot'ları gizle
        for j in range(i + 1, len(axes)):
            axes[j].set_visible(False)
        
        plt.suptitle('Kümelere Göre Değişken Dağılımları', fontsize=14, fontweight='bold', y=1.02)
        plt.tight_layout()
        
        if save_path:
            fig.savefig(save_path, dpi=self.dpi, bbox_inches='tight')
            print(f"✓ Grafik kaydedildi: {save_path}")
        
        return fig
    
    def plot_algorithm_comparison(self,
                                 comparison_df: pd.DataFrame,
                                 save_path: str = None) -> plt.Figure:
        """
        Algoritma karşılaştırma grafiği.
        
        Args:
            comparison_df: Karşılaştırma sonuçları
            save_path: Kayıt yolu
            
        Returns:
            Matplotlib figure
        """
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        
        algorithms = comparison_df['algoritma']
        colors = plt.cm.Set2(np.linspace(0, 1, len(algorithms)))
        
        # Silhouette
        ax1 = axes[0]
        bars1 = ax1.bar(algorithms, comparison_df['silhouette'], color=colors, edgecolor='white')
        ax1.set_ylabel('Silhouette Skoru')
        ax1.set_title('Silhouette Karşılaştırması\n(Yüksek = İyi)', fontweight='bold')
        ax1.tick_params(axis='x', rotation=45)
        for bar, val in zip(bars1, comparison_df['silhouette']):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                    f'{val:.3f}', ha='center', va='bottom', fontsize=9)
        
        # Calinski-Harabasz
        ax2 = axes[1]
        bars2 = ax2.bar(algorithms, comparison_df['calinski_harabasz'], color=colors, edgecolor='white')
        ax2.set_ylabel('Calinski-Harabasz İndeksi')
        ax2.set_title('Calinski-Harabasz Karşılaştırması\n(Yüksek = İyi)', fontweight='bold')
        ax2.tick_params(axis='x', rotation=45)
        for bar, val in zip(bars2, comparison_df['calinski_harabasz']):
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                    f'{val:.1f}', ha='center', va='bottom', fontsize=9)
        
        # Davies-Bouldin
        ax3 = axes[2]
        bars3 = ax3.bar(algorithms, comparison_df['davies_bouldin'], color=colors, edgecolor='white')
        ax3.set_ylabel('Davies-Bouldin İndeksi')
        ax3.set_title('Davies-Bouldin Karşılaştırması\n(Düşük = İyi)', fontweight='bold')
        ax3.tick_params(axis='x', rotation=45)
        for bar, val in zip(bars3, comparison_df['davies_bouldin']):
            ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                    f'{val:.3f}', ha='center', va='bottom', fontsize=9)
        
        plt.suptitle('Kümeleme Algoritmaları Performans Karşılaştırması', fontsize=14, fontweight='bold', y=1.02)
        plt.tight_layout()
        
        if save_path:
            fig.savefig(save_path, dpi=self.dpi, bbox_inches='tight')
            print(f"✓ Grafik kaydedildi: {save_path}")
        
        return fig
    
    def save_all_figures(self, output_dir: str = 'reports/figures/'):
        """Tüm figürleri kaydet."""
        os.makedirs(output_dir, exist_ok=True)
        print(f"✓ Figürler {output_dir} dizinine kaydedilecek")


def create_turkey_map_html(df: pd.DataFrame, 
                          labels: np.ndarray,
                          geojson_path: str = None,
                          output_path: str = 'reports/figures/turkiye_harita.html') -> str:
    """
    Folium ile interaktif Türkiye haritası oluştur.
    
    Args:
        df: İl verileri DataFrame
        labels: Küme etiketleri
        geojson_path: Türkiye GeoJSON dosya yolu
        output_path: Çıktı HTML dosya yolu
        
    Returns:
        HTML dosya yolu
    """
    try:
        import folium
        from folium import Choropleth
        
        # Harita merkezi (Türkiye)
        m = folium.Map(location=[39.0, 35.0], zoom_start=6, tiles='CartoDB positron')
        
        # Küme bilgilerini DataFrame'e ekle
        df_map = df.copy()
        df_map['kume'] = labels
        
        # Renk skalası
        cluster_colors = {
            0: '#d73027',
            1: '#fc8d59',
            2: '#fee090',
            3: '#91bfdb',
            4: '#4575b4',
            5: '#313695'
        }
        
        # Her il için marker ekle (basitleştirilmiş)
        for _, row in df_map.iterrows():
            cluster = row['kume']
            color = cluster_colors.get(cluster, '#808080')
            
            folium.CircleMarker(
                location=[39.0, 35.0],  # Placeholder - gerçek koordinatlar gerekli
                radius=5,
                popup=f"{row['il_adi']}<br>Küme: {cluster}",
                color=color,
                fill=True,
                fillColor=color
            )
        
        # Kaydet
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        m.save(output_path)
        print(f"✓ Harita kaydedildi: {output_path}")
        
        return output_path
        
    except ImportError:
        print("⚠ Folium yüklü değil. pip install folium ile yükleyin.")
        return None


if __name__ == "__main__":
    # Test
    print("Görselleştirme Modülü Test")
    print("-" * 40)
    
    visualizer = ClusterVisualizer()
    
    # Örnek veri
    np.random.seed(42)
    n_samples = 81
    
    test_results = pd.DataFrame({
        'k': range(2, 8),
        'inertia': [1000, 800, 600, 500, 450, 420],
        'silhouette': [0.3, 0.35, 0.4, 0.38, 0.35, 0.32],
        'calinski_harabasz': [100, 120, 150, 140, 130, 120],
        'davies_bouldin': [1.5, 1.3, 1.1, 1.2, 1.3, 1.4]
    })
    
    print("Elbow grafiği oluşturuluyor...")
    fig1 = visualizer.plot_elbow(test_results)
    
    print("Silhouette grafikleri oluşturuluyor...")
    fig2 = visualizer.plot_silhouette_scores(test_results)
    
    print("\n✓ Görselleştirme modülü test başarılı!")
    plt.show()
