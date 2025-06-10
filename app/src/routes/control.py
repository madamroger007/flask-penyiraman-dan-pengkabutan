from flask import Blueprint, request, jsonify
from app.src.services.control_service import kontrol_penyiraman_service, kontrol_pengkabutan_service
from app.src.services.penjadwalan_service import update_jadwal_service
from app import socketio
from flask_socketio import emit
from app.src.services.penjadwalan_service import refresh_jadwal_service
from app.src.routes.validation.login import login_required
from app.src.repositories.riwayat_aksi_repositories import delete_riwayat_aksi_repository

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

@control.route('/kontrol/waktu/jadwal-penyiraman/<int:id>', methods=['POST'])
def edit_jadwal_penyiraman(id=None):
    data = request.get_json()
    waktu_1 = data.get("waktu_penyiraman_1")
    waktu_2 = data.get("waktu_penyiraman_2")
    print("id", id)
    result = update_jadwal_service(id, waktu_1, waktu_2, jenis='penyiraman')
    
    if result["success"]:
        # setelah simpan waktu baru:
        refresh_jadwal_service("penyiraman")
        # setelah simpan waktu baru:
        socketio.emit("jadwal_updated", {"jenis": "penyiraman", "jadwal": result["jadwal"]})
        return jsonify({"message": "Jadwal penyiraman berhasil diperbarui"}), 200
    return jsonify({"message": "Gagal memperbarui jadwal"}), 400

@control.route('/kontrol/waktu/jadwal-pengkabutan/<int:id>', methods=['POST'])
def edit_jadwal_pengkabutan(id=None):
    data = request.get_json()
    waktu_1 = data.get("waktu_pengkabutan_1")
    waktu_2 = data.get("waktu_pengkabutan_2")

    result = update_jadwal_service(id, waktu_1, waktu_2, jenis='pengkabutan')

    if result["success"]:
        refresh_jadwal_service("pengkabutan")
        # setelah simpan waktu baru:
        socketio.emit("jadwal_updated", {"jenis": "pengkabutan", "jadwal": result["jadwal"]})
        return jsonify({"message": "Jadwal pengkabutan berhasil diperbarui"}), 200
    return jsonify({"message": "Gagal memperbarui jadwal"}), 400


@control.route('/riwayat/delete', methods=['POST'])
@login_required
def riwayat_delete():
    ids = request.json.get('ids', [])
    deleted_count = 0

    for riwayat_id in ids:
        if delete_riwayat_aksi_repository(riwayat_id):
            deleted_count += 1

    return jsonify({'success': True, 'deleted': deleted_count})
