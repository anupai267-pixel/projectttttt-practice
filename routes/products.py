from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from database import get_db_connection
from utils.scoring import calculate_sustainability_score
from utils.validation import save_product_image

products_bp = Blueprint('products', __name__)

@products_bp.route('/products')
def browse():
    search = request.args.get('search', '').strip()
    category = request.args.get('category', '').strip()
    condition = request.args.get('condition', '').strip()
    location = request.args.get('location', '').strip()
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    sort_by = request.args.get('sort', 'newest')

    query = 'SELECT p.*, u.name as seller_name FROM products p JOIN users u ON p.seller_id = u.id WHERE p.status = "available"'
    params = []

    if search:
        query += ' AND (p.title LIKE ? OR p.description LIKE ? OR p.category LIKE ?)'
        params.extend([f'%{search}%', f'%{search}%', f'%{search}%'])
    if category:
        query += ' AND p.category = ?'
        params.append(category)
    if condition:
        query += ' AND p.condition = ?'
        params.append(condition)
    if location:
        query += ' AND p.location LIKE ?'
        params.append(f'%{location}%')
    if min_price is not None:
        query += ' AND p.price >= ?'
        params.append(min_price)
    if max_price is not None:
        query += ' AND p.price <= ?'
        params.append(max_price)

    if sort_by == 'price_asc':
        query += ' ORDER BY p.price ASC'
    elif sort_by == 'price_desc':
        query += ' ORDER BY p.price DESC'
    elif sort_by == 'sustainability':
        query += ' ORDER BY p.sustainability_score DESC'
    else:
        query += ' ORDER BY p.id DESC'

    conn = get_db_connection()
    products = conn.execute(query, params).fetchall()

    user_wishlist = []
    if 'user_id' in session:
        w_rows = conn.execute('SELECT product_id FROM wishlist WHERE user_id = ?', (session['user_id'],)).fetchall()
        user_wishlist = [w['product_id'] for w in w_rows]
    conn.close()

    return render_template('products.html', products=products, wishlist_ids=user_wishlist)

@products_bp.route('/product/<int:product_id>')
def details(product_id):
    conn = get_db_connection()
    product = conn.execute(
        'SELECT p.*, u.name as seller_name, u.email as seller_email FROM products p JOIN users u ON p.seller_id = u.id WHERE p.id = ?',
        (product_id,)
    ).fetchone()

    if not product:
        conn.close()
        flash('Product not found.', 'danger')
        return redirect(url_for('products.browse'))

    is_wishlisted = False
    if 'user_id' in session:
        w = conn.execute('SELECT id FROM wishlist WHERE user_id = ? AND product_id = ?',
                         (session['user_id'], product_id)).fetchone()
        is_wishlisted = bool(w)

    conn.close()
    return render_template('product-details.html', product=product, is_wishlisted=is_wishlisted)

@products_bp.route('/sell', methods=['GET', 'POST'])
def sell():
    if 'user_id' not in session:
        flash('Please log in to sell items.', 'warning')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        category = request.form.get('category', '').strip()
        condition = request.form.get('condition', '').strip()
        price = request.form.get('price', type=float)
        location = request.form.get('location', '').strip()
        image_file = request.files.get('image')

        if not title or not description or not category or not condition or price is None or not location:
            flash('All product fields are required.', 'danger')
            return render_template('sell.html')

        saved_image_name = ""
        if image_file and image_file.filename != '':
            saved_image_name = save_product_image(image_file, current_app.config['UPLOAD_FOLDER'])

        score = calculate_sustainability_score(category, condition)

        conn = get_db_connection()
        conn.execute('''
            INSERT INTO products (seller_id, title, description, category, condition, price, location, image, sustainability_score)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (session['user_id'], title, description, category, condition, price, location, saved_image_name, score))
        conn.commit()
        conn.close()

        flash('Product listed successfully! 🌱', 'success')
        return redirect(url_for('products.browse'))

    return render_template('sell.html')

@products_bp.route('/product/delete/<int:product_id>', methods=['POST'])
def delete(product_id):
    if 'user_id' not in session:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('auth.login'))

    conn = get_db_connection()
    product = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()

    if not product:
        conn.close()
        flash('Product not found.', 'danger')
        return redirect(url_for('products.browse'))

    if product['seller_id'] != session['user_id'] and session.get('user_role') != 'admin':
        conn.close()
        flash('You are not authorized to delete this product.', 'danger')
        return redirect(url_for('products.browse'))

    conn.execute('DELETE FROM products WHERE id = ?', (product_id,))
    conn.commit()
    conn.close()
    flash('Product deleted successfully.', 'success')
    return redirect(request.referrer or url_for('products.browse'))