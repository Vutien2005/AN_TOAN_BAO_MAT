# Flask app nhận file bảo mật
from flask import Flask, request, render_template, redirect, url_for, flash
import os
import json
from crypto_utils import load_rsa_private_key, load_rsa_public_key, rsa_decrypt, rsa_verify, des_decrypt, sha512_hash, b64decode

UPLOAD_FOLDER = 'uploads'
PRIVATE_KEY_FILE = 'receiver_private.pem'
SENDER_PUBLIC_KEY_FILE = 'sender_public.pem'

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET'])
def index():
    return render_template('receiver.html')

@app.route('/upload', methods=['POST'])
def upload():
    try:
        meta_json = request.form['meta']
        meta_obj = json.loads(meta_json)
        meta_sig = b64decode(meta_obj['sig'])
        meta_data = (meta_obj['filename'] + str(meta_obj['timestamp']) + str(meta_obj['parts'])).encode()
        sender_pub = load_rsa_public_key(open(SENDER_PUBLIC_KEY_FILE, 'rb').read())
        if not rsa_verify(sender_pub, meta_data, meta_sig):
            flash('Chữ ký metadata không hợp lệ!', 'danger')
            return redirect(url_for('index'))
        enc_key = b64decode(request.form['enc_key'])
        priv = load_rsa_private_key(open(PRIVATE_KEY_FILE, 'rb').read())
        session_key = rsa_decrypt(priv, enc_key)
        parts = []
        for i in range(meta_obj['parts']):
            part_json = json.loads(request.form[f'part_{i}'])
            iv = b64decode(part_json['iv'])
            cipher = b64decode(part_json['cipher'])
            hash_recv = part_json['hash']
            sig = b64decode(part_json['sig'])
            hash_calc = sha512_hash(iv + cipher)
            if hash_calc != hash_recv:
                flash(f'Hash không khớp ở phần {i+1}', 'danger')
                return redirect(url_for('index'))
            if not rsa_verify(sender_pub, (iv + cipher), sig):
                flash(f'Chữ ký không hợp lệ ở phần {i+1}', 'danger')
                return redirect(url_for('index'))
            plain = des_decrypt(session_key, iv, cipher)
            parts.append(plain)
        out_path = os.path.join(app.config['UPLOAD_FOLDER'], meta_obj['filename'])
        with open(out_path, 'wb') as f:
            for p in parts:
                f.write(p)
        flash(f'Đã nhận và lưu file: {out_path}', 'success')
    except Exception as e:
        flash(f'Lỗi: {e}', 'danger')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
