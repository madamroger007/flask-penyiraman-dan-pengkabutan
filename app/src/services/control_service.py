from app.src.repositories.riwayat_aksi_repositories import create_riwayat_aksi
from app.src.services.mqtt_service import kirim_perintah_siram, kirim_perintah_kabut

def kontrol_penyiraman_service(perintah):
    kirim_perintah_siram(perintah)
    data = {
        "jenis_aksi": "penyiraman",
        "status": "aktif" if perintah == "1" else "nonaktif"
    }
    create_riwayat_aksi(data)

def kontrol_pengkabutan_service(perintah):
    kirim_perintah_kabut(perintah)
    data = {
        "jenis_aksi": "pengkabutan",
        "status": "aktif" if perintah == "1" else "nonaktif"
    }
    create_riwayat_aksi(data)
