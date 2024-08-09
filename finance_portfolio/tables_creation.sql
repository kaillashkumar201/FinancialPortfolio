-- Create holdings table
CREATE TABLE holdings (
    holding_id INT PRIMARY KEY AUTO_INCREMENT,
    ticker VARCHAR(10) NOT NULL UNIQUE,
    quantity INT NOT NULL,
    price DOUBLE NOT NULL,
    last_modified DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create transactions table
CREATE TABLE transactions (
    trans_id INT PRIMARY KEY AUTO_INCREMENT,
    ticker VARCHAR(10) NOT NULL,
    trans_type ENUM('buy', 'sell') NOT NULL,
    quantity INT NOT NULL,
    price_per_unit DOUBLE NOT NULL,
    cumulative DOUBLE NOT NULL,
    last_modified DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create watchlist table
CREATE TABLE watchlist (
    ticker VARCHAR(50) PRIMARY KEY
);

-- Create nasdaq table
CREATE TABLE nasdaq (
    ticker VARCHAR(50) PRIMARY KEY,
    name VARCHAR(500),
    country VARCHAR(100),
    sector VARCHAR(100)
);
