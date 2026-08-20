from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from database import get_db_connection

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
def admin_dashboard():
    if 'user_id' not in session or session.get('user_role') != 'admin':
        flash('Access denied: Admin privileges required.', 'danger')
        return redirect(url_for('auth.login'))

    conn = get_db_connection()
    total_users = conn.execute('SELECT COUNT(*) FROM users').fetchone()[0]
    total_products = conn.execute('SELECT COUNT(*) FROM products').fetchone()[0]
    active_listings = conn.execute('SELECT COUNT(*) FROM products WHERE status = "available"').fetchone()[0]
    total_wishlists = conn.execute('SELECT COUNT(*) FROM wishlist').fetchone()[0]
    total_messages = conn.execute('SELECT COUNT(*) FROM messages').fetchone()[0]

    users = conn.execute('SELECT id, name, email, role, created_at FROM users ORDER BY id DESC').fetchall()
    products = conn.execute('''
        SELECT p.*, u.name as seller_name 
        FROM products p 
        JOIN users u ON p.seller_id = u.id 
        ORDER BY p.id DESC
    ''').fetchall()
    conn.close()

    stats = {
        'total_users': total_users,
        'total_products': total_products,
        'active_listings': active_listings,
        'total_wishlists': total_wishlists,
        'total_messages': total_messages
    }

    return render_template('admin.html', stats=stats, users=users, products=products)

@admin_bp.route('/admin/user/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    if session.get('user_role') != 'admin':
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('index'))

    if user_id == session.get('user_id'):
        flash('You cannot delete your own admin account.', 'warning')
        return redirect(url_for('admin.admin_dashboard'))

    conn = get_db_connection()
    conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()

    flash('User and their data deleted successfully.', 'success')
    return redirect(url_for('admin.admin_dashboard'))

@admin_bp.route('/dashboard')
def user_dashboard():
    if 'user_id' not in session:
        flash('Please log in to access your dashboard.', 'warning')
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    conn = get_db_connection()
    user_listings = conn.execute('SELECT * FROM products WHERE seller_id = ? ORDER BY id DESC', (user_id,)).fetchall()
    wishlist_count = conn.execute('SELECT COUNT(*) FROM wishlist WHERE user_id = ?', (user_id,)).fetchone()[0]
    unread_messages = conn.execute('SELECT COUNT(*) FROM messages WHERE receiver_id = ? AND is_read = 0', (user_id,)).fetchone()[0]
    conn.close()

    stats = {
        'my_listings': len(user_listings),
        'wishlist_items': wishlist_count,
        'unread_messages': unread_messages,
        'items_sold': 0
    }

    return render_template('dashboard.html', listings=user_listings, stats=stats)