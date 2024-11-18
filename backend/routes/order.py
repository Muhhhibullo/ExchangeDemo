from flask import Blueprint, request, jsonify, make_response
from flask_cors import cross_origin
from models.order import Order
from models.trade import Trade
from database.db_config import db
from utils.matching_engine import OrderMatchingEngine
from sqlalchemy.exc import SQLAlchemyError

# Blueprint for order routes
order_bp = Blueprint('order', __name__)
engine = OrderMatchingEngine()

@order_bp.route('/place', methods=['POST', 'OPTIONS'])
@cross_origin(supports_credentials=True)
def place_order():
    if request.method == 'OPTIONS':
        # Handle preflight CORS request
        response = make_response()
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
        response.headers.add("Access-Control-Allow-Methods", "POST")
        return response, 200

    try:
        data = request.json
        user_id = data.get('user_id')
        order_type = data.get('type')  # 'buy' or 'sell'
        price = data.get('price')
        amount = data.get('amount')

        # Validate required fields
        if not all([user_id, order_type, price, amount]):
            return jsonify({"error": "Missing required fields"}), 400

        # Validate price and amount are positive numbers
        try:
            price = float(price)
            amount = float(amount)
            if price <= 0 or amount <= 0:
                return jsonify({"error": "Price and amount must be positive numbers"}), 400
        except ValueError:
            return jsonify({"error": "Price and amount must be valid numbers"}), 400

        # Create and save the order
        order = Order(user_id=user_id, type=order_type, price=price, amount=amount)
        db.session.add(order)
        db.session.commit()

        # Add order to the matching engine
        engine.add_order(order_type, price, amount)

        # Start transaction to place order and match
        try:
            db.session.begin()  # Begin a new transaction

            # Match orders
            trades = engine.match_orders()

            # Commit the transaction
            db.session.commit()

            # Convert trades to dicts for response
            trade_list = [trade.to_dict() for trade in trades]
            return jsonify({
                "message": "Order placed successfully",
                "order": order.to_dict(),
                "trades": trade_list
            }), 201
        except SQLAlchemyError as e:
            db.session.rollback()  # Rollback on error
            print(f"Error during transaction: {e}")
            return jsonify({"error": "Database transaction failed"}), 500

    except Exception as e:
        print(f"Error placing order: {e}")
        return jsonify({"error": "Failed to place order"}), 500

@order_bp.route('/book', methods=['GET'])
def get_order_book():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        # Paginate the orders
        orders = Order.query.paginate(page, per_page, False).items
        if not orders:
            return jsonify({"message": "No orders found"}), 200

        order_list = [order.to_dict() for order in orders]
        return jsonify(order_list), 200

    except Exception as e:
        print(f"Error fetching order book: {e}")
        return jsonify({"error": "Failed to fetch order book"}), 500

@order_bp.route('/trades/<user_id>', methods=['GET'])
def get_trade_history(user_id):
    try:
        trades = Trade.query.filter(
            (Trade.buyer_id == user_id) | (Trade.seller_id == user_id)
        ).all()

        if not trades:
            return jsonify({"message": "No trades found for this user"}), 200

        # Convert trades to dicts for response
        trade_list = [trade.to_dict() for trade in trades]
        return jsonify(trade_list), 200

    except Exception as e:
        print(f"Error fetching trades for user {user_id}: {e}")
        return jsonify({"error": "Failed to fetch trades"}), 500
