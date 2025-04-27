# Python 3.11 slim imajını kullan
FROM python:3.11-slim

# Çalışma dizini
WORKDIR /app

# Sisteme gerekli bağımlılıkları kur
RUN apt-get update && apt-get install -y libgomp1

# Gerekli dosyaları kopyala
COPY requirements.txt .
COPY predict.py .
COPY retail_demand_model.txt .
COPY X_test.csv .

# Kütüphaneleri yükle
RUN pip install --no-cache-dir -r requirements.txt

# Container başlarken predict.py çalıştır
CMD ["python", "predict.py"]