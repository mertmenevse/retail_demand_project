import pandas as pd
import lightgbm as lgb
import numpy as np
from sklearn.metrics import mean_squared_error
from prometheus_client import start_http_server, Gauge
import time

# Başlangıç mesajı
print("Watchtower Test: Dinamik Versiyon Çalışıyor!")

# 1. Modeli yükle
model = lgb.Booster(model_file="retail_demand_model.txt")

# 2. Prometheus için Metric başlat
rmse_gauge = Gauge('model_rmse', 'Real-time RMSE value of the model')

# 3. Dinamik RMSE güncelleme fonksiyonu
def update_metrics():
    while True:
        # X_test.csv'yi oku
        X_test = pd.read_csv("X_test.csv")

        # Küçük random değişiklikler yap (simülasyon için)
        noise = np.random.normal(0, 1, X_test.shape)
        X_test_simulated = X_test + noise

        # Yeni tahminler yap
        y_pred = model.predict(X_test_simulated)

        # Gerçek değerleri oku
        y_true = pd.read_csv("y_test.csv").squeeze()

        # Yeni RMSE hesapla
        mse = mean_squared_error(y_true, y_pred)
        rmse = np.sqrt(mse)

        # Prometheus metriğini güncelle
        rmse_gauge.set(rmse)

        # Ayrıca loga yaz
        print(f"Yeni hesaplanan RMSE: {rmse}")

        # 5 saniye bekle
        time.sleep(5)

if __name__ == "__main__":
    # Metric server başlat
    start_http_server(8000)
    print("Prometheus metrics server 8000 portunda başladı.")
    
    # Metrikleri sürekli güncelle
    update_metrics()
