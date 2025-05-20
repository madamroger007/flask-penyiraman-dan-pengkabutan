from app import create_app, socketio
import threading
from app.src.services.mqtt_service import run_mqtt_service
from app.src.services.data_sensor_service import start_scheduled_jobs
from app.src.services.naive_bayes_train_service import train_naive_bayes
from app.src.services.control_service import auto_control_loop
from app.src.services.penjadwalan_service import jadwal_service_utama

app = create_app()

def start_background_services():
    threading.Thread(target=run_mqtt_service, daemon=True).start()
    threading.Thread(target=lambda: start_scheduled_jobs(app), daemon=True).start()
    threading.Thread(target=auto_control_loop, daemon=True).start()
    threading.Thread(target=train_naive_bayes, daemon=True).start()

    def run_jadwal():
        with app.app_context():
            jadwal_service_utama(app)

    threading.Thread(target=run_jadwal, daemon=True).start()


if __name__ == "__main__":
    start_background_services()
    socketio.run(app, debug=True, use_reloader=False)
