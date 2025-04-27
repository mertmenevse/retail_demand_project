import pandas as pd
import lightgbm as lgb

# 1. Modeli yükle
model = lgb.Booster(model_file="retail_demand_model.txt")

# 2. Test verisini oku
X_test = pd.read_csv("X_test.csv")

# 3. Tahmin yap
y_pred = model.predict(X_test)

# 4. Sonuçları kaydet
output = pd.DataFrame({
    "Prediction": y_pred
})

output.to_csv("predictions.csv", index=False)

print("Tahminler başarıyla 'predictions.csv' dosyasına kaydedildi.")
