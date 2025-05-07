from flask import Blueprint, render_template, request, redirect, url_for
from models.book import Book
from extensions import db

book = Blueprint('book', __name__)

@book.route('/catalog')
def catalog():
    books = Book.query.all()
    return render_template('catalog.html', books=books)

@book.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        new_book = Book(
            title=request.form.get('title'),
            author=request.form.get('author'),
            description=request.form.get('description'),
            price=float(request.form.get('price')),
            stock=int(request.form.get('stock')),
            seller_id=1  
        )
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('book.catalog'))

    return render_template('add_book.html')

@book.route('/my_books')
def my_books():
    books = Book.query.all()  
    return render_template('my_books.html', books=books)

@book.route('/edit_book/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    book_to_edit = Book.query.get_or_404(book_id)

    if request.method == 'POST':
        book_to_edit.title = request.form.get('title')
        book_to_edit.author = request.form.get('author')
        book_to_edit.description = request.form.get('description')
        book_to_edit.price = float(request.form.get('price'))
        book_to_edit.stock = int(request.form.get('stock'))
        db.session.commit()
        return redirect(url_for('book.catalog'))

    return render_template('edit_book.html', book=book_to_edit)

@book.route('/delete_book/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    book_to_delete = Book.query.get_or_404(book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('book.catalog'))
