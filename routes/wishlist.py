from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from database import get_db_connection

wishlist_bp = Blueprint('wishlist', __name__)

@wishlist_bp.route('/wishlist')
def view_wishlist():
    if 'user_id' not in session:
        flash('Please log in to view your wishlist.', 'warning')
        return redirect(url_for('auth.login'))

    conn = get_db_connection()
    items = conn.execute('''
        SELECT p.*, u.name as seller_name, w.id as wishlist_id
        FROM wishlist w
        JOIN products p ON w.product_id = p.id
        JOIN users u ON p.seller_id = u.id
        WHERE w.user_id = ?
        ORDER BY w.id DESC
    ''', (session['user_id'],)).fetchall()
    conn.close()

    return render_template('wishlist.html', items=items)

@wishlist_bp.route('/wishlist/toggle/<int:product_id>', methods=['POST'])
def toggle_wishlist(product_id):
    if 'user_id' not in session:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': False, 'message': 'Please login first', 'redirect': url_for('auth.login')}), 401
        flash('Please log in to manage your wishlist.', 'warning')
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    conn = get_db_connection()
    existing = conn.execute('SELECT id FROM wishlist WHERE user_id = ? AND product_id = ?',
                            (user_id, product_id)).fetchone()

    if existing:
        conn.execute('DELETE FROM wishlist WHERE id = ?', (existing['id'],))
        conn.commit()
        conn.close()
        action = 'removed'
        msg = 'Removed from wishlist'
    else:
        conn.execute('INSERT INTO wishlist (user_id, product_id) VALUES (?, ?)', (user_id, product_id))
        conn.commit()
        conn.close()
        action = 'added'
        msg = 'Added to wishlist! 🌱'

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'success': True, 'action': action, 'message': msg})

    flash(msg, 'success')
    return redirect(request.referrer or url_for('wishlist.view_wishlist'))