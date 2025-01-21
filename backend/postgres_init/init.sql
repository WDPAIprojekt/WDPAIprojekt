-- Tabela budżetów
CREATE TABLE budget (
    id SERIAL PRIMARY KEY,
    total_amount NUMERIC(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela wydatków
CREATE TABLE expense (
    id SERIAL PRIMARY KEY,
    budget_id INTEGER NOT NULL,
    name VARCHAR(255) NOT NULL,
    amount NUMERIC(10, 2) NOT NULL,
    FOREIGN KEY (budget_id) REFERENCES budget(id) ON DELETE CASCADE
);