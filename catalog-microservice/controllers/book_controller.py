from flask import Blueprint, jsonify, request
from models.book import Book
from extensions import db
from utils.auth import token_required

book = Blueprint('book', __name__)

@book.route('/books', methods=['GET'])
def get_books():
    """Get all books"""
    books = Book.query.all()
    return jsonify([book.to_dict() for book in books])

@book.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    """Get a specific book"""
    book = Book.query.get_or_404(book_id)
    return jsonify(book.to_dict())

@book.route('/books', methods=['POST'])
@token_required
def create_book(current_user):
    """Create a new book"""
    data = request.get_json()
    
    new_book = Book(
        title=data['title'],
        author=data['author'],
        description=data['description'],
        price=data['price'],
        stock=data['stock'],
        seller_id=current_user['id']
    )
    
    db.session.add(new_book)
    db.session.commit()
    
    return jsonify(new_book.to_dict()), 201

@book.route('/books/<int:book_id>', methods=['PUT'])
@token_required
def update_book(current_user, book_id):
    """Update a book"""
    book = Book.query.get_or_404(book_id)
    
    if book.seller_id != current_user['id']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    
    book.title = data['title']
    book.author = data['author']
    book.description = data['description']
    book.price = data['price']
    book.stock = data['stock']
    
    db.session.commit()
    
    return jsonify(book.to_dict())

@book.route('/books/<int:book_id>', methods=['DELETE'])
@token_required
def delete_book(current_user, book_id):
    """Delete a book"""
    book = Book.query.get_or_404(book_id)
    
    if book.seller_id != current_user['id']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    db.session.delete(book)
    db.session.commit()
    
    return '', 204

@book.route('/my-books', methods=['GET'])
@token_required
def get_my_books(current_user):
    """Get books created by the current user"""
    books = Book.query.filter_by(seller_id=current_user['id']).all()
    return jsonify([book.to_dict() for book in books]) 