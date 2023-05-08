from flask import Flask, jsonify, request, send_file, render_template, redirect, url_for
import uuid
import time
import qrcode
from io import BytesIO

app = Flask(__name__)

valid_uuids = {}
valid_keys = ['rois405']
MAX_TIME = 10   # seconds

@app.route('/', methods=['GET'])
def index():
    key = request.cookies.get('key')
    if not key:
        return render_template('login.html')
    if key not in valid_keys:
        return render_template('error.html', message='Invalid Key')
    key = request.cookies.get('key')
    
    uuid = request.cookies.get('uuid')
    if not uuid or len(valid_uuids) == 0:
        return redirect(url_for('get_uuid'))

    uuid_param = request.cookies.get('uuid')
    if uuid_param in valid_uuids:
        seconds_left = int(MAX_TIME - (time.time() - valid_uuids[uuid_param]))
    else:
        seconds_left = None
    return render_template('index.html', uuid=uuid_param, seconds_left=seconds_left)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        key = request.form['key']
        if key not in valid_keys:
            return render_template('login.html', message='Invalid Key')
    resp = redirect(url_for('index'))
    resp.set_cookie("key", key)
    return resp

@app.route('/get_uuid', methods=['GET'])
def get_uuid():
    key = request.cookies.get('key')
    if key not in valid_keys:
        return render_template('error.html', message='Invalid Key')
    new_uuid = str(uuid.uuid4())
    valid_uuids[new_uuid] = time.time()
    resp = redirect(url_for('index'))
    resp.set_cookie("uuid", new_uuid)
    return resp

@app.route('/check_uuid', methods=['POST'])
def check_uuid():
    req_data = request.get_json()
    uuid_to_check = req_data['uuid']
    if uuid_to_check in valid_uuids and (time.time() - valid_uuids[uuid_to_check]) < MAX_TIME:
        del valid_uuids[uuid_to_check]
        return jsonify({'result': 'success'})
    else:
        return jsonify({'result': 'failure'})
    
@app.route('/get_qrcode', methods=['GET'])
def get_qrcode():
    uuid_param = request.args.get('uuid')
    img = qrcode.make(uuid_param)
    img_buffer = BytesIO()
    img.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    return send_file(img_buffer, mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

