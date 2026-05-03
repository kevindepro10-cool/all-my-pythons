from flask import Flask, request, render_template, jsonify
import base64
import qrcode
import random
import string
import hashlib
import json
import urllib.parse

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/base64-encode', methods=['POST'])
def base64_encode():
    data = request.json.get('data', '')
    encoded = base64.b64encode(data.encode()).decode()
    return jsonify({'result': encoded})

@app.route('/api/base64-decode', methods=['POST'])
def base64_decode():
    data = request.json.get('data', '')
    try:
        decoded = base64.b64decode(data.encode()).decode()
        return jsonify({'result': decoded})
    except:
        return jsonify({'error': 'Invalid Base64'})

@app.route('/api/password-generator', methods=['POST'])
def password_generator():
    length = request.json.get('length', 12)
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return jsonify({'result': password})

@app.route('/api/hash-generator', methods=['POST'])
def hash_generator():
    data = request.json.get('data', '')
    algorithm = request.json.get('algorithm', 'sha256')
    
    if algorithm == 'md5':
        hashed = hashlib.md5(data.encode()).hexdigest()
    elif algorithm == 'sha1':
        hashed = hashlib.sha1(data.encode()).hexdigest()
    else:
        hashed = hashlib.sha256(data.encode()).hexdigest()
    
    return jsonify({'result': hashed})

@app.route('/api/json-formatter', methods=['POST'])
def json_formatter():
    data = request.json.get('data', '')
    try:
        formatted = json.dumps(json.loads(data), indent=2)
        return jsonify({'result': formatted})
    except:
        return jsonify({'error': 'Invalid JSON'})

@app.route('/api/url-encode', methods=['POST'])
def url_encode():
    data = request.json.get('data', '')
    encoded = urllib.parse.quote(data)
    return jsonify({'result': encoded})

@app.route('/api/url-decode', methods=['POST'])
def url_decode():
    data = request.json.get('data', '')
    decoded = urllib.parse.unquote(data)
    return jsonify({'result': decoded})

@app.route('/api/text-to-hex', methods=['POST'])
def text_to_hex():
    data = request.json.get('data', '')
    hex_value = data.encode().hex()
    return jsonify({'result': hex_value})

@app.route('/api/hex-to-text', methods=['POST'])
def hex_to_text():
    data = request.json.get('data', '')
    try:
        text = bytes.fromhex(data).decode()
        return jsonify({'result': text})
    except:
        return jsonify({'error': 'Invalid Hex'})

@app.route('/api/character-counter', methods=['POST'])
def character_counter():
    data = request.json.get('data', '')
    return jsonify({
        'characters': len(data),
        'words': len(data.split()),
        'bytes': len(data.encode())
    })

@app.route('/api/text-reversal', methods=['POST'])
def text_reversal():
    data = request.json.get('data', '')
    reversed_text = data[::-1]
    return jsonify({'result': reversed_text})

if __name__ == '__main__':
    app.run(debug=True)