from flask import Blueprint, jsonify, request
from models.wallet import Wallet
from models.user import User
from database.db_config import db

# Define Blueprint
wallet_bp = Blueprint('wallet', __name__)

# Route to get the current balance
@wallet_bp.route('/balance', methods=['GET'])
def get_balance():
    try:
        user_id = request.args.get("user_id", type=int, default=1)
        print("Fetching balance for user_id:", user_id)

        # Find the wallet based on user_id
        wallet = Wallet.query.filter_by(user_id=user_id).first()

        if not wallet:
            return jsonify({"error": "Wallet not found for this user."}), 404

        return jsonify({"balance": f"{wallet.balance} USD"}), 200
    except Exception as e:
        print(f"Error getting balance: {e}")
        return jsonify({"error": "Failed to get balance."}), 500

# Route to deposit funds
@wallet_bp.route('/deposit', methods=['POST'])
def deposit():
    try:
        data = request.json
        print("Deposit request received:", data)
        if not data:
            return jsonify({"error": "Invalid request format. JSON expected."}), 400

        user_id = data.get("user_id", 1)
        amount = float(data.get("amount"))

        # Validate input
        if amount is None or not isinstance(amount, (int, float)) or amount <= 0:
            return jsonify({"error": "Invalid deposit amount."}), 400

        # Find the wallet based on user_id
        wallet = Wallet.query.filter_by(user_id=user_id).first()
        
        if not wallet:
            return jsonify({"error": "Wallet not found for this user."}), 404

        wallet.deposit(amount)
        db.session.commit()

        return jsonify({
            "message": "Deposit successful!",
            "balance": f"{wallet.balance} USD"
        }), 200
    except Exception as e:
        print(f"Error during deposit: {e}")
        return jsonify({"error": f"Failed to deposit funds. {e}"}), 500

# Route to withdraw funds
@wallet_bp.route('/withdraw', methods=['POST'])
def withdraw():
    try:
        data = request.json
        print("Withdrawal request received:", data)

        if not data:
            return jsonify({"error": "Invalid request format. JSON expected."}), 400

        user_id = data.get("user_id", 1)
        amount = float(data.get("amount"))

        # Validate input
        if amount is None or not isinstance(amount, (int, float)) or amount <= 0:
            return jsonify({"error": "Invalid withdrawal amount."}), 400

        # Find the wallet based on user_id
        wallet = Wallet.query.filter_by(user_id=user_id).first()

        if not wallet:
            return jsonify({"error": "Wallet not found for this user."}), 404

        # Check if sufficient funds are available
        if wallet.balance < amount:
            return jsonify({"error": "Insufficient funds."}), 400

        wallet.withdraw(amount)
        db.session.commit()

        return jsonify({
            "message": "Withdrawal successful!",
            "balance": f"{wallet.balance} USD"
        }), 200
    except Exception as e:
        print(f"Error during withdrawal: {e}")
        return jsonify({"error": f"Failed to withdraw funds. {e}"}), 500
