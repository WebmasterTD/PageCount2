from flask import render_template
from app import app

import time
@app.route('/')
@app.route('/index')
def index():
    table = [
        {'name': 'čierno-bielo A4'},
        {'name': 'čierno-bielo A3'},
        {'name': 'farebne A4'},
        {'name': 'farebne A3'},
        {'name': 'scan'},
        {'name': 'obojstranne A4'},
        {'name': 'obojstranne A3'}
    ]
    return render_template('index.html', title='Counter', table = table)
