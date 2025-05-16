from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import pytz
from app.src.services.naive_bayes_train_service import predict_status
from app.src.repositories.data_sensor_repositories import read_all_sensor_data

# Inisialisasi scheduler
scheduler = BackgroundScheduler(timezone=pytz.timezone('Asia/Jakarta'))

def scheduled_prediction():
    # Ambil data sensor terbaru
    sensor_data_list = read_all_sensor_data()
    if not sensor_data_list:
        print("❌ Tidak ada data sensor untuk diproses.")
        return

    # Ambil data sensor terakhir
    latest_data = sensor_data_list[-1]

    # Persiapkan data untuk prediksi
    sensor_data = {
        "Suhu Udara": latest_data.suhu_udara,
        "Kelembapan Udara": latest_data.kelembapan_udara,
        "Kelembapan Tanah": latest_data.kelembapan_tanah
    }

    # Lakukan prediksi status
    prediction = predict_status(sensor_data)
    if prediction:
        print(f"🔮 Prediksi status: {prediction}")
    else:
        print("❌ Gagal melakukan prediksi.")


def start_scheduled_jobs():
    """
    Menjadwalkan tugas prediksi pada jam-jam tertentu setiap hari.
    """
    # Menambahkan tugas prediksi pada jam 09:00, 12:00, 15:00, 18:00, 21:00, dan 00:00
    times = ['09:00', '12:00', '15:00', '18:00', '21:00', '00:00']
    for time in times:
        scheduler.add_job(
            scheduled_prediction,
            CronTrigger(hour=int(time.split(':')[0]), minute=int(time.split(':')[1]), second=0),
            id=f"predict_{time.replace(':', '')}"
        )
    scheduler.start()
    print("Penjadwalan tugas prediksi dimulai.")

# Panggil fungsi start_scheduled_jobs() di tempat yang sesuai dalam aplikasi Anda
