from app import create_app, socketio  # Ambil socketio dari app/__init__.py
import os
import threading
from app.src.services.mqtt_service import run_mqtt_service

app = create_app()

if __name__ == "__main__":
    # Jalankan MQTT di thread terpisah
    mqtt_thread = threading.Thread(target=run_mqtt_service, daemon=True)
    mqtt_thread.start()

    # Jalankan Flask dengan WebSocket (via SocketIO)
    socketio.run(app, debug=True, use_reloader=False)
