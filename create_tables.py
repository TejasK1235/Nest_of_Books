# create_tables.py
"""
Creates all necessary tables for the Nest of Books project.
Safe to run multiple times — it only creates tables if they don't exist.
"""

from app.repositories.user_repository import UserRepository
from app.repositories.book_repository import BookRepository
from app.repositories.order_repository import OrderRepository
from app.repositories.base_repository import BaseRepository     

def setup_database():
    db = BaseRepository()
    cursor = db.conn.cursor()

    # 1️⃣ Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT CHECK(role IN ('admin', 'customer')) NOT NULL,
        address TEXT3
    );
    """)

    # 2️⃣ Books Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        book_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        price REAL NOT NULL CHECK(price >= 0),
        stock INTEGER NOT NULL CHECK(stock >= 0)
    );
    """)

    # 3️⃣ Orders Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        total_amount REAL NOT NULL CHECK(total_amount >= 0),
        status TEXT CHECK(status IN ('Pending', 'Confirmed', 'Cancelled')) NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
    """)

    # 4️⃣ Payments Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS payments (
        payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        method TEXT CHECK(method IN ('Card', 'UPI', 'COD')) NOT NULL,
        status TEXT CHECK(status IN ('Pending', 'Success', 'Failed')) NOT NULL,
        FOREIGN KEY (order_id) REFERENCES orders(order_id)
    );
    """)

    # 5️⃣ Cart Items Table (for persistent cart storage)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cart_items (
        cart_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        book_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL CHECK(quantity > 0),
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (book_id) REFERENCES books(book_id)
    );
    """)

    db.conn.commit()
    print("✅ All tables verified or created successfully!")

if __name__ == "__main__":
    setup_database()
