from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from datetime import datetime
import json, os

app = Flask(__name__)
app.secret_key = 'rahasia'
DATA_FILE = 'data/keuangan.json'

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump([], f)



@app.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/data')
def api_data():
    
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    response = {
        "status_code": 200,
        "message": "Data Retrieved",
        "data": data
    }
    return jsonify(response)

@app.route('/api/tambah', methods=['POST'])
def tambah_data():
    req = request.get_json()
    data_baru = {
        "tanggal": datetime.now().strftime('%Y-%m-%d'),
        "keterangan": req['keterangan'],
        "jumlah": int(req['jumlah']),
        "tipe": req['tipe']
    }
    data = []
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        pass

    data.append(data_baru)
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

    return jsonify({"status": "sukses"})

# ========== Login =================

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == '123':
            session['user'] = username
            return redirect(url_for('index'))
        else:
            return "Login gagal"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

# ========== INI HARUS DI PALING BAWAH ==========

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

