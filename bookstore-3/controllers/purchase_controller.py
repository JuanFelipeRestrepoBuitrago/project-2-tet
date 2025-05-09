from flask import Blueprint, request, redirect, url_for, session, current_app, flash
import requests
from utils.utils import check_user_auth

purchase = Blueprint('purchase', __name__)

@purchase.route('/buy/<int:book_id>', methods=['POST'])
def buy(book_id):
    """
    Handle book purchase by a logged-in user.
    Checks stock and creates a new purchase, reducing book inventory.
    """
    user = check_user_auth(session.get('token'))
    if not user:
        return redirect(url_for('auth.login'))
    quantity = int(request.form.get('quantity'))
    price = float(request.form.get('price'))
    
    response = requests.post(
        f'{current_app.config["PURCHASE_SERVICE_URL"]}/buy',
        json={
            'book_id': book_id,
            'quantity': quantity,
            'price': price,
            'user_id': user['id']
        }
    )

    if not response.ok:
        flash('Error processing purchase' + str(response.json()), 'error')
        return redirect(url_for('book.catalog'))
    
    data = response.json()

    return redirect(url_for('payment.payment_page', purchase_id=data['purchase_id']))
