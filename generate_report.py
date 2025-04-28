import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
from sklearn.metrics import mean_squared_error
import os
from datetime import datetime

# 1. Load data
sales_data = pd.read_csv("retail_sales.csv")
predictions = pd.read_csv("predictions.csv")
y_true = pd.read_csv("y_test.csv").squeeze()

# 2. Calculate RMSE
mse = mean_squared_error(y_true, predictions['Prediction'])
rmse = mse ** 0.5

# 3. Sales per category
sales_per_category = sales_data.groupby("Product Category")["Quantity"].sum()

# 4. Create bar chart
plt.figure(figsize=(12, 6))
sales_per_category.plot(kind='bar')
plt.title("Sales by Product Category")
plt.xlabel("Product Category")
plt.ylabel("Quantity Sold")
plt.xticks(rotation=45, ha='right')  # Rotate labels for better visibility
plt.tight_layout()
if not os.path.exists("reports"):
    os.makedirs("reports")
plt.savefig("reports/temp_chart.png")
plt.close()

# 5. Create PDF
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
pdf = FPDF()
pdf.add_page()

# Title
pdf.set_font("Arial", 'B', 16)
pdf.cell(0, 10, "Retail Demand Prediction Report", ln=True, align='C')
pdf.ln(10)

# Insert RMSE
pdf.set_font("Arial", '', 12)
pdf.cell(0, 10, f"Model RMSE: {rmse:.4f}", ln=True)
pdf.ln(5)

# Insert Chart
pdf.image("reports/temp_chart.png", x=10, y=None, w=pdf.w - 20)

# Save PDF
report_filename = f"reports/performance_report_{timestamp}.pdf"
pdf.output(report_filename)

print(f"New report successfully created: {report_filename}")
