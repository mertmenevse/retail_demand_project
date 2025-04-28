import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
import numpy as np
from sklearn.metrics import mean_squared_error
from datetime import datetime
import os

# 1. Verileri yükle
sales_data = pd.read_csv("retail_sales.csv")
predictions = pd.read_csv("predictions.csv")
y_true = pd.read_csv("y_test.csv").squeeze()

# 2. RMSE hesapla
mse = mean_squared_error(y_true, predictions['Prediction'])
rmse = mse ** 0.5

# 3. Satış Dağılımı Grafiği
plt.figure(figsize=(10,6))
sales_data['Product Category'].value_counts().plot(kind='bar')
plt.title("Ürün Kategorilerine Göre Satış Dağılımı")
plt.xlabel("Ürün Kategorisi")
plt.ylabel("Satış Sayısı")
plt.tight_layout()
if not os.path.exists("reports"):
    os.makedirs("reports")
plt.savefig("reports/sales_distribution.png")
plt.close()

# 4. Gerçek vs Tahmin Grafiği
plt.figure(figsize=(10,6))
plt.plot(y_true.values, label="Gerçek Değerler")
plt.plot(predictions['Prediction'].values, label="Tahminler", linestyle="--")
plt.title(f"Gerçek vs Tahmin (RMSE: {rmse:.4f})")
plt.xlabel("Veri Nokası")
plt.ylabel("Quantity")
plt.legend()
plt.tight_layout()
plt.savefig("reports/prediction_vs_actual.png")
plt.close()

# 5. PDF Raporu Oluştur
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", 'B', 16)
pdf.cell(200, 10, txt="Perakende Talep Tahmini Performans Raporu", ln=True, align="C")

pdf.set_font("Arial", size=12)
current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
pdf.cell(200, 10, txt=f"Tarih: {current_time}", ln=True, align="C")

pdf.ln(10)
pdf.set_font("Arial", size=11)
pdf.multi_cell(0, 10, 
"""Sistemde belirli aralıklarla çalışan generate_report.py scripti ile, hem satış 
dağılımı hem de modelin performans metrikleri analiz edilmekte ve bu analizler PDF formatında bir rapora 
dönüştürülmektedir. Rapor içerisinde grafiksel gösterimler, kategori bazlı satış istatistikleri ve model doğruluğu 
bilgisi yer almaktadır. Bu raporlar, karar vericilerin sistem hakkındaki güncel durumu anlaması ve stratejik adımlar 
atabilmesi için referans kaynağı olarak kullanılmaktadır."""
)

pdf.ln(10)
pdf.set_font("Arial", 'B', 14)
pdf.cell(200, 10, txt="Ürün Kategorilerine Göre Satış Dağılımı", ln=True)
pdf.image("reports/sales_distribution.png", x=10, y=None, w=190)

pdf.ln(85)
pdf.set_font("Arial", 'B', 14)
pdf.cell(200, 10, txt="Gerçek vs Tahmin Grafiği", ln=True)
pdf.image("reports/prediction_vs_actual.png", x=10, y=None, w=190)

pdf.ln(85)
pdf.set_font("Arial", 'B', 14)
pdf.cell(200, 10, txt=f"Model Performansı (RMSE): {rmse:.4f}", ln=True)

# Timestamp ile dosya adı
timestamp_for_filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
pdf_path = f"reports/performance_report_{timestamp_for_filename}.pdf"
pdf.output(pdf_path)

print(f"Performans raporu başarıyla oluşturuldu: {pdf_path}")
