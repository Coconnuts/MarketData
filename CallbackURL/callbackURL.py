from flask import Flask, request

app = Flask(__name__)

@app.route('/receive', methods=['GET'])
def receive():
    print("Query params:", request.args)
    return "GET received!", 200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8443, ssl_context=('cert.pem', 'key.pem'))