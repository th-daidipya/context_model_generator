
# insert_data.py
import sqlite3

def insert_order(db_name, order_data):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO orders (order_id, customer_id_fk, product_id_fk, quantity, order_date) 
        VALUES (?, ?, ?, ?, ?);
    """, order_data)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    order_data = ('ORD02', 'CUST01', 'P102', 1, '2023-10-28')
    insert_order('bakery.sqlite', order_data)
