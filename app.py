import os
from flask import Flask, render_template, send_from_directory
from database import init_db, get_db_connection
from routes.auth import auth_bp
from routes.products import products_bp
from routes.wishlist import wishlist_bp
from routes.messages import messages_bp
from routes.admin import admin_bp

app = Flask(__name__)
app.secret_key = "ecofinds_hackathon_super_secret_key"
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads', 'products')

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(products_bp)
app.register_blueprint(wishlist_bp)
app.register_blueprint(messages_bp)
app.register_blueprint(admin_bp)

# Auto-initialize SQLite database tables
with app.app_context():
    init_db()

@app.route('/')
def index():
    conn = get_db_connection()
    featured_products = conn.execute(
        'SELECT p.*, u.name as seller_name FROM products p JOIN users u ON p.seller_id = u.id WHERE p.status = "available" ORDER BY p.id DESC LIMIT 6'
    ).fetchall()
    conn.close()
    return render_template('index.html', products=featured_products)

@app.route('/uploads/products/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True, port=5000)