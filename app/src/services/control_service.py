from app.src.repositories.riwayat_aksi_repositories import create_riwayat_aksi_repository,get_all_riwayat_aksi_repository
from app.src.services.mqtt_service import kirim_perintah_siram, kirim_perintah_kabut
# Akses latest_sensor_data dari mqtt_service
from app.src.services.mqtt_service import latest_sensor_data
from app.src.services.notification_service import notify_sensor_data_Service
import time
from datetime import datetime
from dotenv import load_dotenv
import os
from flask import current_app as app
load_dotenv()

def kontrol_penyiraman_service(perintah):
    kirim_perintah_siram(perintah)
    created_notification_service(perintah,"penyiraman")

def kontrol_pengkabutan_service(perintah):
    kirim_perintah_kabut(perintah)
    created_notification_service(perintah,"pengkabutan")
   

def created_notification_service(perintah,action=None):
    data = {
        "jenis_aksi": action,
        "status": "aktif" if perintah == "1" else "nonaktif"
    }
    status = "Aktif" if perintah == "1" else "Mati"
    waktu = datetime.now().strftime('Tanggal %d-%m-%Y, jam :%H:%M')
    flask_url = os.getenv('FLASK_URL')
    pesan = f"Akses Dashboard {flask_url}. 🚨 {action}: {status}. {waktu}"
    notify_sensor_data_Service(pesan, app)
    create_riwayat_aksi_repository(data)
    notify_sensor_data_Service(pesan, app)

def get_jadwal_penyiraman_service():
    # Implement the logic to retrieve the watering schedule from the database
    get_all_riwayat_aksi = get_all_riwayat_aksi_repository()
    return get_all_riwayat_aksi

def auto_control_loop():
    print("🚀 Auto Control Service started")
    while True:
        kelembapan_tanah = latest_sensor_data.get("Kelembapan Tanah")
        suhu_udara = latest_sensor_data.get("Suhu Udara")
        kelembapan_udara = latest_sensor_data.get("Kelembapan Udara")

        if kelembapan_tanah is not None and kelembapan_tanah > 80:
            kirim_perintah_siram("0")
        if suhu_udara is not None and kelembapan_udara is not None:
            print(f"Suhu Udara: {suhu_udara}, Kelembapan Udara: {kelembapan_udara}")
            if suhu_udara < 27 and kelembapan_udara > 71:
                kirim_perintah_kabut("0")  # Matikan kabut
        time.sleep(5)  # Delay untuk menghindari loop terlalu cepat