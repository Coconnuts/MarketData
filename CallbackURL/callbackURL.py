from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/receive', methods=['GET'])
def receive():
    code = request.args.get('code')
    state = request.args.get('state')

    if code:
        print(f"Authorization code received: {code}")
        return f"""
            <h2>Authorization Code Received</h2>
            <p><strong>Code:</strong> {code}</p>
            <p><strong>State:</strong> {state}</p>
            <p>You can now close this tab and paste the code into your app.</p>
        """, 200
    else:
        print("No code in request:", request.args)
        return "No authorization code received. Please try again.", 400

if __name__ == '__main__':
    cert_path = os.path.join(os.path.dirname(__file__), 'cert.pem')
    key_path = os.path.join(os.path.dirname(__file__), 'key.pem')
    app.run(host='127.0.0.1', port=8443, ssl_context=(cert_path, key_path))