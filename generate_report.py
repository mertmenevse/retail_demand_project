import pandas as pd
import matplotlib.pyplot as plt
import lightgbm as lgb
from sklearn.metrics import mean_squared_error
import joblib
import os
from datetime import datetime

# Verileri oku
sales_data = pd.read_csv("retail_sales.csv")
X_test = pd.read_csv("X_test.csv")
y_test = pd.read_csv("y_test.csv")

# Modeli yükle
model = lgb.Booster(model_file='retail_demand_model.txt')

# Tahmin yap
predictions = model.predict(X_test)

# Performans metriğini hesapla
rmse = mean_squared_error(y_test, predictions, squared=False)

# Grafik oluştur
plt.figure(figsize=(10,6))
sales_data.groupby('Product Category')['Total Amount'].sum().sort_values().plot(kind='barh')
plt.title("Sales by Product Category", fontsize=14)
plt.xlabel("Total Sales", fontsize=12)
plt.ylabel("Product Category", fontsize=12)
plt.tight_layout()

# Grafik dosyasını kaydet
chart_filename = "temp_chart.png"
plt.savefig(chart_filename)
plt.close()

# PDF oluştur
from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Retail Demand Report', ln=True, align='C')
        self.ln(10)

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, title, ln=True, align='L')
        self.ln(5)

    def chapter_body(self, text):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, text)
        self.ln()

# PDF yazımı
pdf = PDF()
pdf.add_page()
pdf.chapter_title("Model Performance")
pdf.chapter_body(f"Root Mean Squared Error (RMSE): {rmse:.4f}")
pdf.chapter_title("Sales by Category")
pdf.image(chart_filename, w=180)

# Klasör yoksa oluştur
if not os.path.exists("reports"):
    os.makedirs("reports")

# PDF kaydet
now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
pdf.output(f"reports/performance_report_{now}.pdf")

print(f"New report generated: reports/performance_report_{now}.pdf")
