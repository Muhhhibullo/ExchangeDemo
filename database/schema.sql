USE crypto_exchange;

CREATE TABLE wallet (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    balance DECIMAL(18, 8) DEFAULT 0,
    currency VARCHAR(10) NOT NULL
);

CREATE TABLE transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    wallet_id INT NOT NULL,
    type ENUM('deposit', 'withdraw', 'transfer') NOT NULL,
    amount DECIMAL(18, 8) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (wallet_id) REFERENCES wallet(id)
);
