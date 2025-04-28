import time
import subprocess
from datetime import datetime

def generate_report():
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Starting report generation...")
    result = subprocess.run(["python", "generate_report.py"], capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Report successfully generated.")
    else:
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Error generating report:\n{result.stderr}")

if __name__ == "__main__":
    while True:
        generate_report()
        print("Waiting 5 minutes before next report...\n")
        time.sleep(5 * 60)  # 5 dakika bekle
