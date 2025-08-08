import sqlite3
import os


def setup_mock_database(db_path: str):
    """Sets up a mock SQLite database and populates it with sample data."""
    # Ensure the client_data directory exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Drop tables to ensure a clean slate
    cursor.execute("DROP TABLE IF EXISTS products")
    cursor.execute("DROP TABLE IF EXISTS customers")
    cursor.execute("DROP TABLE IF EXISTS orders")

    # DDL for tables
    cursor.execute("""
        CREATE TABLE products (
            product_id TEXT PRIMARY KEY,
            product_name TEXT NOT NULL,
            category TEXT,
            price REAL NOT NULL
        );
    """)
    cursor.execute("""
        CREATE TABLE customers (
            customer_id TEXT PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email_address TEXT
        );
    """)
    cursor.execute("""
        CREATE TABLE orders (
            order_id TEXT PRIMARY KEY,
            customer_id_fk TEXT,
            product_id_fk TEXT,
            quantity INTEGER,
            order_date TEXT,
            FOREIGN KEY(customer_id_fk) REFERENCES customers(customer_id),
            FOREIGN KEY(product_id_fk) REFERENCES products(product_id)
        );
    """)

    # Insert sample data
    cursor.execute("INSERT INTO products VALUES ('P101', 'Croissant', 'Pastry', 2.50)")
    cursor.execute("INSERT INTO products VALUES ('P102', 'Baguette', 'Bread', 3.00)")
    cursor.execute("INSERT INTO customers VALUES ('CUST01', 'Alice', 'Smith', 'alice@example.com')")
    cursor.execute("INSERT INTO orders VALUES ('ORD01', 'CUST01', 'P101', 2, '2023-10-27')")

    conn.commit()
    conn.close()


def create_mock_documentation(doc_path: str):
    """Creates a simple documentation file."""
    os.makedirs(os.path.dirname(doc_path), exist_ok=True)

    with open(doc_path, "w") as f:
        f.write("Our business has a few simple rules.\n\n")
        f.write("A customer's email address must be a valid email format.\n")
        f.write("All orders must have a positive quantity.\n")
        f.write("The order_date should always be on or after the effective date of the customer record.\n")
        f.write("We use product_id as the unique identifier for our products.\n")
        f.write("The 'orders' table links our customers to their purchased products.\n")
        f.write("The `insert_data.py` script is used to ingest new order records into the database.")


def create_mock_codebase(code_path: str):
    """Creates a simple Python script to act as code input."""
    os.makedirs(os.path.dirname(code_path), exist_ok=True)

    script_content = """
# insert_data.py
import sqlite3

def insert_order(db_name, order_data):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(\"\"\"
        INSERT INTO orders (order_id, customer_id_fk, product_id_fk, quantity, order_date) 
        VALUES (?, ?, ?, ?, ?);
    \"\"\", order_data)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    order_data = ('ORD02', 'CUST01', 'P102', 1, '2023-10-28')
    insert_order('bakery.sqlite', order_data)
"""
    with open(code_path + "/insert_data.py", "w") as f:
        f.write(script_content)


if __name__ == "__main__":
    # Example usage when running this file directly
    db_path = "../resources/client_data/bakery.sqlite"
    doc_path = "../resources/client_data/business_rules.txt"
    setup_mock_database(db_path)
    create_mock_documentation(doc_path)
    create_mock_codebase("../resources/client_data")
    print(f"Mock database created at: {db_path}")
    print(f"Mock documentation created at: {doc_path}")
