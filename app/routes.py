import os
from flask import Blueprint, render_template, send_file, jsonify
from zipfile import ZipFile
from io import BytesIO
import json

main = Blueprint('main', __name__)

@main.route('/')
def index():
  return render_template('index.html')

@main.route('/api/files')
def files():
  return jsonify([{'name': 'new.txt', 'size': '10GB'}])

@main.route('/api/settings')
def settings():
  return jsonify(data)

@main.route('/api/upload')
def upload():
  return jsonify(data)