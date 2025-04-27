import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF

# 1. Tahmin sonuçlarını oku
predictions = pd.read_csv("predictions.csv")

# 2. Gerçek değerleri oku
y_test = pd.read_csv("y_test.csv").squeeze()

# 3. RMSE hesapla
from sklearn.metrics import mean_squared_error
import numpy as np

mse = mean_squared_error(y_test, predictions["Prediction"])
rmse = np.sqrt(mse)

# 4. Grafik çiz
plt.figure(figsize=(10,6))
plt.plot(y_test.values, label="Gerçek Değerler")
plt.plot(predictions["Prediction"].values, label="Tahminler")
plt.legend()
plt.title("Gerçek vs Tahmin")
plt.xlabel("Örnek")
plt.ylabel("Miktar")
plt.savefig("comparison_plot.png")
plt.close()

# 5. PDF Raporu oluştur
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)

# Başlık
pdf.cell(200, 10, txt="Retail Demand Prediction Report", ln=True, align="C")

# RMSE değeri
pdf.ln(10)
pdf.cell(200, 10, txt=f"RMSE: {rmse:.4f}", ln=True, align="C")

# Grafik ekle
pdf.ln(10)
pdf.image("comparison_plot.png", x=10, y=40, w=180)

# PDF'i kaydet
pdf.output("performance_report.pdf")

print("PDF raporu başarıyla oluşturuldu: performance_report.pdf")
