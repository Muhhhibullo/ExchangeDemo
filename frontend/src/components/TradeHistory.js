import React, { useEffect, useState } from "react";
import axios from "axios";

const TradeHistory = ({ userId }) => {
    const [trades, setTrades] = useState([]);

    useEffect(() => {
        const fetchTrades = async () => {
            const response = await axios.get("http://127.0.0.1:5000/api/order/trade/${userId}");
            setTrades(response.data);
        };
        fetchTrades();
    }, [userId]);

    return (
        <div>
            <h2>Trade History</h2>
            <table>
                <thead>
                    <tr>
                        <th>Buyer</th>
                        <th>Seller</th>
                        <th>Price</th>
                        <th>Amount</th>
                        <th>Timestamp</th>
                    </tr>
                </thead>
                <tbody>
                    {trades.map((trade) => (
                        <tr key={trade.id}>
                            <td>{trade.buyer_id}</td>
                            <td>{trade.seller_id}</td>
                            <td>{trade.price}</td>
                            <td>{trade.amount}</td>
                            <td>{trade.timestamp}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default TradeHistory;
