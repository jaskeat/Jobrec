from flask import Flask, url_for, render_template, request, redirect, flash, send_from_directory
import pandas as pd
import json
from hashlib import sha256

app = Flask(__name__, static_folder='static')
#app.secret_key = "9773e89f69e69285cf11c10cbc44a37945f6abbc5d78d5e20c2b1b0f12d75ab7"

@app.route('/')
def index():
    return render_template('base.html')

# Add this route to help debug static files
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)