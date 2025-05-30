import paho.mqtt.client as paho
from paho import mqtt
import os
import time
import requests
from datetime import datetime, timedelta
import ssl
import certifi
from dotenv import load_dotenv
from app import socketio  # Untuk emit ke client
from app.src.services.notification_service import notify_sensor_data_Service
from flask import current_app
# Memuat variabel lingkungan dari file .env
load_dotenv()

# 🔧 Konfigurasi MQTT & Flask API
BROKER = os.environ.get('MQTT_BROKER', '')
PORT = 8883
USERNAME = os.environ.get('MQTT_USERNAME')
PASSWORD = os.environ.get('MQTT_PASSWORD')
FLASK_URL = os.environ.get('FLASK_URL')
# mqtt_service.py
app_context = None
TOPICS = [
    ("otomatis/siram/status", 1),
    ("otomatis/kabut/status", 1),
    ("sensor/kelembapan_tanah", 1),
    ("sensor/suhu_udara", 1),
    ("sensor/kelembapan_udara", 1)
]

# 🔄 Data sensor & waktu terakhir update
latest_sensor_data = {
    "Suhu Udara": None,
    "Kelembapan Udara": None,
    "Kelembapan Tanah": None
}

sensor_last_seen = {
    "Suhu Udara": None,
    "Kelembapan Udara": None,
    "Kelembapan Tanah": None
}

sensor_last_value = {
    "Suhu Udara": None,
    "Kelembapan Udara": None,
    "Kelembapan Tanah": None
}

sensor_last_change = {
    "Suhu Udara": None,
    "Kelembapan Udara": None,
    "Kelembapan Tanah": None
}

SENSOR_TIMEOUT_SECONDS = 10
SENSOR_STALE_SECONDS = 60  # ⏰ Jika nilai tidak berubah dalam 1 menit, beri peringatan

client = None

# 🟢 Callback koneksi MQTT
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("✅ Terhubung ke MQTT Broker")
        for topic, qos in TOPICS:
            client.subscribe(topic, qos)
            print(f"📡 Berlangganan ke: {topic}")
    else:
        print(f"❌ Koneksi MQTT gagal, kode: {rc}")

# 📥 Callback untuk data sensor
def handle_sensor_data(client, userdata, msg):
    topic = msg.topic
    value = msg.payload.decode('utf-8').strip()

    mapping = {
        "sensor/kelembapan_tanah": "Kelembapan Tanah",
        "sensor/suhu_udara": "Suhu Udara",
        "sensor/kelembapan_udara": "Kelembapan Udara",
    }

    label = mapping.get(topic)
    if label:
        try:
            value_float = float(value)
        except ValueError:
            print(f"❌ Nilai sensor tidak valid: {value}")
            return

        now = datetime.now()
        last_val = sensor_last_value[label]

        # Deteksi perubahan nilai
        if last_val != value_float:
            sensor_last_change[label] = now
            sensor_last_value[label] = value_float

        latest_sensor_data[label] = value_float
        sensor_last_seen[label] = now

        
        socketio.emit("sensor_update", latest_sensor_data)

# ⛔ Cek timeout data dan perubahan nilai
def check_sensor_status():
    now = datetime.now()
    updated = False

    for label in latest_sensor_data:
        last_seen = sensor_last_seen.get(label)
        last_change = sensor_last_change.get(label)
        val = latest_sensor_data[label]

        # Reset jika data sudah usang
        if last_seen and (now - last_seen).total_seconds() > SENSOR_TIMEOUT_SECONDS:
            if val is not None:
                latest_sensor_data[label] = None
                updated = True
                print(f"⚠️ Data {label} tidak update >{SENSOR_TIMEOUT_SECONDS}s. Di-reset.")
        
        # Peringatan jika tidak berubah dalam 60 detik
        if last_change and (now - last_change).total_seconds() > SENSOR_STALE_SECONDS:
            notify_sensor_data_Service(
                f"🚨 Peringatan: {label} tidak berubah selama lebih dari 1 jam.\n"
                f" Cek sinyal atau perangkat.\n",  app_context
            )
            print(f"🚨 WARNING: {label} tidak berubah selama lebih dari 1 jam")

    if updated:
        socketio.emit("sensor_update", latest_sensor_data)

# 🚀 Jalankan MQTT
def run_mqtt_service(app_instance):
    global app_context
    app_context = app_instance
    global client
    print(f"🔌 Menghubungkan ke MQTT {BROKER}:{PORT}")
    
    client = paho.Client(client_id="otomatisasi_penyiram", protocol=paho.MQTTv5)
    client.username_pw_set(USERNAME, PASSWORD)
    client.tls_set(ca_certs=certifi.where(), tls_version=ssl.PROTOCOL_TLS_CLIENT)

    client.on_connect = on_connect
    client.message_callback_add("sensor/kelembapan_tanah", handle_sensor_data)
    client.message_callback_add("sensor/suhu_udara", handle_sensor_data)
    client.message_callback_add("sensor/kelembapan_udara", handle_sensor_data)

    try:
        client.connect(BROKER, PORT)
        client.loop_start()
    except Exception as e:
        print(f"❌ Gagal koneksi: {e}")
        socketio.emit("mqtt_error", {"error": str(e)})
        return

    try:
        while True:
            check_sensor_status()

            time.sleep(3600)  # Cek setiap 1 jam
    except KeyboardInterrupt:
        print("🛑 Menutup koneksi MQTT...")
        client.disconnect()
        client.loop_stop()

# 📤 Perintah manual
def kirim_perintah_siram(perintah):
    if client:
        client.publish("otomatis/siram/status", perintah)
        socketio.emit("status_siram", {"status": perintah})

def kirim_perintah_kabut(perintah):
    if client:
        client.publish("otomatis/kabut/status", perintah)
        socketio.emit("status_kabut", {"status": perintah})
        
