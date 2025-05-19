import paho.mqtt.client as paho
from paho import mqtt
import os
import time
import requests
import ssl
import certifi
from dotenv import load_dotenv
from app import socketio  # 🔥 Tambahkan ini agar bisa emit dari sini

load_dotenv()

# 🔧 Konfigurasi MQTT & Flask API
BROKER = os.environ.get('MQTT_BROKER', '')
PORT = 8883
USERNAME = os.environ.get('MQTT_USERNAME')
PASSWORD = os.environ.get('MQTT_PASSWORD')
FLASK_URL = os.environ.get('FLASK_URL')

TOPICS = [
    ("otomatis/siram/status", 1),
    ("otomatis/kabut/status", 1),
    ("sensor/kelembapan_tanah", 1),
    ("sensor/suhu_udara", 1),
    ("sensor/kelembapan_udara", 1)
]

latest_sensor_data = {
    "Suhu Udara": None,
    "Kelembapan Udara": None,
    "Kelembapan Tanah": None
}

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

# 📥 Callback status penyiraman
def handle_siram_status(client, userdata, msg):
    status = msg.payload.decode('utf-8').strip()
    print(f"🚿 Status penyiraman diterima: {status}")

    # Emit ke WebSocket
    socketio.emit("status_siram", {"status": status})
    print("🔄 Emit WebSocket: status_siram")

    # Kirim ke Flask endpoint
    try:
        response = requests.post(f"{FLASK_URL}/otomatis/siram", json={"status": status})
        print("📤 Kirim status siram ke server:", response.status_code)
    except Exception as e:
        print(f"❌ Gagal kirim ke server: {e}")

# 📥 Callback status pengkabutan
def handle_kabut_status(client, userdata, msg):
    status = msg.payload.decode('utf-8').strip()
    print(f"💨 Status pengkabutan diterima: {status}")

    # Emit ke WebSocket
    socketio.emit("status_kabut", {"status": status})
    print("🔄 Emit WebSocket: status_kabut")

    # Kirim ke Flask endpoint
    try:
        response = requests.post(f"{FLASK_URL}/otomatis/kabut", json={"status": status})
        print("📤 Kirim status kabut ke server:", response.status_code)
    except Exception as e:
        print(f"❌ Gagal kirim ke server: {e}")

# 📥 Callback data sensor
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
            latest_sensor_data[label] = float(value)
        except ValueError:
            print(f"❌ Nilai sensor tidak valid: {value}")
            return

        # Emit data via WebSocket
        socketio.emit("sensor_update", {
            label: latest_sensor_data[label]
        })


# 🚀 Mulai koneksi MQTT
def run_mqtt_service():
    global client
    print(f"🔌 Menghubungkan ke MQTT {BROKER}:{PORT}")
    
    client = paho.Client(client_id="otomatisasi_penyiram", protocol=paho.MQTTv5)
    client.username_pw_set(USERNAME, PASSWORD)
    client.tls_set(ca_certs=certifi.where(), tls_version=ssl.PROTOCOL_TLS_CLIENT)
    
    client.on_connect = on_connect
    client.message_callback_add("otomatis/siram/status", handle_siram_status)
    client.message_callback_add("otomatis/kabut/status", handle_kabut_status)
    client.message_callback_add("sensor/kelembapan_tanah", handle_sensor_data)
    client.message_callback_add("sensor/suhu_udara", handle_sensor_data)
    client.message_callback_add("sensor/kelembapan_udara", handle_sensor_data)


    try:
        client.connect(BROKER, PORT)
        client.loop_start()
    except Exception as e:
        print(f"❌ Gagal konek ke broker: {e}")
        return

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("🛑 Menutup koneksi MQTT...")
        client.disconnect()
        client.loop_stop()

# 📤 Perintah manual (jika perlu)
def kirim_perintah_siram(perintah):
    if client:
        client.publish("otomatis/siram/status", perintah)
        socketio.emit("status_siram", {"status": perintah})
        print(f"📤 Perintah penyiraman dikirim: {perintah}")

def kirim_perintah_kabut(perintah):
    if client:
        client.publish("otomatis/kabut/status", perintah)
        socketio.emit("status_kabut", {"status": perintah})
        print(f"📤 Perintah pengkabutan dikirim: {perintah}")

