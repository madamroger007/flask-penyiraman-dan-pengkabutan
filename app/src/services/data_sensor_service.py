from app import socketio
import requests
from dotenv import load_dotenv
import os

# Define the FLASK_URL variable
FLASK_URL = "http://localhost:5000"  # Replace with your actual Flask server URL

def handle_siram_status(client, userdata, msg):
    status = msg.payload.decode('utf-8').strip()
    print(f"🚿 Status penyiraman diterima: {status}")

    # Kirim ke browser (misalnya sebagai event sensor_update)
    socketio.emit('sensor_update', {
        'Kelembapan Tanah': int(status),  # Sesuaikan label
    })

    try:
        # Load environment variables from .env file
        load_dotenv()

        # Get FLASK_URL from environment variables
        flask_url = os.getenv("FLASK_URL")

        if not flask_url:
            raise ValueError("FLASK_URL is not set in the environment variables")

        requests.post(f"{flask_url}/otomatis/siram", json={"status": status})
    except Exception as e:
        print("Gagal kirim ke server:", e)
