from flask import Blueprint, render_template, redirect, request, url_for, session, flash, jsonify, current_app
from flask import request
import app.config as config
from app.src.routes.validation.login import login_required
from app.src.repositories.data_sensor_repositories import (
    delete_data_sensor_repository
)



sensor = Blueprint('sensor', __name__)
@sensor.route('/sensor/delete', methods=['POST'])
@login_required
def sensor_delete():
    ids = request.json.get('ids', [])  # Ganti ini
    deleted_count = 0

    for data_sensor_id in ids:
        if delete_data_sensor_repository(data_sensor_id):
            deleted_count += 1

    return jsonify({'success': True, 'deleted': deleted_count})


