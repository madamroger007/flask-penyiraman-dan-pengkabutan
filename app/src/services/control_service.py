from app.src.repositories.riwayat_aksi_repositories import create_riwayat_aksi_repository,get_all_riwayat_aksi_repository
from app.src.services.mqtt_service import kirim_perintah_siram, kirim_perintah_kabut
# Akses latest_sensor_data dari mqtt_service
from app.src.services.mqtt_service import latest_sensor_data
import time

def kontrol_penyiraman_service(perintah):
    kirim_perintah_siram(perintah)
    data = {
        "jenis_aksi": "penyiraman",
        "status": "aktif" if perintah == "1" else "nonaktif"
    }
    create_riwayat_aksi_repository(data)

def kontrol_pengkabutan_service(perintah):
    kirim_perintah_kabut(perintah)
    data = {
        "jenis_aksi": "pengkabutan",
        "status": "aktif" if perintah == "1" else "nonaktif"
    }
    create_riwayat_aksi_repository(data)

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

        if kelembapan_tanah is not None and kelembapan_tanah > 50:
            kirim_perintah_siram("0")
            print(f"🔔 [AutoControl] Kelembapan tanah {kelembapan_tanah} > 50, kirim perintah siram=0")

        if suhu_udara is not None and kelembapan_udara is not None:
            if suhu_udara > 30 and kelembapan_udara > 50:
                kirim_perintah_kabut("0")
                print(f"🔔 [AutoControl] Suhu udara {suhu_udara} > 30 dan kelembapan udara {kelembapan_udara} > 50, kirim perintah kabut=0")

        time.sleep(1)