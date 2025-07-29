from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello over HTTPS"

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8443, ssl_context=('cert.pem', 'key.pem'))