import React, { useState, useEffect } from "react";
import axios from "axios";

const Wallet = () => {
  const [balance, setBalance] = useState("");
  const [amount, setAmount] = useState("");

  // Fetch wallet balance on component load
  useEffect(() => {
    const fetchBalance = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:5000/api/wallet/balance");
        setBalance(response.data.balance);
      } catch (error) {
        console.error("Error fetching wallet balance:", error);
        alert("Failed to fetch wallet balance.");
      }
    };
    fetchBalance();
  }, []);

  // Handle deposit action
  const handleDeposit = async () => {
    try {
      const response = await axios.post("http://127.0.0.1:5000/api/wallet/deposit", { amount });
      alert(response.data.message);
      // Optionally fetch the updated balance after deposit
      fetchBalance();
    } catch (error) {
      console.error("Error during deposit:", error);
      alert("Failed to deposit funds.");
    }
  };

  // Handle withdraw action
  const handleWithdraw = async () => {
    try {
      const response = await axios.post("http://127.0.0.1:5000/api/wallet/withdraw", { amount });
      alert(response.data.message);
      // Optionally fetch the updated balance after withdrawal
      fetchBalance();
    } catch (error) {
      console.error("Error during withdrawal:", error);
      alert("Failed to withdraw funds.");
    }
  };

  // Fetch updated balance
  const fetchBalance = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:5000/api/wallet/balance");
      setBalance(response.data.balance);
    } catch (error) {
      console.error("Error fetching wallet balance:", error);
    }
  };

  return (
    <div>
      <h2>Wallet</h2>
      <p>Current Balance: {balance}</p>
      <div>
        <h3>Deposit</h3>
        <input
          type="number"
          placeholder="Enter amount"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
        />
        <button onClick={handleDeposit}>Deposit</button>
      </div>
      <div>
        <h3>Withdraw</h3>
        <input
          type="number"
          placeholder="Enter amount"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
        />
        <button onClick={handleWithdraw}>Withdraw</button>
      </div>
    </div>
  );
};

export default Wallet;
