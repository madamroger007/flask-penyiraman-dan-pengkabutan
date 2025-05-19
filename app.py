from app import create_app, socketio  # Ambil socketio dari app/__init__.py
import threading
from app.src.services.mqtt_service import run_mqtt_service
from app.src.services.data_sensor_service import start_scheduled_jobs
from app.src.services.naive_bayes_train_service import train_naive_bayes
from app.src.services.control_service import auto_control_loop  # Import fungsi auto control
app = create_app()


if __name__ == "__main__":
    # Jalankan MQTT di thread terpisah
    mqtt_thread = threading.Thread(target=run_mqtt_service, daemon=True)
    mqtt_thread.start()
    train_naive_bayes()
    scheduler_thread = threading.Thread(target=start_scheduled_jobs, daemon=True)
    scheduler_thread.start()
    auto_control_thread = threading.Thread(target=auto_control_loop, daemon=True)  # thread baru untuk auto control
    auto_control_thread.start()
     # Mulai penjadwalan otomatis setelah semua komponen terdaftar
    from app.src.services.penjadwalan_service import jadwal_service_utama

    with app.app_context():
        jadwal_service_utama()
    # Menjalankan scheduler di thread terpisah

    # Jalankan Flask dengan WebSocket (via SocketIO)
    socketio.run(app, debug=True, use_reloader=False)
