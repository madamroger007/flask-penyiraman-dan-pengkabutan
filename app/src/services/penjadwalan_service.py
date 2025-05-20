from app.src.repositories.jadwal_penyiraman_repositories import update_jadwal_by_id_repository, create_jadwal_penyiraman_repository
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz
from app.src.services.control_service import kontrol_penyiraman_service,kontrol_pengkabutan_service
from app.src.repositories.jadwal_penyiraman_repositories import get_jadwal_penyiraman_by_jenis_repository
from flask import current_app
from app import socketio
scheduler = BackgroundScheduler(timezone=pytz.timezone('Asia/Jakarta'))

# penjadwalan_service.py

scheduler = BackgroundScheduler(timezone=pytz.timezone('Asia/Jakarta'))

app = None  # global app instance

def init_app(app_instance):
    global app
    app = app_instance


def update_jadwal_service(jadwal_id, waktu_1, waktu_2, jenis):
    try:
        if jadwal_id is None:
            create_jadwal = {
                "waktu_1": waktu_1,
                "waktu_2": waktu_2,
                "jenis_aksi": jenis
            }
            jadwal = create_jadwal_penyiraman_repository(create_jadwal)
            return {"success": True, "jadwal": {
                "id": jadwal.id,
                "waktu_1": jadwal.waktu_1.strftime("%H:%M:%S"),
                "waktu_2": jadwal.waktu_2.strftime("%H:%M:%S"),
                "jenis_aksi": jadwal.jenis_aksi
            }}
        jadwal = update_jadwal_by_id_repository(jadwal_id, waktu_1, waktu_2, jenis)
        return {"success": True, "jadwal": {
            "id": jadwal.id,
            "waktu_1": jadwal.waktu_1.strftime("%H:%M:%S"),
            "waktu_2": jadwal.waktu_2.strftime("%H:%M:%S"),
            "jenis_aksi": jadwal.jenis_aksi
        }}
    except Exception as e:
        print("Error update_jadwal:", e)
        return {"success": False}


# Wrapper supaya fungsi kontrol dijalankan dalam Flask app context
def kontrol_penyiraman_service_wrapper(perintah):
    with app.app_context():
        kontrol_penyiraman_service(perintah)

def kontrol_pengkabutan_service_wrapper(perintah):
    with app.app_context():
        kontrol_pengkabutan_service(perintah)




def jadwal_penyiraman_service():
    penyiraman = get_jadwal_penyiraman_by_jenis_repository(jenis_aksi='penyiraman')
    if not penyiraman:
        print("⚠️ Jadwal penyiraman tidak ditemukan di database.")
        return

    times = [penyiraman.waktu_1, penyiraman.waktu_2]

    for idx, time_obj in enumerate(times):
        try:
            hour = time_obj.hour
            minute = time_obj.minute
            job_id = f"penyiraman_{idx+1}_{hour:02d}{minute:02d}"

            if not scheduler.get_job(job_id):
                scheduler.add_job(
                    func=kontrol_penyiraman_service_wrapper,
                    trigger=CronTrigger(hour=hour, minute=minute, second=0),
                    id=job_id,
                    replace_existing=True,
                    kwargs={"perintah": "1"}  # <-- Inject app
                )
        except Exception as e:
            print(f"❌ Gagal menambahkan job untuk waktu '{time_obj}': {e}")

    if not scheduler.running:
        scheduler.start()
        print("🕒 Penjadwalan tugas penyiraman dimulai.")
    else:
        print("🕒 Scheduler sudah berjalan.")



def jadwal_pengkabutan_service():
    pengkabutan = get_jadwal_penyiraman_by_jenis_repository(jenis_aksi='pengkabutan')

    if not pengkabutan:
        print("⚠️ Jadwal pengkabutan tidak ditemukan di database.")
        return

    times = [pengkabutan.waktu_1, pengkabutan.waktu_2]

    for idx, time_obj in enumerate(times):
        try:
            hour = time_obj.hour
            minute = time_obj.minute
            job_id = f"pengkabutan_{idx+1}_{hour:02d}{minute:02d}"

            if not scheduler.get_job(job_id):
                scheduler.add_job(
                    func=kontrol_pengkabutan_service_wrapper,
                    trigger=CronTrigger(hour=hour, minute=minute, second=0),
                    id=job_id,
                    replace_existing=True,
                    kwargs={"perintah": "1"}  # <-- Inject app
                )
              
        except Exception as e:
            print(f"❌ Gagal menambahkan job untuk waktu '{time_obj}': {e}")

    if not scheduler.running:
        scheduler.start()
        print("🕒 Penjadwalan tugas pengkabutan dimulai.")
    else:
        print("🕒 Scheduler sudah berjalan.")


def refresh_jadwal_service(jenis_aksi: str):
    """ Hapus semua job untuk jenis aksi lalu jadwalkan ulang berdasarkan data terbaru. """
    prefix = f"{jenis_aksi}_"
    job_ids = [job.id for job in scheduler.get_jobs() if job.id.startswith(prefix)]

    for job_id in job_ids:
        scheduler.remove_job(job_id)

    if jenis_aksi == "penyiraman":
        jadwal_penyiraman_service()
    elif jenis_aksi == "pengkabutan":
        jadwal_pengkabutan_service()


def jadwal_service_utama(app_instance):
    init_app(app_instance)  # Simpan app global
    jadwal_penyiraman_service()
    jadwal_pengkabutan_service()


