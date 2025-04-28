import time
import subprocess
from datetime import datetime

def run_report():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    print(f"{timestamp} - Yeni rapor oluşturuluyor...")
    subprocess.run(["python", "generate_report.py"])
    print(f"{timestamp} - Rapor başarıyla oluşturuldu.")

if __name__ == "__main__":
    while True:
        run_report()
        print("5 dakika bekleniyor...")
        time.sleep(300)
