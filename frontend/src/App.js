import './App.css';
import React from "react";
import TradingViewWidget from "./components/Chart";
import OrderForm from './components/OrderForm';
import OrderBook from './components/OrderBook';
import Wallet from './components/Wallet';
import TradeHistory from './components/TradeHistory';

function App() {
  return (
    <div className="app-container">
      <div className="main-container">
        {/* Trading Chart */}
        <div className="chart-container">
          <TradingViewWidget />
        </div>
        
        <div className="side-panel">
          {/* Order Form */}
          <div className="panel-section">
            <h3>Place Order</h3>
            <OrderForm />
          </div>
          
          {/* Order Book */}
          <div className="panel-section">
            <h3>Order Book</h3>
            <OrderBook />
          </div>
          
          {/* Wallet */}
          <div className="panel-section">
            <h3>Your Wallet</h3>
            <Wallet />
          </div>

          {/* Trade History */}
          <div className="panel-section">
            <h3>Trade History</h3>
            <TradeHistory />
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
