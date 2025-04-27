import pandas as pd
import lightgbm as lgb
import numpy as np
from sklearn.metrics import mean_squared_error
from prometheus_client import start_http_server, Gauge
import time

# Watchtower Testi için hemen başta print
print("Watchtower Test: Yeni Versiyon Çalışıyor!")

# 1. Modeli yükle
model = lgb.Booster(model_file="retail_demand_model.txt")

# 2. Test verisini oku
X_test = pd.read_csv("X_test.csv")

# 3. Tahmin yap
y_pred = model.predict(X_test)

# 4. RMSE hesapla
y_true = pd.read_csv("y_test.csv").squeeze()
mse = mean_squared_error(y_true, y_pred)
rmse = np.sqrt(mse)

# 5. Tahminleri kaydet
output = pd.DataFrame({"Prediction": y_pred})
output.to_csv("predictions.csv", index=False)

print(f"Tahminler başarıyla 'predictions.csv' dosyasına kaydedildi.")
print(f"Test Seti RMSE: {rmse}")

# 6. Prometheus için Metric başlat
rmse_gauge = Gauge('model_rmse', 'Real-time RMSE value of the model')

def update_metrics():
    while True:
        rmse_gauge.set(rmse)
        time.sleep(5)

if __name__ == "__main__":
    # Metric server başlat
    start_http_server(8000)  # localhost:8000 adresinde metrik yayınlanacak
    print("Prometheus metrics server 8000 portunda başladı.")
    
    # Sonsuz metrik güncellemesi
    update_metrics()
