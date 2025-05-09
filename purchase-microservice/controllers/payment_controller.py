from flask import Blueprint, request, jsonify

from models.payment import Payment
from models.purchase import Purchase
from extensions import db

payment = Blueprint('payment', __name__)

@payment.route('/payment', methods=['POST'])
def payment_page():
    """
    Handle payment processing for a given purchase.
    On POST: create payment record and mark purchase as 'Paid'.
    """
    try:
        data = request.get_json()
        purchase_id = data.get('purchase_id')
        method = data.get('method')
        amount = data.get('amount')
        
        new_payment = Payment(
            purchase_id=purchase_id,
            amount=amount,
            payment_method=method,
            payment_status='Paid'
        )
        
        db.session.add(new_payment)
        
        purchase = Purchase.query.get(purchase_id)
        purchase.status = 'Paid'
        db.session.commit()
        
        return jsonify({
            'message': 'Payment processed successfully.',
            'payment_id': new_payment.id
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'message': 'Error processing payment.',
            'error': str(e)
        }), 500
