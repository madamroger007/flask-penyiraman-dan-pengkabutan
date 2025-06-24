from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import pytz
import os
from twilio.rest import Client
from app.src.services.naive_bayes_train_service import predict_status
from app.src.services.mqtt_service import latest_sensor_data
from dotenv import load_dotenv
from app.src.services.notification_service import notify_sensor_data_Service
from app.src.repositories.data_sensor_repositories import (
    create_data_sensor_repository,
    get_all_data_sensors_repository,
)
load_dotenv()

# Inisialisasi scheduler dengan zona waktu Jakarta
scheduler = BackgroundScheduler(timezone=pytz.timezone('Asia/Jakarta'))

def _scheduled_prediction(app):
    with app.app_context():
        print(f"🔄 Emit WebSocket: Kelembapan Tanah = {latest_sensor_data.get('Kelembapan Tanah')}")

        if None in latest_sensor_data.values():
            print("❌ Data sensor tidak lengkap untuk prediksi.")
            return

        prediction = predict_status(latest_sensor_data)
        if not prediction:
            print("❌ Gagal melakukan prediksi.")
            return

        # Ambil status penyiraman dan pengkabutan dari hasil prediksi
        status_penyiraman = prediction.get('Penyiraman')
        status_pengkabutan = prediction.get('Pengkabutan')

        data_sensor = {
            'suhu': latest_sensor_data['Suhu Udara'],
            'kelembapan_udara': latest_sensor_data['Kelembapan Udara'],
            'kelembapan_tanah': latest_sensor_data['Kelembapan Tanah'],
            'penyiraman': status_penyiraman == 'Perlu' if status_penyiraman == True else False,
            'pengkabutan': status_pengkabutan == 'Perlu' if status_pengkabutan == True else False,
        }
        print(f"📊 Data sensor: {data_sensor}")
        # Kirim notifikasi jika perlu
        if status_penyiraman == 'Perlu':
            notify_sensor_data_Service(
                f"Penyiraman diperlukan.\n"
                f"➡️ Suhu: {data_sensor['suhu']}°C\n"
                f"➡️ Kelembapan Udara: {data_sensor['kelembapan_udara']}%\n"
                f"➡️ Kelembapan Tanah: {data_sensor['kelembapan_tanah']}%\n"
                f"📡 Akses: {os.getenv('FLASK_URL')}",app
            )
        if status_pengkabutan == 'Perlu':
            notify_sensor_data_Service(
                f"Pengkabutan diperlukan.\n"
                f"➡️ Suhu: {data_sensor['suhu']}°C\n"
                f"➡️ Kelembapan Udara: {data_sensor['kelembapan_udara']}%\n"
                f"➡️ Kelembapan Tanah: {data_sensor['kelembapan_tanah']}%\n"
                f"📡 Akses: {os.getenv('FLASK_URL')}",app
            )

        print(f"🔮 Prediksi status: {prediction}")
        create_data_sensor_repository(data_sensor)


def start_scheduled_jobs(app):
    times = ['03:00', '06:00', '09:00', '12:00','15:00', '18:00', '21:00', '00:00']
    for time_str in times:
        hour, minute = map(int, time_str.strip().split(':'))
        
        scheduler.add_job( 
            _scheduled_prediction,
            CronTrigger(hour=hour, minute=minute, second=0),
            args=[app],
            id=f"predict_{hour:02d}{minute:02d}",
            replace_existing=True
        )
    scheduler.start()
    print("🕒 Penjadwalan tugas prediksi dimulai.")

def get_all_data_sensors_service():
    return get_all_data_sensors_repository()


