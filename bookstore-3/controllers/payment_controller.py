from flask import Blueprint, render_template, request, redirect, url_for, session, current_app, flash
from utils.utils import check_user_auth
import requests

payment = Blueprint('payment', __name__)

@payment.route('/payment/<int:purchase_id>', methods=['GET', 'POST'])
def payment_page(purchase_id):
    """
    Handle payment processing for a given purchase.
    On POST: create payment record and mark purchase as 'Paid'.
    """
    user = check_user_auth(session.get('token'))
    if not user:
        return redirect(url_for('auth.login'))
    if request.method == 'POST':
        method = request.form.get('method')
        amount = request.form.get('amount')
        
        response = requests.post(
            f'{current_app.config["PURCHASE_SERVICE_URL"]}/payment',
            json={
                'purchase_id': purchase_id,
                'amount': amount,
                'method': method
            }
        )

        if not response.ok:
            flash('Error processing payment' + str(response.json()), 'error')
            return redirect(url_for('book.catalog'))

        return redirect(url_for('delivery.select_delivery', purchase_id=purchase_id))

    return render_template('payment.html', purchase_id=purchase_id, my_user=user)
