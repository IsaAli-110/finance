from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from datetime import datetime
import json, os

app = Flask(__name__)
app.secret_key = 'rahasia'

# File data
DATA_FILE = 'data/keuangan.json'

# Jika file belum ada, buat kosong
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump([], f)

# ================= ROUTE UTAMA =================

@app.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/transaksi')
def data_transaksi():
    return render_template('transaksi.html')

@app.route('/laporan')
def laporan():
    print("Route /laporan dipanggil")
    with open(DATA_FILE, 'r') as f:
        daftar_transaksi = json.load(f)
    return render_template('laporan.html', daftar_transaksi=daftar_transaksi)

# ================= API ROUTES =================
# GET semua data transaksi
@app.route('/api/laporan', methods=['GET'])
def api_laporan_get():
    try:
        with open(DATA_FILE, 'r') as f:
            daftar_transaksi = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        daftar_transaksi = []

    return jsonify(daftar_transaksi)

# POST tambah transaksi baru
@app.route('/api/laporan', methods=['POST'])
def api_laporan_post():
    req = request.get_json()
    data_baru = {
        "tanggal": datetime.now().strftime('%Y-%m-%d'),
        "keterangan": req['keterangan'],
        "jumlah": int(req['jumlah']),
        "tipe": req['tipe']
    }

    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    data.append(data_baru)
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

    return jsonify({"status": "sukses"})


# ============== api data transaksi ============

@app.route('/simpan', methods=['POST'])
def simpan_transaksi():
    data_baru = {
        "tanggal": request.form['tanggal'],
        "keterangan": request.form['keterangan'],
        "jumlah": int(request.form['jumlah']),
        "tipe": request.form['tipe']
    }

    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    data.append(data_baru)

    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

    return redirect(url_for('laporan'))

# ============== api tambah transaksi ============

# @app.route('/simpan', methods=['POST'])
# def simpan_transaksi():
#     data_baru = {
#         "tanggal": datetime.now().strftime('%Y-%m-%d'),
#         "keterangan": request.form['keterangan'],
#         "jumlah": int(request.form['jumlah']),
#         "tipe": request.form['tipe']
#     }

#     try:
#         with open(DATA_FILE, 'r') as f:
#             data = json.load(f)
#     except (FileNotFoundError, json.JSONDecodeError):
#         data = []

#     data.append(data_baru)

#     with open(DATA_FILE, 'w') as f:
#         json.dump(data, f, indent=4)

#     return redirect(url_for('laporan'))



# ================= LOGIN LOGOUT =================

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

# ================= RUN APP =================

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
