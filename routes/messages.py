from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from database import get_db_connection

messages_bp = Blueprint('messages', __name__)

@messages_bp.route('/messages')
def view_messages():
    if 'user_id' not in session:
        flash('Please log in to access your inbox.', 'warning')
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    conn = get_db_connection()
    
    messages = conn.execute('''
        SELECT m.*, p.title as product_title, 
               sender.name as sender_name, receiver.name as receiver_name
        FROM messages m
        JOIN products p ON m.product_id = p.id
        JOIN users sender ON m.sender_id = sender.id
        JOIN users receiver ON m.receiver_id = receiver.id
        WHERE m.sender_id = ? OR m.receiver_id = ?
        ORDER BY m.created_at DESC
    ''', (user_id, user_id)).fetchall()

    conn.execute('UPDATE messages SET is_read = 1 WHERE receiver_id = ?', (user_id,))
    conn.commit()
    conn.close()

    return render_template('messages.html', messages=messages)

@messages_bp.route('/messages/send', methods=['POST'])
def send_message():
    if 'user_id' not in session:
        flash('Please log in to send messages.', 'warning')
        return redirect(url_for('auth.login'))

    sender_id = session['user_id']
    product_id = request.form.get('product_id', type=int)
    message_text = request.form.get('message', '').strip()

    if not product_id or not message_text:
        flash('Message text cannot be empty.', 'danger')
        return redirect(request.referrer or url_for('products.browse'))

    conn = get_db_connection()
    product = conn.execute('SELECT seller_id FROM products WHERE id = ?', (product_id,)).fetchone()

    if not product:
        conn.close()
        flash('Product not found.', 'danger')
        return redirect(url_for('products.browse'))

    receiver_id = product['seller_id']

    if receiver_id == sender_id:
        conn.close()
        flash('You cannot message yourself about your own product.', 'warning')
        return redirect(url_for('products.details', product_id=product_id))

    conn.execute('''
        INSERT INTO messages (sender_id, receiver_id, product_id, message)
        VALUES (?, ?, ?, ?)
    ''', (sender_id, receiver_id, product_id, message_text))
    conn.commit()
    conn.close()

    flash('Message sent to the seller!', 'success')
    return redirect(url_for('messages.view_messages'))