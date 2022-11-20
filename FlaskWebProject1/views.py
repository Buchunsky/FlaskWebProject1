from datetime import datetime
from flask import render_template, Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/servers')
def servers():
    return render_template(
        'servers.html',
        title='Servers',
        year=datetime.now().year,
        message='Your application description page.'
    )

app.run(port=5000)