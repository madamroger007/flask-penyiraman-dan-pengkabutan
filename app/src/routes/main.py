from flask import Blueprint, render_template, redirect, request, url_for, session, flash, jsonify, current_app
import app.config as config
from app.src.utils import cards,table_rows   


main = Blueprint('main', __name__)
@main.route('/')
def dashboard():
  

    return render_template('pages/index.html', cards=cards, table_rows=table_rows)