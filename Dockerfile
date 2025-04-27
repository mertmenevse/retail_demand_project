FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y libgomp1

COPY requirements.txt .
COPY predict.py .
COPY retail_demand_model.txt .
COPY X_test.csv .
COPY y_test.csv .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "predict.py"]
