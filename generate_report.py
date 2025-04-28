import pandas as pd
import matplotlib.pyplot as plt
import lightgbm as lgb
import numpy as np
from sklearn.metrics import mean_squared_error
from fpdf import FPDF
from datetime import datetime
import os

# 1. Canlı model yükleme ve tahmin
model = lgb.Booster(model_file="retail_demand_model.txt")
X_test = pd.read_csv("X_test.csv")
y_true = pd.read_csv("y_test.csv").squeeze()
y_pred = model.predict(X_test)

# 2. Canlı RMSE hesaplama
mse = mean_squared_error(y_true, y_pred)
rmse = np.sqrt(mse)

# 3. Satış verisini oku
sales_data = pd.read_csv("retail_sales.csv")

# 4. Grafik oluştur
plt.figure(figsize=(10, 6))
sales_data.groupby('Category')['Sales'].sum().sort_values(ascending=False).plot(kind='bar')
plt.title('Sales Distribution by Category')
plt.ylabel('Total Sales')
plt.xticks(rotation=45, ha='right')  # X eksenindeki yazıları yatık yap, tamamen göster
plt.tight_layout()
chart_path = "reports/temp_chart.png"
plt.savefig(chart_path)
plt.close()

# 5. PDF oluştur
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
pdf_path = f"reports/performance_report_{timestamp}.pdf"

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", "B", 16)
pdf.cell(0, 10, "Retail Demand Prediction Report", ln=True, align="C")

pdf.set_font("Arial", size=12)
pdf.ln(10)
pdf.cell(0, 10, f"Generated at: {timestamp}", ln=True)
pdf.cell(0, 10, f"Model RMSE: {rmse:.4f}", ln=True)

pdf.ln(10)
pdf.cell(0, 10, "Sales Distribution by Category:", ln=True)
pdf.image(chart_path, x=10, y=None, w=190)

pdf.output(pdf_path)

# 6. Geçici grafik dosyasını sil
if os.path.exists(chart_path):
    os.remove(chart_path)

print(f"New report successfully created: {pdf_path}")
