from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required

from models.payment import Payment
from models.purchase import Purchase
from extensions import db

payment = Blueprint('payment', __name__)

@payment.route('/payment/<int:purchase_id>', methods=['GET', 'POST'])
@login_required
def payment_page(purchase_id):
    """
    Handle payment processing for a given purchase.
    On POST: create payment record and mark purchase as 'Paid'.
    """
    if request.method == 'POST':
        method = request.form.get('method')
        amount = request.form.get('amount')

        # Create payment record
        new_payment = Payment(
            purchase_id=purchase_id,
            amount=amount,
            payment_method=method,
            payment_status='Paid'
        )
        db.session.add(new_payment)

        # Update purchase status
        purchase = Purchase.query.get(purchase_id)
        purchase.status = 'Paid'

        db.session.commit()

        return redirect(url_for('delivery.select_delivery', purchase_id=purchase_id))

    return render_template('payment.html', purchase_id=purchase_id)
