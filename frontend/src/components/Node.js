const { Pool } = require("pg");

const pool = new Pool({
  user: "postgres",
  host: "localhost",
  database: "crypto_exchange",
  password: "postgres",
  port: 5432,
});

const resetDatabase = async () => {
  try {
    await pool.query("DROP DATABASE IF EXISTS crypto_exchange");
    console.log("Database dropped.");

    await pool.query("CREATE DATABASE crypto_exchange;");
    console.log("Database created.");

    const client = new Pool({
      user: "postgres",
      host: "localhost",
      database: "crypto_exchange",
      password: "postgres",
      port: 5432,
    });

    await client.query(`
      CREATE TABLE wallet (
        id SERIAL PRIMARY KEY,
        user_id INT NOT NULL,
        balance NUMERIC(18, 8) DEFAULT 0,
        currency VARCHAR(10) NOT NULL
      );

      CREATE TABLE transactions (
        id SERIAL PRIMARY KEY,
        wallet_id INT NOT NULL REFERENCES wallet(id),
        type VARCHAR(50) NOT NULL CHECK (type IN ('deposit', 'withdraw', 'transfer')),
        amount NUMERIC(18, 8) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      );
    `);
    console.log("Tables created.");

    await client.query(`
      INSERT INTO wallet (user_id, balance, currency) VALUES
      (1, 1000.00, 'USDT'),
      (2, 500.00, 'BTC');
    `);
    console.log("Initial data inserted.");
  } catch (err) {
    console.error("Error resetting the database:", err);
  } finally {
    pool.end();
  }
};

resetDatabase();
