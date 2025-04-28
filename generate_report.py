import pandas as pd
import lightgbm as lgb
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from fpdf import FPDF
from datetime import datetime
import os

# 1. Load model
model = lgb.Booster(model_file="retail_demand_model.txt")

# 2. Load test data
X_test = pd.read_csv("X_test.csv")
y_test = pd.read_csv("y_test.csv").squeeze()

# 3. Predict
y_pred = model.predict(X_test)

# 4. Calculate RMSE
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

# 5. Save predictions
predictions = pd.DataFrame({"Prediction": y_pred})
predictions.to_csv("predictions.csv", index=False)

# 6. Load retail sales data
sales_data = pd.read_csv("retail_sales.csv")

# 7. Create a plot
plt.figure(figsize=(16, 8))
sales_data.groupby('Category')['Sales'].sum().sort_values().plot(kind='barh')
plt.title("Sales Distribution by Category", fontsize=14)
plt.xlabel("Total Sales", fontsize=12)
plt.ylabel("Category", fontsize=12)
plt.tight_layout()
plt.savefig("temp_chart.png")
plt.close()

# 8. Create the report
pdf = FPDF()
pdf.add_page()

pdf.set_font("Arial", size=16)
pdf.cell(200, 10, txt="Retail Demand Project Report", ln=True, align='C')

pdf.set_font("Arial", size=12)
pdf.ln(10)
pdf.cell(200, 10, txt=f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align='L')

pdf.ln(10)
pdf.cell(200, 10, txt=f"Model RMSE: {rmse:.4f}", ln=True, align='L')

pdf.ln(10)
pdf.cell(200, 10, txt="Sales Distribution Chart:", ln=True, align='L')

pdf.image("temp_chart.png", x=10, y=70, w=190)

# Create reports folder if it doesn't exist
if not os.path.exists("reports"):
    os.makedirs("reports")

# Save PDF
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
pdf.output(f"reports/performance_report_{timestamp}.pdf")

print(f"New report successfully generated: reports/performance_report_{timestamp}.pdf")
