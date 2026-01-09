# Türkiye İlleri Sosyo-Ekonomik Kümeleme Projesi

## 📋 Proje Hakkında

Bu proje, Türkiye'deki 81 ilin gelişmişlik ve sosyo-ekonomik seviyelerine göre kümeleme analizi yapan bir makine öğrenmesi çalışmasıdır. Lisans bitirme projesi olarak hazırlanmıştır.

## 🎯 Amaç

- 81 ilin sosyo-ekonomik göstergelerini analiz etmek
- K-Means ve Hiyerarşik Kümeleme algoritmaları ile illeri gruplandırmak
- Gelişmişlik düzeylerine göre küme profilleri oluşturmak
- Sonuçları SEGE (Sosyo-Ekonomik Gelişmişlik Endeksi) ile karşılaştırmak

## 📁 Proje Yapısı

```
bitirme-projesi/
├── data/
│   ├── raw/                    # Ham veriler
│   ├── processed/              # İşlenmiş veriler
│   └── external/               # Harici kaynaklar (GeoJSON vb.)
├── notebooks/
│   └── kumeleme_analizi.ipynb  # Ana analiz notebook
├── src/
│   ├── __init__.py
│   ├── preprocessing.py        # Veri ön işleme
│   ├── clustering.py           # Kümeleme algoritmaları
│   └── visualization.py        # Görselleştirme
├── reports/
│   ├── figures/                # Grafikler ve haritalar
│   └── final_report.md         # Bitirme raporu
├── requirements.txt
├── README.md
└── config.yaml
```

## 📊 Veri Kaynakları

| Kaynak | Veri Türü | URL |
|--------|-----------|-----|
| TÜİK | Nüfus, İstihdam, Eğitim, Sağlık | https://biruni.tuik.gov.tr/ilgosterge/ |
| SEGE 2022 | Gelişmişlik Endeksi | Sanayi ve Teknoloji Bakanlığı |
| Hava Kalitesi | PM10, Hava Kalitesi İndeksi | https://sim.csb.gov.tr/ |

## 🔧 Kullanılan Değişkenler

### Demografik (5 değişken)
- Nüfus yoğunluğu (kişi/km²)
- Kentleşme oranı (%)
- Net göç hızı (‰)
- Medyan yaş
- Yaşlı bağımlılık oranı (%)

### Ekonomik (6 değişken)
- Kişi başı GSYH (TL)
- İşsizlik oranı (%)
- İstihdam oranı (%)
- Kişi başı ihracat ($)
- Kişi başı mevduat (TL)
- Girişimcilik oranı (%)

### Eğitim (4 değişken)
- Yükseköğretim mezun oranı (%)
- Ortaöğretim okullaşma oranı (%)
- Öğretmen başına öğrenci sayısı
- Okur-yazar oranı (%)

### Sağlık (4 değişken)
- 10.000 kişiye düşen doktor sayısı
- 10.000 kişiye düşen yatak sayısı
- Bebek ölüm hızı (‰)
- Yaşam beklentisi (yıl)

### Altyapı ve Yaşam Kalitesi (5 değişken)
- İnternet erişim oranı (%)
- 1.000 kişiye düşen araç sayısı
- Kişi başı elektrik tüketimi (kWh)
- Hava kalitesi indeksi
- Suç oranı (100.000 kişi başına)

## 🚀 Kurulum ve Çalıştırma

```bash
# Sanal ortam oluştur
python -m venv venv
venv\Scripts\activate  # Windows

# Bağımlılıkları yükle
pip install -r requirements.txt

# Jupyter notebook başlat
jupyter notebook notebooks/kumeleme_analizi.ipynb
```

## 📈 Metodoloji

1. **Veri Toplama**: TÜİK, TCMB ve resmi kaynaklardan il bazlı veri derleme
2. **Veri Ön İşleme**: Eksik veri analizi, normalizasyon, aykırı değer tespiti
3. **Keşifsel Analiz**: Korelasyon analizi, PCA ile boyut indirgeme
4. **Kümeleme**: K-Means ve Hiyerarşik Kümeleme algoritmaları
5. **Değerlendirme**: Silhouette, Calinski-Harabasz, Davies-Bouldin metrikleri
6. **Görselleştirme**: Türkiye haritası üzerinde küme gösterimi

## 📝 Lisans

Bu proje lisans bitirme tezi kapsamında hazırlanmıştır.

## 👤 Yazar

Bitirme Projesi - Güz Dönemi 2025-2026
