# Flask app gửi file bảo mật
from flask import Flask, render_template, request, redirect, url_for, flash
import requests
import os
import json
import time
from crypto_utils import load_rsa_private_key, load_rsa_public_key, rsa_encrypt, rsa_sign, des_encrypt, generate_des_key, generate_iv, sha512_hash, b64encode

PRIVATE_KEY_FILE = 'sender_private.pem'
RECEIVER_PUBLIC_KEY_FILE = 'receiver_public.pem'

app = Flask(__name__)
app.secret_key = 'supersecretkey'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        receiver_url = request.form['receiver_url']
        if not file or not receiver_url:
            flash('Vui lòng chọn file và nhập địa chỉ receiver!', 'danger')
            return redirect(url_for('index'))
        data = file.read()
        part_size = len(data) // 3
        parts = [data[i*part_size:(i+1)*part_size] for i in range(2)]
        parts.append(data[2*part_size:])
        session_key = generate_des_key()
        priv = load_rsa_private_key(open(PRIVATE_KEY_FILE, 'rb').read())
        recv_pub = load_rsa_public_key(open(RECEIVER_PUBLIC_KEY_FILE, 'rb').read())
        meta = {
            'filename': file.filename,
            'timestamp': int(time.time()),
            'parts': 3
        }
        meta_data = (meta['filename'] + str(meta['timestamp']) + str(meta['parts'])).encode()
        meta['sig'] = b64encode(rsa_sign(priv, meta_data))
        enc_key = rsa_encrypt(recv_pub, session_key)
        form_data = {
            'meta': json.dumps(meta),
            'enc_key': b64encode(enc_key)
        }
        for i, part in enumerate(parts):
            iv = generate_iv()
            cipher = des_encrypt(session_key, iv, part)
            hash_val = sha512_hash(iv + cipher)
            sig = rsa_sign(priv, iv + cipher)
            part_obj = {
                'iv': b64encode(iv),
                'cipher': b64encode(cipher),
                'hash': hash_val,
                'sig': b64encode(sig)
            }
            form_data[f'part_{i}'] = json.dumps(part_obj)
        try:
            resp = requests.post(receiver_url + '/upload', data=form_data)
            if resp.status_code == 200:
                flash('Gửi file thành công!', 'success')
            else:
                flash('Gửi file thất bại!', 'danger')
        except Exception as e:
            flash(f'Lỗi: {e}', 'danger')
        return redirect(url_for('index'))
    return render_template('sender.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=True)
