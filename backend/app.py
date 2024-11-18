# app.py
from flask import Flask, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from routes.user import user_bp
from routes.wallet import wallet_bp
from routes.order import order_bp
from database.db_config import db, init_db  # Make sure you import db here
import secrets

# Initialize Flask app
app = Flask(__name__)

# Configure CORS
CORS(app, resources={r"/*": {"origins": "*"}})

# Configure SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

# Configure JWT
app.config['JWT_SECRET_KEY'] = secrets.token_hex(32)
jwt = JWTManager(app)

# Initialize Database
init_db(app)

# Initialize Migrate
migrate = Migrate(app, db)

# Register Blueprints
app.register_blueprint(user_bp, url_prefix="/api/user")
app.register_blueprint(wallet_bp, url_prefix="/api/wallet")
app.register_blueprint(order_bp, url_prefix="/api/order")

@app.route('/')
def home():
    return jsonify({"message": "Crypto Exchange API is live!"})

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Creates the database tables if they don't exist

    socketio.run(app, debug=True)
