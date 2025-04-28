import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from fpdf import FPDF
import datetime
import os

# 1. Verileri oku
data = pd.read_csv("retail_sales.csv")
predictions = pd.read_csv("predictions.csv")
y_true = pd.read_csv("y_test.csv").squeeze()

# 2. RMSE hesapla
mse = mean_squared_error(y_true, predictions["Prediction"])
rmse = mse ** 0.5

# 3. PDF raporu oluştur
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)

# 4. Satış Dağılımı Grafiği
plt.figure(figsize=(10, 6))
data["Product Category"].value_counts().plot(kind="bar")
plt.title("Ürün Kategorilerine Göre Satış Dağılımı")
plt.savefig("sales_distribution.png")
pdf.image("sales_distribution.png", x=10, y=20, w=180)

# 5. RMSE Bilgisi
pdf.set_y(100)
pdf.cell(200, 10, txt=f"Model RMSE: {rmse:.4f}", ln=1, align="C")

# 6. Zaman damgası oluştur
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# 7. /reports klasörü yoksa oluştur
if not os.path.exists("reports"):
    os.makedirs("reports")

# 8. PDF'i kayıt et
pdf_path = f"reports/performance_report_{timestamp}.pdf"
pdf.output(pdf_path)

print(f"Yeni rapor başarıyla oluşturuldu: {pdf_path}")
