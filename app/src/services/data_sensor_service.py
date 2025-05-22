from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import pytz
import os
from twilio.rest import Client
from app.src.services.naive_bayes_train_service import predict_status
from app.src.services.mqtt_service import latest_sensor_data
from dotenv import load_dotenv
import requests
from app.src.repositories.nohp_repositories import (
    get_all_nomor_hp,
)

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

        # Kirim notifikasi jika perlu
        if status_penyiraman == 'Perlu':
            notify_sensor_data(
                f"Penyiraman diperlukan.\n"
                f"➡️ Suhu: {data_sensor['suhu']}°C\n"
                f"➡️ Kelembapan Udara: {data_sensor['kelembapan_udara']}%\n"
                f"➡️ Kelembapan Tanah: {data_sensor['kelembapan_tanah']}%\n"
                f"📡 Akses: {os.getenv('FLASK_URL')}"
            )
        if status_pengkabutan == 'Perlu':
            notify_sensor_data(
                f"Pengkabutan diperlukan.\n"
                f"➡️ Suhu: {data_sensor['suhu']}°C\n"
                f"➡️ Kelembapan Udara: {data_sensor['kelembapan_udara']}%\n"
                f"➡️ Kelembapan Tanah: {data_sensor['kelembapan_tanah']}%\n"
                f"📡 Akses: {os.getenv('FLASK_URL')}"
            )

        print(f"🔮 Prediksi status: {prediction}")
        create_data_sensor_repository(data_sensor)


def start_scheduled_jobs(app):
    times = ['03:00', '06:00', '09:00', '12:00', '15:00', '18:00', '21:00', '00:00']
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

def notify_sensor_data(msg):
    wa_server_url = os.getenv('WA_SERVER_URL')
    session_id = os.getenv('WA_SESSION_ID')

    if not wa_server_url:
        print("❌ WA_SERVER_URL tidak ditemukan di .env")
        return
    if not session_id:
        print("❌ WA_SESSION_ID tidak ditemukan di .env")
        return

    try:
        # Ambil semua nomor dari database
        numbers = get_all_nomor_hp()

        if not numbers:
            print("⚠️ Tidak ada nomor WA yang ditemukan di database.")
            return

        for record in numbers:
            phone_number = record.nomor_hp if hasattr(record, 'nomor_hp') else record['nomor_hp']

            payload = {
                "number": phone_number,
                "message": msg,
                "sessionId": session_id
            }

            try:
                response = requests.post(wa_server_url, json=payload)
                response.raise_for_status()
                res_json = response.json()

                if res_json.get("status") == "success":
                    print(f"✅ Pesan berhasil dikirim ke {phone_number}")
                else:
                    print(f"❌ Gagal kirim ke {phone_number}: {res_json}")

            except requests.exceptions.RequestException as err:
                print(f"❌ Error koneksi ke {phone_number}: {err}")

    except Exception as e:
        print(f"❌ Error saat mengambil nomor dari database: {e}")
