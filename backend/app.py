from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from routes.auth import auth_bp
from routes.device import device_bp
from routes.activation import activation_bp
from routes.evidence import evidence_bp
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(device_bp, url_prefix='/device')
app.register_blueprint(activation_bp, url_prefix='/agent')
app.register_blueprint(evidence_bp, url_prefix='/evidence')

@app.route('/')
def home():
    return {"message": "Phantom Guard Backend is running!"}

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)