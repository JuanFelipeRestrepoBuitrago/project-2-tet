from flask import Blueprint, jsonify, request
from models.book import Book
from extensions import db

book = Blueprint('book', __name__)

@book.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([{
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'description': book.description,
        'price': book.price,
        'stock': book.stock,
        'seller_id': book.seller_id
    } for book in books])

@book.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get_or_404(book_id)
    return jsonify({
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'description': book.description,
        'price': book.price,
        'stock': book.stock,
        'seller_id': book.seller_id
    })

@book.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()
    new_book = Book(
        title=data['title'],
        author=data['author'],
        description=data.get('description'),
        price=float(data['price']),
        stock=int(data['stock']),
        seller_id=data['seller_id']
    )
    db.session.add(new_book)
    db.session.commit()
    return jsonify({
        'id': new_book.id,
        'title': new_book.title,
        'author': new_book.author,
        'description': new_book.description,
        'price': new_book.price,
        'stock': new_book.stock,
        'seller_id': new_book.seller_id
    }), 201

@book.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = Book.query.get_or_404(book_id)
    data = request.get_json()
    
    book.title = data.get('title', book.title)
    book.author = data.get('author', book.author)
    book.description = data.get('description', book.description)
    book.price = float(data.get('price', book.price))
    book.stock = int(data.get('stock', book.stock))
    book.seller_id = data.get('seller_id', book.seller_id)
    
    db.session.commit()
    return jsonify({
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'description': book.description,
        'price': book.price,
        'stock': book.stock,
        'seller_id': book.seller_id
    })

@book.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return '', 204

@book.route('/my-books', methods=['POST'])
def get_my_books():
    """Get books created by the current user"""
    data = request.get_json()
    books = Book.query.filter_by(seller_id=data["user_id"]).all()
    return jsonify([{
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'description': book.description,
        'price': book.price,
        'stock': book.stock,
        'seller_id': book.seller_id
    } for book in books])
