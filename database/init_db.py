import sys
import os

# Add parent directory to path to allow importing app modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from werkzeug.security import generate_password_hash
from database import get_db_connection, init_db
from utils.scoring import calculate_sustainability_score

def seed_database():
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()

    # Predefined users
    admin_pw = generate_password_hash("admin123")
    user1_pw = generate_password_hash("user123")
    user2_pw = generate_password_hash("user123")

    cursor.execute("INSERT OR IGNORE INTO users (id, name, email, password, role) VALUES (?, ?, ?, ?, ?)",
                   (1, "EcoFinds Admin", "admin@ecofinds.com", admin_pw, "admin"))
    cursor.execute("INSERT OR IGNORE INTO users (id, name, email, password, role) VALUES (?, ?, ?, ?, ?)",
                   (2, "Anuradha Sharma", "anuradha@ecofinds.com", user1_pw, "user"))
    cursor.execute("INSERT OR IGNORE INTO users (id, name, email, password, role) VALUES (?, ?, ?, ?, ?)",
                   (3, "Alex Chen", "alex@ecofinds.com", user2_pw, "user"))

    # Demo marketplace products
    sample_products = [
        (2, "Engineering Mathematics 5th Ed", "Clean condition with minimal markings. Essential for semester 1 & 2.", "Books", "Good", 25.00, "Campus Library Block", ""),
        (3, "Refurbished ThinkPad T480", "16GB RAM, 512GB SSD, Intel i5 8th Gen. Battery health 88%.", "Electronics", "Used", 220.00, "Downtown Center", ""),
        (2, "HydroFlask Insulated Water Bottle", "Stainless steel 32oz bottle. No dents, thoroughly sanitized.", "Accessories", "Like New", 14.00, "Student Union", ""),
        (3, "Ergonomic Mesh Study Chair", "Adjustable height and lumbar support. Minor cosmetic wear on armrests.", "Furniture", "Fair", 45.00, "North Campus", ""),
        (2, "Wireless Noise-Cancelling Headphones", "Over-ear bluetooth headphones with charging case and auxiliary cord.", "Electronics", "Good", 38.00, "West Hall", ""),
        (3, "Trail Runner Outdoor Shoes (Size 10)", "Only worn twice for trail test. Soles intact and spotless.", "Sports", "Like New", 30.00, "Sports Complex", "")
    ]

    for prod in sample_products:
        score = calculate_sustainability_score(prod[3], prod[4])
        cursor.execute('''
            INSERT OR IGNORE INTO products (seller_id, title, description, category, condition, price, location, image, sustainability_score)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (prod[0], prod[1], prod[2], prod[3], prod[4], prod[5], prod[6], prod[7], score))

    conn.commit()
    conn.close()
    print("EcoFinds database tables created and seeded successfully.")

if __name__ == '__main__':
    seed_database()