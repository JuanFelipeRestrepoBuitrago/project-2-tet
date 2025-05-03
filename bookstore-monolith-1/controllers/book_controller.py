from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

from models.book import Book
from extensions import db

book = Blueprint('book', __name__)

# Public catalog view
@book.route('/catalog')
def catalog():
    """
    Display all available books in the public catalog.
    """
    books = Book.query.all()
    return render_template('catalog.html', books=books)

# View books posted by the current user
@book.route('/my_books')
@login_required
def my_books():
    """
    Display books created by the currently logged-in user.
    """
    books = Book.query.filter_by(seller_id=current_user.id).all()
    return render_template('my_books.html', books=books)

# Add a new book
@book.route('/add_book', methods=['GET', 'POST'])
@login_required
def add_book():
    """
    Handle creation of a new book by the logged-in user.
    """
    if request.method == 'POST':
        new_book = Book(
            title=request.form.get('title'),
            author=request.form.get('author'),
            description=request.form.get('description'),
            price=float(request.form.get('price')),
            stock=int(request.form.get('stock')),
            seller_id=current_user.id
        )
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('book.catalog'))

    return render_template('add_book.html')

# Edit an existing book
@book.route('/edit_book/<int:book_id>', methods=['GET', 'POST'])
@login_required
def edit_book(book_id):
    """
    Handle editing of an existing book by its owner.
    """
    book_to_edit = Book.query.get_or_404(book_id)
    
    if book_to_edit.seller_id != current_user.id:
        return "No tienes permiso para editar este libro.", 403

    if request.method == 'POST':
        book_to_edit.title = request.form.get('title')
        book_to_edit.author = request.form.get('author')
        book_to_edit.description = request.form.get('description')
        book_to_edit.price = float(request.form.get('price'))
        book_to_edit.stock = int(request.form.get('stock'))
        db.session.commit()
        return redirect(url_for('book.catalog'))

    return render_template('edit_book.html', book=book_to_edit)

# Delete a book
@book.route('/delete_book/<int:book_id>', methods=['POST'])
@login_required
def delete_book(book_id):
    """
    Delete a book if the current user is the owner.
    """
    book_to_delete = Book.query.get_or_404(book_id)

    if book_to_delete.seller_id != current_user.id:
        return "No tienes permiso para eliminar este libro.", 403

    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('book.catalog'))
