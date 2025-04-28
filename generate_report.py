import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
import datetime
from sklearn.metrics import mean_squared_error

# 1. Load Data
sales_data = pd.read_csv("retail_sales.csv")
predictions = pd.read_csv("predictions.csv")
y_true = pd.read_csv("y_test.csv").squeeze()

# 2. Calculate RMSE
mse = mean_squared_error(y_true, predictions['Prediction'])
rmse = mse ** 0.5

# 3. Create a new PDF
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)

# 4. Add Title
pdf.cell(200, 10, txt="Retail Demand Prediction Report", ln=True, align="C")
pdf.ln(10)

# 5. Add RMSE Score
pdf.cell(200, 10, txt=f"Model RMSE Score: {rmse:.4f}", ln=True, align="C")
pdf.ln(10)

# 6. Create Sales Distribution Plot
plt.figure(figsize=(12,6))
sales_data["Product Category"].value_counts().plot(kind="bar")
plt.title("Sales Distribution by Product Category")
plt.xlabel("Product Categories")
plt.ylabel("Number of Sales")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("sales_distribution.png")
plt.close()

# 7. Add Image to PDF
pdf.image("sales_distribution.png", x=10, y=None, w=190)

# 8. Save PDF to reports folder
now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
output_path = f"reports/performance_report_{now}.pdf"
pdf.output(output_path)

print(f"New report successfully created: {output_path}")
