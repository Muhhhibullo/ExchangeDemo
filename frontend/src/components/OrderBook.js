import React, { useEffect, useState } from "react";
import axios from "axios";

const OrderBook = () => {
  const [orders, setOrders] = useState([]);
  const [error, setError] = useState(null);  // To store any error message

  useEffect(() => {
    const fetchOrders = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:5000/api/order/book");
        setOrders(response.data);
      } catch (error) {
        setError("Failed to fetch orders");
        console.error("Error fetching orders:", error);
      }
    };
    fetchOrders();
  }, []);

  return (
    <div>
      <h2>Order Book</h2>
      {error && <div style={{ color: "red" }}>{error}</div>}  {/* Display error message */}
      <table>
        <thead>
          <tr>
            <th>Type</th>
            <th>Price</th>
            <th>Amount</th>
          </tr>
        </thead>
        <tbody>
            {orders.length > 0 ? (
                orders.map((order) => (
                <tr key={order.id}>
                    <td>{order.type}</td>
                    <td>{order.price}</td>
                    <td>{order.amount}</td>
                </tr>
                ))
            ) : (
                <tr>
                <td colSpan="3">No orders available</td>
                </tr>
            )}
            </tbody>
      </table>
    </div>
  );
};

export default OrderBook;
