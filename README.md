# 📦 Retail Demand Prediction & Monitoring System

## 🚀 Proje Özeti

Bu proje, perakende satış verilerini kullanarak talep tahmini yapan bir yapay zeka (LightGBM) modelini:

- Docker container'ı içinde çalıştırır,
- Performansını Prometheus & Grafana ile gerçek zamanlı izler,
- Otomatik PDF raporlar oluşturur,
- Flask tabanlı bir web panelde raporları erişilebilir hale getirir,
- GitHub Actions + Watchtower ile otomatik CI/CD sücrecine sahiptir.

---

## ⚙️ Kullanılan Teknolojiler

- Python 3.11
- LightGBM
- Scikit-learn
- Pandas, Numpy, Matplotlib, FPDF
- Flask
- Prometheus + Grafana
- Docker + Docker Hub
- GitHub Actions (CI/CD)
- Watchtower (Otomatik Docker Güncelleyici)

---

## 📂 Proje Yapısı

```
retail_demand_project/
├── predict.py                  # AI model tahmin + Prometheus metrics
├── generate_report.py           # PDF rapor üretimi
├── report_scheduler.py          # 5 dakikada bir otomatik rapor üretimi
├── webserver.py                 # Flask webserver (rapor gösterimi)
├── retail_demand_model.txt      # Eğitilmiş LightGBM model
├── X_test.csv                   # Test verisi
├── y_test.csv                   # Gerçek sonuçlar
├── predictions.csv              # Model tahmin sonuçları
├── retail_sales.csv             # Ham satış verisi
├── reports/                     # Otomatik oluşan PDF raporlar
├── Dockerfile                   # Model ve metrics için
├── Dockerfile.report            # Rapor scheduler için
├── Dockerfile.web               # Flask webserver için
├── requirements.txt             # Python kütüphaneleri listesi
└── prometheus.yml               # Prometheus ayarları
```

---

## ⚡️ Kurulum Adımları

### 1. Docker Image'ını Build Et

```bash
docker build -t mertmenevse/retail-demand-project .
docker build -f Dockerfile.report -t mertmenevse/retail-report-scheduler .
docker build -f Dockerfile.web -t mertmenevse/retail-webserver .
```

### 2. Container'ı Başlat

```bash
# AI model + Prometheus Metrics
docker run -d --name retail-demand-project -p 8000:8000 mertmenevse/retail-demand-project

# Rapor Scheduler
docker run -d --name retail-report-scheduler -v %cd%/reports:/app/reports mertmenevse/retail-report-scheduler

# Webserver
docker run -d --name retail-webserver -p 5000:5000 -v %cd%/reports:/app/reports mertmenevse/retail-webserver
```

### 3. Prometheus ve Grafana Kurulumu

```bash
docker run -d --name prometheus-server -p 9090:9090 -v %cd%/prometheus.yml:/etc/prometheus/prometheus.yml prom/prometheus
docker run -d --name grafana -p 3000:3000 grafana/grafana
```

### 4. Watchtower ile Otomatik Güncelleme

```bash
docker run -d --name watchtower --restart unless-stopped -v //var/run/docker.sock:/var/run/docker.sock containrrr/watchtower --cleanup --interval 30
```

---

## 🌍 Web Paneller

| Uygulama | Adres |
|:---|:---|
| Predict Metrics | [http://localhost:8000/metrics](http://localhost:8000/metrics) |
| Prometheus | [http://localhost:9090](http://localhost:9090) |
| Grafana | [http://localhost:3000](http://localhost:3000) |
| Web Rapor Paneli | [http://localhost:5000](http://localhost:5000) |

---

## 📈 Dashboard ve Raporlama Özeti

- **Grafana** üzerinde `model_rmse` metriği izleniyor.
- **5 dakikada 1** PDF raporlar otomatik oluşur.
- **Flask Webserver** üzerinden raporlar anlık listelenir ve indirilebilir.

---

## 📢 Olası Sorunlar ve Çözümler

- **Prometheus veri çekmiyor**: `host.docker.internal` adresini kontrol et.
- **Watchtower çalışmıyor**: Docker servislerini yeniden başlat.
- **Volume hatası**: Windows için volume yollarında `//` kullan.
- **Docker Build hatası**: Eksik dosya veya klasör ("reports/" gibi) eksikliğini kontrol et.

---

## 👨‍💻 Geliştirici

- GitHub: [@mertmenevse](https://github.com/mertmenevse)


