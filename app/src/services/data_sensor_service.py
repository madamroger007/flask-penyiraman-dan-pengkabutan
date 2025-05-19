from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import pytz
from app import create_app
from app.src.services.naive_bayes_train_service import predict_status
from app.src.services.mqtt_service import latest_sensor_data
from app.src.repositories.data_sensor_repositories import create_data_sensor_repository,get_all_data_sensors_repository

# Inisialisasi scheduler dengan zona waktu Jakarta
scheduler = BackgroundScheduler(timezone=pytz.timezone('Asia/Jakarta'))

def scheduled_prediction():
    from app import create_app
    app = create_app()
    with app.app_context():  # ✅ Gunakan context Flask
        print("🔄 Emit WebSocket: Kelembapan Tanah =", latest_sensor_data.get("Kelembapan Tanah"))

        # Periksa apakah semua data tersedia
        if None in latest_sensor_data.values():
            print("❌ Data sensor tidak lengkap untuk prediksi.")
            return

        # Lakukan prediksi
        prediction = predict_status(latest_sensor_data)
        if prediction:
            print(f"🔮 Prediksi status: {prediction}")
               # Konversi hasil prediksi ke boolean
            penyiraman_bool = str(prediction['Penyiraman']) == 'Perlu'
            pengkabutan_bool = str(prediction['Pengkabutan']) == 'Perlu'
            # Simpan ke database
            data_sensor = {
                'suhu': latest_sensor_data['Suhu Udara'],
                'kelembapan_udara': latest_sensor_data['Kelembapan Udara'],
                'kelembapan_tanah': latest_sensor_data['Kelembapan Tanah'],
                'penyiraman': penyiraman_bool,
                'pengkabutan': pengkabutan_bool,
            }
            create_data_sensor_repository(data_sensor)
        else:
            print("❌ Gagal melakukan prediksi.")

def start_scheduled_jobs():
    times = ['03:00','06:00','09:00', '12:00', '15:00', ' 18:00', '21:00', '00:00']
    for time in times:
        hour, minute = map(int, time.split(':'))
        scheduler.add_job(
            scheduled_prediction,
            CronTrigger(hour=hour, minute=minute, second=0),
            id=f"predict_{hour:02d}{minute:02d}"
        )
    scheduler.start()
    print("🕒 Penjadwalan tugas prediksi dimulai.")

def get_all_data_sensors_service():
    return get_all_data_sensors_repository()
