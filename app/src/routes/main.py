from flask import Blueprint, render_template, redirect, request, url_for, session, flash, jsonify, current_app
import app.config as config
from app.src.utils import cards,table_rows   
from app.src.routes.validation.login import login_required

main = Blueprint('main', __name__)
@main.route('/')
@login_required
def index():
    return render_template('pages/index.html', cards=cards, table_rows=table_rows)

@main.route('/data-sensor', methods=['GET'])
@login_required
def data_sensor():
    return render_template('pages/data-sensor/data_sensor.html',table_rows=table_rows)

@main.route('/kontrol-alat', methods=['GET'])
@login_required
def control():
    return render_template('pages/kontrol-alat/kontrol.html',table_rows=table_rows)

@main.route('/whatsapp', methods=['GET'])
@login_required
def whatsapp():
    return render_template('pages/notification/whatapps.html')