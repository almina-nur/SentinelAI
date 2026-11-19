
# SentinelAI - AI-Powered Cybersecurity Analyst

Güvenlik sistemlerinden gelen logları analiz ederek şüpheli davranışları tespit eden ve güvenlik analistlerine olay incelemesinde yardımcı olan yapay zeka destekli bir platform.

## Projenin Amacı ve Çözdüğü Problem

Kurum sistemlerinde her gün binlerce hatta milyonlarca log oluşmaktadır. Bu logların manuel incelenmesi imkansızdır. SentinelAI, aşağıdaki türdeki anomalileri otomatik tespit etmek ve analistlere sunmak için geliştirilmiştir:

- Aynı IP adresinden çok sayıda başarısız giriş yapılması (Brute Force)
- Olağan dışı saatlerde oturum açılması
- Normal kullanıcı davranışından sapmalar
- Yetkisiz erişim girişimleri

**Temel Prensiplerimiz:**
- Yapay zekanın her şüpheli olayı kesin saldırı olarak etiketlememesi.
- Yanlış pozitiflerin (False Positive) ölçülmesi ve minimize edilmesi.
- Halüsinasyon riskini sıfırlamak için kural tabanlı doğrulama kullanılması.

## Geliştirilen Modüller

| Modül | Açıklama | Durum |
| :--- | :--- | :--- |
| Log Collector & Parser | Log dosyalarını sisteme alma ve standartlaştırma | Tamamlandı |
| Anomaly Detection | Olağan dışı davranışları belirleme (Isolation Forest & PyTorch) | Tamamlandı |
| Threat Classification | Güvenlik olaylarını sınıflandırma (Kural Motoru) | Tamamlandı |
| MITRE ATT&CK Mapping | Tespitleri ilgili saldırı teknikleriyle ilişkilendirme | Tamamlandı |
| AI Assistant | Güvenlik olaylarını doğal dille açıklama (RAG & LLM) | Tamamlandı |
| Incident Dashboard | Olayları önem derecesine göre gösterme (Streamlit) | Tamamlandı |

## Kullanılan Teknolojiler

- **Veri İşleme:** Python, Pandas, PyArrow (Parquet)
- **Makine Öğrenmesi:** Scikit-learn (Isolation Forest), PyTorch (Autoencoder)
- **Yapay Zeka & NLP:** HuggingFace Transformers (Qwen), Sentence-Transformers, FAISS (RAG)
- **Backend & Veritabanı:** FastAPI, PostgreSQL, SQLAlchemy
- **Frontend & Arayüz:** Streamlit
- **Altyapı & Dağıtım:** Docker, Google Colab (Geliştirme ortamı)

## Değerlendirme ve Mühendislik Çözümleri

Proje geliştirilirken karşılaşılan temel zorluklar ve uygulanan mühendislik çözümleri:

1. **Yanlış Alarm (False Positive) Optimizasyonu:**
   - *Başlangıç Durumu:* "Gece girişi" kuralı 261 normal logu yanlışlıkla saldırı olarak işaretledi (Precision: 0.27).
   - *Çözüm:* Kullanıcı geçmiş davranışını (baseline) kontrol eden bir kural yazıldı. Precision skoru 0.89'a yükseltildi, analistin önüne giden gereksiz alarm sayısı 12'ye düşürüldü.

2. **LLM Halüsinasyonu Yönetimi:**
   - *Başlangıç Durumu:* Küçük dil modeli (Qwen 0.5B) Türkçe raporlarda bağlam dışı aksiyonlar üretti.
   - *Çözüm:* Hibrit yaklaşım benimsendi. Aksiyonlar (IP bloklama, şifre değiştirme) deterministik olarak Python `if-else` yapılarıyla koda gömüldü. LLM sadece metin özetleme ve çıkarım aşamasında kullanıldı.

3. **Veri Hattı (Data Pipeline) Tutarlılığı:**
   - *Başlangıç Durumu:* Model çıktılarının (örneğin `anomaly` sütunu) notebook'lar arası aktarımda kaybolması.
   - *Çözüm:* Her adımın çıktısı `logs_with_anomaly.parquet` ve `logs_classified.parquet` gibi anlamlı isimlerle diske kaydedildi. Veri sızıntısını (data leakage) önlemek için `fit_transform` yerine sadece `transform` kullanıldı.

## Proje Yapısı

```text
SentinelAI/
├── data/
│   ├── raw/                  # Ham loglar
│   ├── processed/            # İşlenmiş veriler (Parquet)
│   └── mitre/                # MITRE ATT&CK referansları
├── models/                   # Eğitilmiş modeller
├── notebooks/                # Geliştirme aşamaları
│   ├── 01_log_parser.ipynb
│   ├── 02_threat_classification.ipynb
│   ├── 03_ai_assistant_rag.ipynb
│   └── 04_full_stack_production.ipynb
├── reports/                  # Değerlendirme raporları
├── app.py                    # Streamlit Dashboard
├── api.py                    # FastAPI Backend
├── Dockerfile                # Docker konfigürasyonu
├── requirements.txt          # Python bağımlılıkları
└── README.md
```

## Kurulum ve Çalıştırma

Projeyi kendi ortamınızda çalıştırmak için:

1. Depoyu klonlayın:
   ```bash
   git clone https://github.com/kullanici_adiniz/SentinelAI.git
   cd SentinelAI
   ```
2. Gerekli kütüphaneleri yükleyin:
   ```bash
   pip install -r requirements.txt
   ```
3. Streamlit uygulamasını başlatın:
   ```bash
   streamlit run app.py
   ```

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır.
```

