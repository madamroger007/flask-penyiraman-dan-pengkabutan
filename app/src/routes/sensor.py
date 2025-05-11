from flask import Blueprint, render_template, redirect, request, url_for, session, flash, jsonify, current_app
import app.config as config



sensor = Blueprint('sensor', __name__)
