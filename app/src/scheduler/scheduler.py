# app/src/scheduler/scheduler.py

import schedule
import time
from datetime import datetime
from app.src.services.data_sensor_service import scheduled_prediction

def job():
    print(f"🔄 Menjalankan prediksi status pada {datetime.now()}")
    scheduled_prediction()

def start_scheduled_jobs():
    # Daftar waktu yang diinginkan untuk menjalankan prediksi
    times = ["09:00", "12:00", "15:00", "18:00", "21:00", "00:00"]
    
    for t in times:
        schedule.every().day.at(t).do(job)
        print(f"✅ Menjadwalkan prediksi pada pukul {t}")
    
    while True:
        schedule.run_pending()
        time.sleep(60)  # Tunggu selama 1 menit sebelum memeriksa jadwal berikutnya
