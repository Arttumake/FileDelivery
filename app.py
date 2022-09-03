from asyncio import subprocess
from urllib import response
from wsgiref.util import request_uri
from flask import Flask
from flask import url_for, request, render_template, flash, send_file, redirect

import subprocess
import os, glob
from pathlib import Path

p = Path(Path.cwd(), 'Raportit')

XRF_FOLDER = 'xrf_thermo'
ALLOWED_EXTENSIONS = {'csv', 'xlsx'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = XRF_FOLDER
app.config['DOWNLOAD_FOLDER'] = p
app.secret_key = b"\x92\xcb=\x0bT/,\xff\x8d\xd4'|\xa7/IY"


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
@app.route('/upload')
def home():
    return render_template('upload.html')

@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        filename = file.filename
        if file and allowed_file(file.filename):
            filename = file.filename
            if 'xlsx' in file.filename:
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            elif 'csv' in file.filename:
                to_be_deleted = list(p.glob('*.xlsx'))
                for f in to_be_deleted:
                    os.remove(f)
                file.save(filename)
                subprocess.call(['python', 'xrf.py'], cwd=app.config['UPLOAD_FOLDER'])
                excels = list(p.glob('*.xlsx'))
                latest = max(excels, key=os.path.getctime)
                return send_file(latest)
        else:
            flash("Choose csv type file to upload", category="error")
            return redirect('upload')
    else:
        return redirect('upload')

    