import React, { useState } from "react";
import axios from "axios";

const OrderForm = () => {
  const [type, setType] = useState("buy");
  const [price, setPrice] = useState("");
  const [amount, setAmount] = useState("");

  
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("http://127.0.0.1:5000/api/order/place", {
        user_id: 1, // Replace with logged-in user's ID
        type,
        price: parseFloat(price),
        amount: parseFloat(amount),
      });
      alert("Order placed successfully!");
      console.log("Response:", response.data);
    } catch (error) {
      console.error("Error placing order:", error);
      alert("Failed to place order.");
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Place Order</h2>
      <label>
        Order Type:
        <select value={type} onChange={(e) => setType(e.target.value)}>
          <option value="buy">Buy</option>
          <option value="sell">Sell</option>
        </select>
      </label>
      <label>
        Price:
        <input
          type="number"
          value={price}
          onChange={(e) => setPrice(e.target.value)}
          required
        />
      </label>
      <label>
        Amount:
        <input
          type="number"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
          required
        />
      </label>
      <button type="submit">Place Order</button>
    </form>
  );
};

export default OrderForm;
