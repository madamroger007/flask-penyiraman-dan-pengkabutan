from flask import Blueprint, request, jsonify
from app.src.services.control_service import kontrol_penyiraman_service, kontrol_pengkabutan_service

control = Blueprint('control', __name__)

@control.route('/kontrol/penyiraman', methods=['POST'])
def kontrol_penyiraman():
    data = request.get_json()
    perintah = data.get("perintah")
    kontrol_penyiraman_service(perintah)
    return jsonify({"message": "Perintah penyiraman berhasil dikirim"}), 200

@control.route('/kontrol/pengkabutan', methods=['POST'])
def kontrol_pengkabutan():
    data = request.get_json()
    perintah = data.get("perintah")
    kontrol_pengkabutan_service(perintah)
    return jsonify({"message": "Perintah pengkabutan berhasil dikirim"}), 200
