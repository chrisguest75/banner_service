import os
from app import app
from flask import render_template, send_from_directory
import logging

@app.route('/')
def root():
    return render_template("banner.html")

@app.route('/index.html')
def home():
    return render_template("banner.html")

# https://flask.palletsprojects.com/en/1.1.x/patterns/favicon/
@app.route('/favicon.ico')
def favicon():
    # logger = logging.getLogger()
    # logger.info(f"Values", extra={"app.root_path": app.root_path})    
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/png')
