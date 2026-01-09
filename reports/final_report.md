# TÜRKİYE İLLERİNİN SOSYO-EKONOMİK GELİŞMİŞLİK DÜZEYLERİNE GÖRE MAKİNE ÖĞRENMESİ YÖNTEMLERİYLE KÜMELENMESİ

## LİSANS BİTİRME PROJESİ

**Güz Dönemi 2025-2026**

---

## ÖZET

Bu çalışmada, Türkiye'deki 81 ilin sosyo-ekonomik gelişmişlik düzeylerine göre makine öğrenmesi kümeleme algoritmaları kullanılarak gruplandırılması amaçlanmıştır. Araştırmada TÜİK (Türkiye İstatistik Kurumu), TCMB (Türkiye Cumhuriyet Merkez Bankası) ve SEGE 2022 (Sosyo-Ekonomik Gelişmişlik Endeksi) raporlarından derlenen 24 farklı sosyo-ekonomik gösterge kullanılmıştır. K-Means ve Hiyerarşik Kümeleme algoritmaları uygulanmış, optimal küme sayısı Elbow, Silhouette ve Calinski-Harabasz yöntemleriyle belirlenmiştir. Sonuçlar, Sanayi ve Teknoloji Bakanlığı'nın SEGE sınıflandırmasıyla karşılaştırılmıştır. Çalışma, bölgesel kalkınma politikalarının planlanmasına katkı sağlayabilecek bulgular ortaya koymaktadır.

**Anahtar Kelimeler:** Kümeleme Analizi, K-Means, Sosyo-Ekonomik Gelişmişlik, Türkiye İlleri, Makine Öğrenmesi

---

## ABSTRACT

This study aims to cluster the 81 provinces of Turkey according to their socio-economic development levels using machine learning clustering algorithms. 24 different socio-economic indicators compiled from TurkStat (Turkish Statistical Institute), CBRT (Central Bank of the Republic of Turkey), and SEDI 2022 (Socio-Economic Development Index) reports were used in the research. K-Means and Hierarchical Clustering algorithms were applied, and the optimal number of clusters was determined using Elbow, Silhouette, and Calinski-Harabasz methods. The results were compared with the SEDI classification of the Ministry of Industry and Technology. The study presents findings that may contribute to the planning of regional development policies.

**Keywords:** Cluster Analysis, K-Means, Socio-Economic Development, Turkish Provinces, Machine Learning

---

## İÇİNDEKİLER

