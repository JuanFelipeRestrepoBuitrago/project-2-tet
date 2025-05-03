from flask import Blueprint, request, redirect, url_for
from flask_login import login_required, current_user

from models.purchase import Purchase
from models.book import Book
from extensions import db

purchase = Blueprint('purchase', __name__)

@purchase.route('/buy/<int:book_id>', methods=['POST'])
@login_required
def buy(book_id):
    """
    Handle book purchase by a logged-in user.
    Checks stock and creates a new purchase, reducing book inventory.
    """
    quantity = int(request.form.get('quantity'))
    price = float(request.form.get('price'))

    book = Book.query.get_or_404(book_id)

    if book.stock < quantity:
        return "No hay suficiente stock disponible.", 400

    total_price = price * quantity

    # Create purchase
    new_purchase = Purchase(
        user_id=current_user.id,
        book_id=book_id,
        quantity=quantity,
        total_price=total_price,
        status='Pending Payment'
    )

    # Update stock
    book.stock -= quantity

    db.session.add(new_purchase)
    db.session.commit()

    return redirect(url_for('payment.payment_page', purchase_id=new_purchase.id))
