import time
import os

while True:
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp} - Running live prediction...")
    os.system("python predict.py")  # Önce yeni prediction alınacak

    print(f"{timestamp} - Generating new report...")
    os.system("python generate_report.py")  # Sonra yeni rapor üretilecek

    print("Waiting 5 minutes...\n")
    time.sleep(300)  # 5 dakika bekle