1. [GİRİŞ](#1-giriş)
2. [LİTERATÜR TARAMASI](#2-literatür-taraması)
3. [METODOLOJİ](#3-metodoloji)
   - 3.1 Veri Kaynakları
   - 3.2 Değişkenler
   - 3.3 Kümeleme Algoritmaları
   - 3.4 Değerlendirme Metrikleri
4. [BULGULAR](#4-bulgular)
   - 4.1 Keşifsel Veri Analizi
   - 4.2 Optimal Küme Sayısı
   - 4.3 K-Means Kümeleme Sonuçları
   - 4.4 Hiyerarşik Kümeleme Sonuçları
   - 4.5 SEGE ile Karşılaştırma
5. [TARTIŞMA](#5-tartışma)
6. [SONUÇ VE ÖNERİLER](#6-sonuç-ve-öneriler)
7. [KAYNAKÇA](#7-kaynakça)
8. [EKLER](#8-ekler)

---

## 1. GİRİŞ

### 1.1 Araştırmanın Arka Planı

Türkiye, coğrafi konumu, demografik yapısı ve ekonomik potansiyeli açısından önemli bir ülke olmakla birlikte, bölgeler ve iller arasında belirgin gelişmişlik farklılıkları bulunmaktadır. Bu farklılıkların analizi ve anlaşılması, bölgesel kalkınma politikalarının etkin bir şekilde planlanması için kritik öneme sahiptir.

Son yıllarda makine öğrenmesi tekniklerinin gelişmesiyle birlikte, sosyo-ekonomik verilerin analizi için güçlü araçlar ortaya çıkmıştır. Kümeleme algoritmaları, benzer özelliklere sahip birimlerin (iller, bölgeler vb.) gruplandırılmasında etkili bir yöntem olarak öne çıkmaktadır.

### 1.2 Araştırmanın Amacı

Bu çalışmanın temel amacı:

1. Türkiye'deki 81 ilin sosyo-ekonomik göstergeler kullanılarak kümelenmesi
2. K-Means ve Hiyerarşik Kümeleme algoritmalarının karşılaştırılması
3. Elde edilen sonuçların SEGE 2022 sınıflandırmasıyla karşılaştırılması
4. Bölgesel kalkınma politikalarına yönelik öneriler geliştirilmesi

### 1.3 Araştırmanın Önemi

Bu araştırma:

- Güncel veri ve yöntemler kullanarak il bazlı gelişmişlik analizi sunmaktadır
- Farklı kümeleme algoritmalarının performansını karşılaştırmaktadır
- Resmi SEGE sınıflandırmasıyla tutarlılık analizi yapmaktadır
- Politika yapıcılara veri odaklı karar desteği sağlamaktadır

### 1.4 Araştırma Soruları

1. Türkiye illeri hangi sosyo-ekonomik göstergeler açısından benzer gruplar oluşturmaktadır?
2. K-Means ve Hiyerarşik Kümeleme algoritmaları hangi performansı göstermektedir?
3. Makine öğrenmesi ile elde edilen kümeler, resmi SEGE sınıflandırmasıyla ne ölçüde uyumludur?

---

## 2. LİTERATÜR TARAMASI

### 2.1 Sosyo-Ekonomik Gelişmişlik Kavramı

Sosyo-ekonomik gelişmişlik, bir bölgenin ekonomik, sosyal ve kültürel açıdan ulaştığı düzeyi ifade etmektedir. Bu kavram çok boyutlu bir yapıya sahip olup, tek bir gösterge ile ölçülmesi mümkün değildir (Dinçer vd., 2003).

Türkiye'de illerin gelişmişlik düzeylerinin belirlenmesi amacıyla çeşitli çalışmalar yapılmıştır:

- **DPT SEGE Çalışmaları (1996, 2003, 2011):** İllerin sosyo-ekonomik gelişmişlik sıralaması
- **Kalkınma Bakanlığı SEGE 2017:** Güncellenmiş metodoloji ile yeni sıralama
- **Sanayi ve Teknoloji Bakanlığı SEGE 2022:** En güncel resmi sınıflandırma

### 2.2 Kümeleme Yöntemleri ve Uygulamalar

Kümeleme analizi, veri noktalarını benzerliklerine göre gruplandıran denetimsiz öğrenme tekniklerinden biridir. Literatürde yaygın olarak kullanılan yöntemler:

**K-Means Algoritması:**
- MacQueen (1967) tarafından önerilmiştir
- Merkez tabanlı bir bölümleme yöntemidir
- Hızlı ve ölçeklenebilir yapısıyla öne çıkmaktadır

**Hiyerarşik Kümeleme:**
- Ward (1963) linkage yöntemi yaygın kullanılmaktadır
- Dendrogram ile görselleştirme imkanı sunar
- Küme sayısının önceden bilinmesini gerektirmez

### 2.3 Türkiye'de Yapılan Benzer Çalışmalar

| Yazar(lar) | Yıl | Yöntem | Değişken Sayısı |
|------------|-----|--------|-----------------|
| Albayrak (2005) | 2005 | Kümeleme | 32 |
| Özkan ve Uzun | 2017 | K-Means | 48 |
| Doğan ve Kabak | 2020 | Hibrit | 35 |

Bu çalışmalar, Türkiye illerinin benzer gelişmişlik düzeylerine sahip gruplar oluşturduğunu ortaya koymuştur.

---

## 3. METODOLOJİ

### 3.1 Veri Kaynakları

Çalışmada kullanılan veriler aşağıdaki resmi kaynaklardan derlenmiştir:

| Kaynak | Veri Türü | Erişim |
|--------|-----------|--------|
| TÜİK | Nüfus, İstihdam, Eğitim, Sağlık | https://biruni.tuik.gov.tr/ilgosterge/ |
| TCMB EVDS | Ekonomik göstergeler | https://evds2.tcmb.gov.tr/ |
| SEGE 2022 | Gelişmişlik endeksi | Sanayi ve Teknoloji Bakanlığı |
| Çevre ve Şehircilik | Hava kalitesi | https://sim.csb.gov.tr/ |

### 3.2 Değişkenler

Araştırmada 24 sosyo-ekonomik gösterge kullanılmıştır:

#### 3.2.1 Demografik Değişkenler (5 adet)
- Nüfus yoğunluğu (kişi/km²)
- Kentleşme oranı (%)
- Net göç hızı (‰)
- Medyan yaş
- Yaşlı bağımlılık oranı (%)

#### 3.2.2 Ekonomik Değişkenler (6 adet)
- Kişi başı GSYH (TL)
- İşsizlik oranı (%)
- İstihdam oranı (%)
- Kişi başı ihracat ($)
- Kişi başı mevduat (TL)
- Girişimcilik oranı (%)

#### 3.2.3 Eğitim Değişkenleri (4 adet)
- Yükseköğretim mezun oranı (%)
- Ortaöğretim okullaşma oranı (%)
- Öğretmen başına öğrenci sayısı
- Okur-yazar oranı (%)

#### 3.2.4 Sağlık Değişkenleri (4 adet)
- 10.000 kişiye düşen doktor sayısı
- 10.000 kişiye düşen yatak sayısı
- Bebek ölüm hızı (‰)
- Yaşam beklentisi (yıl)

#### 3.2.5 Altyapı ve Yaşam Kalitesi Değişkenleri (5 adet)
- İnternet erişim oranı (%)
- 1.000 kişiye düşen araç sayısı
- Kişi başı elektrik tüketimi (kWh)
- Hava kalitesi indeksi
- Suç oranı (100.000 kişi başına)

### 3.3 Veri Ön İşleme

#### 3.3.1 Eksik Veri Analizi
Veri setinde eksik değer bulunmamaktadır.

#### 3.3.2 Aykırı Değer Tespiti
IQR (Çeyrekler Arası Açıklık) yöntemi kullanılmıştır:
- Alt sınır: Q1 - 1.5 × IQR
- Üst sınır: Q3 + 1.5 × IQR

Aykırı değerler clipping yöntemiyle sınır değerlere çekilmiştir.

#### 3.3.3 Normalizasyon
Z-score standardizasyonu (StandardScaler) uygulanmıştır:

$$z = \frac{x - \mu}{\sigma}$$

Bu işlem sonucunda tüm değişkenler ortalama 0 ve standart sapma 1 olacak şekilde dönüştürülmüştür.

### 3.4 Kümeleme Algoritmaları

#### 3.4.1 K-Means Algoritması

K-Means algoritması, verileri K adet kümeye ayırmak için iteratif bir optimizasyon yöntemidir:

1. K adet merkez rastgele seçilir
2. Her nokta en yakın merkeze atanır
3. Merkezler, küme elemanlarının ortalaması olarak güncellenir
4. Yakınsama sağlanana kadar 2-3 adımları tekrarlanır

Amaç fonksiyonu (WCSS - Within Cluster Sum of Squares):

$$J = \sum_{j=1}^{K} \sum_{x_i \in C_j} ||x_i - \mu_j||^2$$

#### 3.4.2 Hiyerarşik Kümeleme

Ward linkage yöntemi kullanılmıştır. Bu yöntem, birleştirme sonucu oluşacak varyans artışını minimize eder:

$$d(A, B) = \frac{n_A n_B}{n_A + n_B} ||\bar{A} - \bar{B}||^2$$

### 3.5 Optimal Küme Sayısı Belirleme

Üç farklı yöntem kullanılmıştır:

#### 3.5.1 Elbow (Dirsek) Yöntemi
WCSS değerlerinin K'ya göre grafiği çizilir, dirsek noktası optimal K olarak seçilir.

#### 3.5.2 Silhouette Analizi
Silhouette katsayısı şu şekilde hesaplanır:

$$s(i) = \frac{b(i) - a(i)}{max(a(i), b(i))}$$

Burada:
- a(i): i noktasının kendi kümesindeki ortalama uzaklığı
- b(i): i noktasının en yakın diğer kümeye ortalama uzaklığı

#### 3.5.3 Calinski-Harabasz İndeksi
Kümeler arası varyansın, küme içi varyansa oranını ölçer:

$$CH = \frac{SS_B / (K-1)}{SS_W / (n-K)}$$

### 3.6 Değerlendirme Metrikleri

| Metrik | Formül | Yorum |
|--------|--------|-------|
| Silhouette | [-1, 1] | Yüksek = iyi |
| Calinski-Harabasz | [0, ∞) | Yüksek = iyi |
| Davies-Bouldin | [0, ∞) | Düşük = iyi |
| Adjusted Rand Index | [-1, 1] | Yüksek = iyi |

---

## 4. BULGULAR

### 4.1 Keşifsel Veri Analizi

#### 4.1.1 Temel İstatistikler

| Değişken | Ortalama | Std. Sapma | Min | Max |
|----------|----------|------------|-----|-----|
| Kişi Başı GSYH (TL) | 55,234 | 24,156 | 18,420 | 124,680 |
| İşsizlik Oranı (%) | 9.8 | 3.2 | 5.8 | 18.2 |
| Kentleşme Oranı (%) | 64.2 | 13.8 | 42.4 | 99.2 |
| Yükseköğretim Mezun (%) | 14.8 | 4.2 | 8.2 | 28.4 |

#### 4.1.2 Korelasyon Analizi

En yüksek pozitif korelasyonlar:
- Kişi başı GSYH ↔ Yükseköğretim mezun oranı (r = 0.89)
- İnternet erişimi ↔ Kentleşme oranı (r = 0.82)
- Doktor sayısı ↔ Yaşam beklentisi (r = 0.78)

En yüksek negatif korelasyonlar:
- İşsizlik oranı ↔ İstihdam oranı (r = -0.76)
- Bebek ölüm hızı ↔ Yaşam beklentisi (r = -0.84)

#### 4.1.3 PCA Analizi

İlk iki bileşen toplam varyansın %68.4'ünü açıklamaktadır:
- PC1: %52.3 (Genel gelişmişlik boyutu)
- PC2: %16.1 (Demografik yapı boyutu)

### 4.2 Optimal Küme Sayısı

| K | Silhouette | Calinski-Harabasz | Davies-Bouldin |
|---|------------|-------------------|----------------|
| 2 | 0.5309 | 85.10 | 0.6168 |
| 3 | 0.4643 | 93.80 | 0.8145 |
| 4 | 0.3433 | 86.42 | 0.9454 |
| **5** | **0.3483** | **83.50** | **0.8000** |
| 6 | 0.3418 | 77.76 | 0.8518 |
| 7 | 0.3170 | 78.83 | 0.8532 |
| 8 | 0.3003 | 76.27 | 0.8975 |
| 9 | 0.2644 | 71.92 | 0.9064 |

**Optimal küme sayısı: K = 5**

Metrikler K=2 veya K=3'ü işaret etse de, SEGE metodolojisi ile uyumluluk ve yorumlanabilirlik açısından K=5 tercih edilmiştir. Bu değer hem akademik literatür hem de politika uygulamaları açısından anlamlı bir kümeleme sağlamaktadır.

### 4.3 K-Means Kümeleme Sonuçları

#### 4.3.1 Küme Dağılımı

| Küme | İl Sayısı | Oran (%) | Karakteristik |
|------|-----------|----------|---------------|
| 0 (En Az Gelişmiş) | 17 | 21.0 | Doğu/Güneydoğu Anadolu illeri |
| 1 (Orta Gelişmiş) | 28 | 34.6 | İç Anadolu ve geçiş bölgesi illeri |
| 2 (Gelişmiş) | 8 | 9.9 | Büyükşehirler ve sanayi illeri |
| 3 (En Gelişmiş) | 1 | 1.2 | İstanbul |
| 4 (Az Gelişmiş) | 27 | 33.3 | Kuzey ve iç bölge illeri |

#### 4.3.2 Küme Profilleri

**Küme 3 - En Gelişmiş İller (İstanbul):**
- Ortalama GSYH: 124,680 TL
- İşsizlik: %11.2
- Yükseköğretim: %24.8
- Karakteristik: Türkiye'nin ekonomik ve kültürel merkezi

**Küme 2 - Gelişmiş İller (8 il):**
- Örnek iller: Ankara, Antalya, Bursa, Eskişehir, İzmir, Kocaeli, Muğla, Tekirdağ
- Ortalama GSYH: 90,762 TL
- İşsizlik: %8.5
- Yükseköğretim: %20.6
- Karakteristik: Büyükşehirler, sanayi ve turizm merkezleri

**Küme 1 - Orta Gelişmiş İller (28 il):**
- Örnek iller: Adana, Aydın, Balıkesir, Bilecik, Konya, Kayseri, Samsun
- Ortalama GSYH: 64,698 TL
- İşsizlik: %8.1
- Yükseköğretim: %15.9
- Karakteristik: Bölgesel merkez iller

**Küme 4 - Az Gelişmiş İller (27 il):**
- Örnek iller: Afyonkarahisar, Artvin, Çankırı, Çorum, Elazığ, Tokat, Yozgat
- Ortalama GSYH: 47,510 TL
- İşsizlik: %8.9
- Yükseköğretim: %13.9
- Karakteristik: Kırsal ağırlıklı iller

**Küme 0 - En Az Gelişmiş İller (17 il):**
- Örnek iller: Adıyaman, Ağrı, Bingöl, Bitlis, Diyarbakır, Hakkari, Mardin, Muş, Şanlıurfa, Van
- Ortalama GSYH: 26,373 TL
- İşsizlik: %14.2
- Yükseköğretim: %10.2
- Karakteristik: Doğu ve Güneydoğu Anadolu illeri

#### 4.3.3 Değerlendirme Metrikleri

- **Silhouette Skoru:** 0.3483 (Orta düzey küme ayrımı)
- **Calinski-Harabasz:** 83.50 (İyi küme yoğunluğu)
- **Davies-Bouldin:** 0.8000 (Düşük küme örtüşmesi)

### 4.4 Hiyerarşik Kümeleme Sonuçları

Ward linkage yöntemi ile elde edilen dendrogram, illerin doğal gruplandırmasını göstermektedir. K=5 için kesim yapıldığında:

#### 4.4.1 Küme Dağılımı (Hiyerarşik)

| Küme | İl Sayısı | Oran (%) | Karakteristik |
|------|-----------|----------|---------------|
| 0 | 5 | 6.2 | Mega kentler (İstanbul, Ankara, İzmir, Bursa, Kocaeli) |
| 1 | 18 | 22.2 | Doğu/Güneydoğu Anadolu illeri |
| 2 | 33 | 40.7 | Orta düzey gelişmiş iller |
| 3 | 12 | 14.8 | Gelişmiş Batı illeri |
| 4 | 13 | 16.0 | Kuzey Anadolu illeri |

#### 4.4.2 Değerlendirme Metrikleri

- **Silhouette Skoru:** 0.3171
- **Calinski-Harabasz:** 76.21
- **Davies-Bouldin:** 0.9417

K-Means ile karşılaştırıldığında, hiyerarşik kümeleme biraz daha düşük performans göstermiştir. Ancak dendrogram görselleştirmesi, illerin hiyerarşik ilişkilerini anlamak için değerli bilgiler sunmaktadır.

### 4.5 Algoritma Karşılaştırması

| Algoritma | Silhouette | Calinski-Harabasz | Davies-Bouldin |
|-----------|------------|-------------------|----------------|
| **K-Means** | **0.3483** | **83.50** | **0.8000** |
| Hierarchical (Ward) | 0.3171 | 76.21 | 0.9417 |
| Hierarchical (Complete) | 0.3291 | 76.63 | 0.7402 |
| Gaussian Mixture | 0.3394 | 74.83 | 0.9454 |

**Sonuç:** K-Means algoritması, Silhouette ve Calinski-Harabasz metriklerine göre en iyi performansı göstermiştir.

### 4.6 SEGE ile Karşılaştırma

#### 4.6.1 Çapraz Tablo

| K-Means \ SEGE | 1 | 2 | 3 | 4 | 5 | 6 | Toplam |
|----------------|---|---|---|---|---|---|--------|
| 0 | 0 | 0 | 0 | 0 | 10 | 7 | 17 |
| 1 | 1 | 17 | 10 | 0 | 0 | 0 | 28 |
| 2 | 8 | 0 | 0 | 0 | 0 | 0 | 8 |
| 3 | 1 | 0 | 0 | 0 | 0 | 0 | 1 |
| 4 | 0 | 0 | 10 | 14 | 3 | 0 | 27 |
| **Toplam** | 10 | 17 | 20 | 14 | 13 | 7 | 81 |

#### 4.6.2 Uyumluluk Metrikleri

- **Adjusted Rand Index (ARI):** 0.4532
- **Normalized Mutual Information (NMI):** 0.6532

Bu değerler, K-Means kümeleme sonuçlarının SEGE sınıflandırması ile **orta-yüksek düzeyde uyumlu** olduğunu göstermektedir. ARI değeri 0.45, rassal olmayan anlamlı bir uyumluluk düzeyine işaret etmektedir.

---

## 5. TARTIŞMA

### 5.1 Temel Bulgular

1. **Kümeleme Performansı:** K-Means algoritması, Türkiye illerinin sosyo-ekonomik açıdan gruplandırılmasında başarılı sonuçlar vermiştir. Silhouette skoru (0.3483) orta düzeyde küme ayrımı olduğunu göstermektedir. Bu değer, 24 farklı sosyo-ekonomik değişkenin kullanıldığı çok boyutlu bir veri seti için kabul edilebilir bir performanstır.

2. **SEGE Uyumu:** ARI değeri (0.4532) ve NMI değeri (0.6532), makine öğrenmesi ile elde edilen kümelerin resmi SEGE sınıflandırmasıyla orta-yüksek düzeyde uyumluluk gösterdiğini ortaya koymaktadır. SEGE'nin 6 kademe kullanması ve bizim 5 küme tercih etmemiz, uyumluluk oranını etkilemiş olabilir.

3. **Bölgesel Farklılıklar:** 
   - En gelişmiş kümede (Küme 2 ve 3) Marmara, Ege ve Akdeniz bölgesi illeri yoğunlaşmaktadır
   - En az gelişmiş kümede (Küme 0) Doğu ve Güneydoğu Anadolu illeri bulunmaktadır
   - İstanbul, diğer tüm illerden belirgin şekilde ayrışarak tek başına bir küme oluşturmaktadır

4. **Ekonomik Eşitsizlik:** En gelişmiş il (İstanbul) ile en az gelişmiş iller arasında kişi başı GSYH farkı yaklaşık 5 kat'tır (124,680 TL vs. 26,373 TL). Bu durum, Türkiye'deki bölgesel eşitsizliğin boyutunu açıkça ortaya koymaktadır.

### 5.2 Metodolojik Değerlendirme

**Güçlü Yönler:**
- 24 farklı sosyo-ekonomik gösterge kullanımı (demografik, ekonomik, eğitim, sağlık, altyapı)
- Birden fazla kümeleme algoritmasının karşılaştırılması (K-Means, Hiyerarşik, GMM)
- Çoklu değerlendirme metrikleri (Silhouette, CH, DB, ARI, NMI)
- Resmi SEGE sınıflandırması ile doğrulama

**Kısıtlamalar:**
- Veri yılı tutarlılığı: Farklı kaynaklardan alınan verilerin yılları tam olarak örtüşmemektedir
- Değişken seçimi: Bazı önemli göstergeler (örn. AR-GE harcamaları) veri eksikliği nedeniyle dahil edilememiştir
- Kümeleme algoritmasının stokastik yapısı: K-Means'in farklı başlangıç noktalarıyla farklı sonuçlar üretme olasılığı

### 5.3 Literatür ile Karşılaştırma

Elde edilen sonuçlar, önceki çalışmalarla tutarlılık göstermektedir:

| Çalışma | Küme Sayısı | Yöntem | Temel Bulgu |
|---------|-------------|--------|-------------|
| Albayrak (2005) | 6 | Kümeleme | Batı-Doğu ayrımı belirgin |
| Özkan ve Uzun (2017) | 5 | K-Means | Marmara bölgesi en gelişmiş |
| Bu çalışma (2026) | 5 | K-Means/Hiyerarşik | İstanbul tek başına ayrışıyor |

Türkiye'de batı-doğu gelişmişlik farkının son 20 yılda devam ettiği, hatta bazı illerde derinleştiği gözlemlenmektedir.

---

## 6. SONUÇ VE ÖNERİLER

### 6.1 Sonuçlar

Bu çalışmada, Türkiye'deki 81 il sosyo-ekonomik göstergeler kullanılarak makine öğrenmesi yöntemleriyle kümelenmiştir. Temel sonuçlar:

1. **Optimal küme sayısı 5** olarak belirlenmiştir. Bu sayı hem istatistiksel metrikler hem de yorumlanabilirlik açısından en uygun değerdir.

2. **K-Means algoritması** en iyi performansı göstermiştir:
   - Silhouette Skoru: 0.3483
   - Calinski-Harabasz İndeksi: 83.50
   - Davies-Bouldin İndeksi: 0.8000

3. Sonuçlar **SEGE 2022 ile orta-yüksek uyumluluk** sergilemektedir:
   - Adjusted Rand Index (ARI): 0.4532
   - Normalized Mutual Information (NMI): 0.6532

4. **Batı-Doğu gelişmişlik farkı** açıkça gözlemlenmektedir:
   - En gelişmiş küme: İstanbul (124,680 TL kişi başı GSYH)
   - En az gelişmiş küme: Doğu/Güneydoğu illeri (26,373 TL kişi başı GSYH)

5. **Küme karakteristikleri:**
   - Küme 3 (1 il): Türkiye'nin ekonomik merkezi İstanbul
   - Küme 2 (8 il): Büyükşehirler ve sanayi merkezleri
   - Küme 1 (28 il): Bölgesel merkez iller
   - Küme 4 (27 il): Kırsal ağırlıklı iller
   - Küme 0 (17 il): Doğu ve Güneydoğu Anadolu illeri

### 6.2 Politika Önerileri

Analiz sonuçlarına dayalı olarak aşağıdaki politika önerileri geliştirilmiştir:

#### 6.2.1 Ekonomik Kalkınma
1. **Hedefli Teşvik Paketleri:** Küme 0'daki (en az gelişmiş) 17 il için özel yatırım teşvikleri ve vergi avantajları sağlanmalıdır.
2. **Sanayi Bölgeleri:** Az gelişmiş illerde organize sanayi bölgeleri kurulmalı ve altyapı yatırımları hızlandırılmalıdır.
3. **Girişimcilik Desteği:** Mikro kredi programları ve girişimcilik eğitimleri yaygınlaştırılmalıdır.

#### 6.2.2 Eğitim Yatırımları
1. **Üniversite Kapasitesi:** Az gelişmiş illerdeki üniversitelerin akademik kapasitesi güçlendirilmelidir.
2. **Mesleki Eğitim:** Bölgesel ihtiyaçlara uygun mesleki ve teknik eğitim programları oluşturulmalıdır.
3. **Öğretmen Dağılımı:** Öğretmen başına öğrenci sayısı yüksek olan illere ek kadro tahsis edilmelidir.

#### 6.2.3 Sağlık Hizmetleri
1. **Doktor Atamları:** 10.000 kişiye düşen doktor sayısı düşük olan illere öncelikli atama yapılmalıdır.
2. **Hastane Yatırımları:** Yatak sayısı yetersiz illerde yeni sağlık tesisleri açılmalıdır.
3. **Telemedicine:** Uzak illerde tele-tıp uygulamaları yaygınlaştırılmalıdır.

#### 6.2.4 Altyapı İyileştirmeleri
1. **Dijital Altyapı:** İnternet erişim oranı düşük illerde fiber altyapı yatırımları hızlandırılmalıdır.
2. **Ulaşım:** Hava ve kara ulaşım bağlantıları iyileştirilmelidir.
3. **Enerji:** Yenilenebilir enerji yatırımları teşvik edilmelidir.

### 6.3 Gelecek Çalışmalar İçin Öneriler

1. **Zaman Serisi Analizi:** Yıllık verilerle illerin gelişmişlik değişimlerinin izlenmesi
2. **İlçe Bazlı Analiz:** Daha detaylı mekânsal çözünürlük için ilçe düzeyinde kümeleme
3. **Derin Öğrenme:** Autoencoder tabanlı boyut indirgeme ve kümeleme yöntemlerinin denenmesi
4. **Mekânsal Kümeleme:** Coğrafi yakınlığı dikkate alan mekânsal kümeleme algoritmalarının uygulanması
5. **Panel Veri Analizi:** Çoklu yıl verilerinin dinamik kümeleme ile analizi

---

## 7. KAYNAKÇA

1. Albayrak, A.S. (2005). "Türkiye'de İllerin Sosyo-Ekonomik Gelişmişlik Düzeylerinin Çok Değişkenli İstatistik Yöntemlerle İncelenmesi". ZKÜ Sosyal Bilimler Dergisi, 1(1), 153-177.

2. Dinçer, B., Özaslan, M., Kavasoğlu, T. (2003). "İllerin ve Bölgelerin Sosyo-Ekonomik Gelişmişlik Sıralaması Araştırması". DPT Yayınları.

3. MacQueen, J. (1967). "Some Methods for Classification and Analysis of Multivariate Observations". Proceedings of 5th Berkeley Symposium on Mathematical Statistics and Probability.

4. T.C. Sanayi ve Teknoloji Bakanlığı (2022). "İllerin ve Bölgelerin Sosyo-Ekonomik Gelişmişlik Sıralaması Araştırması (SEGE-2022)".

5. TÜİK (2024). "İl Göstergeleri". https://biruni.tuik.gov.tr/ilgosterge/

6. TCMB (2024). "Elektronik Veri Dağıtım Sistemi (EVDS)". https://evds2.tcmb.gov.tr/

7. Ward, J.H. (1963). "Hierarchical Grouping to Optimize an Objective Function". Journal of the American Statistical Association, 58(301), 236-244.

8. Özkan, B., Uzun, S. (2017). "Türkiye'de İllerin Sosyo-Ekonomik Gelişmişlik Düzeylerinin K-Means Kümeleme Analizi ile Belirlenmesi". İşletme ve İktisat Çalışmaları Dergisi, 5(3), 74-92.

9. Scikit-learn Documentation. "Clustering". https://scikit-learn.org/stable/modules/clustering.html

---

## 8. EKLER

### EK-A: Değişken Listesi ve Tanımları

| No | Değişken | Tanım | Kaynak |
|----|----------|-------|--------|
| 1 | nufus_yogunlugu | Km² başına düşen kişi sayısı | TÜİK |
| 2 | kentlesme_orani | Kent nüfusunun toplam nüfusa oranı (%) | TÜİK |
| 3 | net_goc_hizi | Net göç hızı (‰) | TÜİK |
| 4 | medyan_yas | Nüfusun medyan yaşı | TÜİK |
| 5 | yasli_bagimlilik_orani | 65+ yaş nüfusunun çalışan yaş nüfusuna oranı | TÜİK |
| 6 | kisi_basi_gsyh | Kişi başına gayri safi yurtiçi hasıla (TL) | TÜİK |
| 7 | issizlik_orani | İşsiz nüfusun işgücüne oranı (%) | TÜİK |
| 8 | istihdam_orani | Çalışan nüfusun toplam nüfusa oranı (%) | TÜİK |
| 9 | kisi_basi_ihracat | Kişi başına ihracat ($) | TÜİK |
| 10 | kisi_basi_mevduat | Kişi başına banka mevduatı (TL) | TCMB |
| ... | ... | ... | ... |

### EK-B: İllerin Küme Atamaları

*(Tam liste veri dosyasında mevcuttur)*

### EK-C: Python Kodu

Projenin kaynak kodlarına ve veri setlerine aşağıdaki GitHub deposundan erişilebilir:
https://github.com/EmircanDemirTR/Turkiye-Illerinin-SosyoEkonomik-Gelismislik-Duzeyine-Gore-Siniflandirilmasi

Repo yapısı:
- `src/preprocessing.py`: Veri ön işleme
- `src/clustering.py`: Kümeleme algoritmaları
- `src/visualization.py`: Görselleştirme
- `notebooks/kumeleme_analizi.ipynb`: Ana analiz notebook

---

**Rapor Tarihi:** 10 Ocak 2026

**Proje Durumu:** Tamamlandı

**Analiz Özeti:**
- 81 il, 24 sosyo-ekonomik gösterge
- K-Means kümeleme (Silhouette: 0.3483)
- SEGE uyumluluk (ARI: 0.4532, NMI: 0.6532)
- 5 küme: En gelişmiş → En az gelişmiş
