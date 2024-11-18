from database.db_config import db
from models.order import Order
from models.trade import Trade
from flask_socketio import emit


class OrderMatchingEngine:
    def __init__(self):
        self.buy_orders = []  # Sorted list of buy orders (max-heap style)
        self.sell_orders = []  # Sorted list of sell orders (min-heap style)

    def add_order(self, order_type, price, amount, user_id):
        order = {
            "price": price,
            "amount": amount,
            "user_id": user_id
        }

        if order_type == "buy":
            self.buy_orders.append(order)
            self.buy_orders.sort(key=lambda x: x["price"], reverse=True)  # Sort by price (descending)
        elif order_type == "sell":
            self.sell_orders.append(order)
            self.sell_orders.sort(key=lambda x: x["price"])  # Sort by price (ascending)

    def match_orders(self):
        trades = []

        # Continue matching orders while there are both buy and sell orders available
        while self.buy_orders and self.sell_orders:
            buy_order = self.buy_orders[0]
            sell_order = self.sell_orders[0]

            # Check if the buy order price is greater than or equal to the sell order price
            if buy_order["price"] >= sell_order["price"]:
                # Trade occurs
                trade_price = sell_order["price"]
                trade_amount = min(buy_order["amount"], sell_order["amount"])

                # Record the trade (buyer_id, seller_id, price, and amount)
                trade = Trade(
                    buyer_id=buy_order["user_id"],
                    seller_id=sell_order["user_id"],
                    price=trade_price,
                    amount=trade_amount
                )
                db.session.add(trade)

                # Update remaining amounts of the buy and sell orders
                buy_order["amount"] -= trade_amount
                sell_order["amount"] -= trade_amount

                # Remove fully filled orders
                if buy_order["amount"] == 0:
                    self.buy_orders.pop(0)
                if sell_order["amount"] == 0:
                    self.sell_orders.pop(0)

                # Store the trade details in the response list
                trades.append({
                    "buyer_id": buy_order["user_id"],
                    "seller_id": sell_order["user_id"],
                    "price": trade_price,
                    "amount": trade_amount
                })
            else:
                break  # No more matching trades possible

        # Emit the updated order book to connected clients via WebSocket (optional feature)
        emit('update_order_book', {
            "buy_orders": self.buy_orders,
            "sell_orders": self.sell_orders
        }, broadcast=True)

        # Commit trade data to the database
        db.session.commit()

        return trades

    @staticmethod
    def save_trade(buyer_id, seller_id, price, amount):
        # Save a single trade to the database (used for manual trades or other operations)
        trade = Trade(buyer_id=buyer_id, seller_id=seller_id, price=price, amount=amount)
        db.session.add(trade)
        db.session.commit()
