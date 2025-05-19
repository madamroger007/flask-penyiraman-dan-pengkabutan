from flask import Blueprint, render_template, redirect, request, url_for, session, flash, jsonify, current_app
import app.config as config
from app.src.utils import cards,table_rows   
from app.src.routes.validation.login import login_required
from app.src.services.data_sensor_service import get_all_data_sensors_service
from app.src.services.control_service import get_jadwal_penyiraman_service
from app.src.repositories.jadwal_penyiraman_repositories import get_jadwal_penyiraman_by_jenis_repository
main = Blueprint('main', __name__)
@main.route('/')
@login_required
def index():
    data_sensor = get_all_data_sensors_service()
    return render_template('pages/index.html', cards=cards, table_rows=data_sensor)

@main.route('/data-sensor', methods=['GET'])
@login_required
def data_sensor():
    data_sensor = get_all_data_sensors_service()
    return render_template('pages/data-sensor/data_sensor.html',table_rows=data_sensor)

@main.route('/kontrol-alat', methods=['GET'])
@login_required
def control():
    # Mengambil data jadwal penyiraman dari service
    penyiraman = get_jadwal_penyiraman_by_jenis_repository(jenis_aksi='penyiraman')
    pengkabutan = get_jadwal_penyiraman_by_jenis_repository(jenis_aksi='pengkabutan')
    if penyiraman is None or pengkabutan is None:
        flash("Jadwal penyiraman atau pengkabutan tidak ditemukan.", "danger")
        return redirect(url_for('main.index'))
    table_rows = get_jadwal_penyiraman_service()
    return render_template('pages/kontrol-alat/kontrol.html',
                           table_rows=table_rows,
                           penyiraman_id=penyiraman.id,
                           waktu_1_penyiraman=penyiraman.waktu_1.strftime("%H:%M"),
                           waktu_2_penyiraman=penyiraman.waktu_2.strftime("%H:%M"),
                           pengkabutan_id=pengkabutan.id,
                           waktu_1_pengkabutan=pengkabutan.waktu_1.strftime("%H:%M"),
                           waktu_2_pengkabutan=pengkabutan.waktu_2.strftime("%H:%M"))

@main.route('/whatsapp', methods=['GET'])
@login_required
def whatsapp():
    return render_template('pages/notification/whatapps.html')