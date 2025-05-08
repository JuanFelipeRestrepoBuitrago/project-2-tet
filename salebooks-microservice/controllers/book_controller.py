from flask import Blueprint, render_template, request, redirect, url_for, session, current_app, flash
import requests
from utils.utils import check_user_auth

book = Blueprint('book', __name__)

# Public catalog view
@book.route('/catalog')
def catalog():
    """
    Display all available books in the public catalog.
    """
    user = check_user_auth(session.get('token'))
    response = requests.get(f'{current_app.config["CATALOG_SERVICE_URL"]}/catalog/books')
    books = response.json() if response.ok else []
    return render_template('catalog.html', books=books, my_user=user)

# View books posted by the current user
@book.route('/my_books')
def my_books():
    """
    Display books created by the currently logged-in user.
    """
    user = check_user_auth(session.get('token'))
    if not user:
        return redirect(url_for('auth.login'))

    response = requests.post(
        f'{current_app.config["CATALOG_SERVICE_URL"]}/catalog/my-books',
        json={
            'user_id': user['id']
        }
    )
    if not response.ok:
        flash('Error fetching your books. Please try again.', 'error')
        return redirect(url_for('book.catalog'))
    books = response.json()
    return render_template('my_books.html', books=books, my_user=user)

# Add a new book
@book.route('/add_book', methods=['GET', 'POST'])
def add_book():
    """
    Handle creation of a new book by the logged-in user.
    """
    user = check_user_auth(session.get('token'))
    if not user:
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        response = requests.post(
            f'{current_app.config["CATALOG_SERVICE_URL"]}/catalog/books',
            json={
                'title': request.form.get('title'),
                'author': request.form.get('author'),
                'description': request.form.get('description'),
                'price': float(request.form.get('price')),
                'stock': int(request.form.get('stock')),
                'seller_id': user['id']
            }
        )
        if response.ok:
            return redirect(url_for('book.catalog'))
        else:
            flash('Error creating book. Please try again.', 'error')

    return render_template('add_book.html', my_user=user)

# Edit an existing book
@book.route('/edit_book/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    """
    Handle editing of an existing book.
    """
    user = check_user_auth(session.get('token'))
    if not user:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        response = requests.put(
            f'{current_app.config["CATALOG_SERVICE_URL"]}/catalog/books/{book_id}',
            json={
                'title': request.form.get('title'),
                'author': request.form.get('author'),
                'description': request.form.get('description'),
                'price': float(request.form.get('price')),
                'stock': int(request.form.get('stock')),
                'seller_id': user['id']
            }
        )
        if response.ok:
            return redirect(url_for('book.catalog'))
        else:
            flash('Error updating book. Please try again.', 'error')

    # Get book details
    response = requests.get(f'{current_app.config["CATALOG_SERVICE_URL"]}/catalog/books/{book_id}')
    if not response.ok:
        flash('Book not found.', 'error')
        return redirect(url_for('book.catalog'))
    
    book = response.json()
    return render_template('edit_book.html', book=book, my_user=user)

# Delete a book
@book.route('/delete_book/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    """
    Handle deletion of a book.
    """
    user = check_user_auth(session.get('token'))
    if not user:
        return redirect(url_for('auth.login'))

    response = requests.delete(
        f'{current_app.config["CATALOG_SERVICE_URL"]}/catalog/books/{book_id}'
    )
    
    if response.ok:
        flash('Book deleted successfully.', 'success')
    else:
        flash('Error deleting book. Please try again.', 'error')
    
    return redirect(url_for('book.catalog'))
