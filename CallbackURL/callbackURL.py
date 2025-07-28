from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/receive', methods=['GET'])
def receive():
    print("Query params:", request.args)
    return "GET received!", 200

if __name__ == '__main__':
    cert_path = os.path.join(os.path.dirname(__file__), 'cert.pem')
    key_path = os.path.join(os.path.dirname(__file__), 'key.pem')
    app.run(host='127.0.0.1', port=8443, ssl_context=(cert_path, key_path))