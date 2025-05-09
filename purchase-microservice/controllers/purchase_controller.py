from flask import Blueprint, request, jsonify

from models.purchase import Purchase
from models.book import Book
from extensions import db

purchase = Blueprint('purchase', __name__)

@purchase.route('/buy', methods=['POST'])
def buy():
    """
    Handle book purchase by a logged-in user.
    Checks stock and creates a new purchase, reducing book inventory.
    """
    try:
        data = request.get_json()
        book_id = data.get('book_id')
        quantity = data.get('quantity')
        price = data.get('price')
        user_id = data.get('user_id')
        
        book = Book.query.get_or_404(book_id)
        
        if book.stock < quantity:
            return jsonify({
                'message': 'No hay suficiente stock disponible.',
                'status': 400
            }), 400
            
        total_price = price * quantity
        
        new_purchase = Purchase(
            user_id=user_id,
            book_id=book_id,
            quantity=quantity,
            total_price=total_price,
            status='Pending Payment'
        )
        book.stock -= quantity
        db.session.add(new_purchase)
        db.session.commit()
        return jsonify({
            'message': 'Compra realizada con éxito.',
            'purchase_id': new_purchase.id
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'message': 'Error al procesar la compra.',
            'error': str(e)
        }), 500
