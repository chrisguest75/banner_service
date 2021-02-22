import os
from app import app
from flask import render_template, send_from_directory


@app.route("/")
def home():
    return render_template("banner.html")

# https://flask.palletsprojects.com/en/1.1.x/patterns/favicon/
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/png')
