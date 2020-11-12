from ..extensions import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))


class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))

    current_request_id = db.Column(db.Integer, db.ForeignKey('book_requests.id'))
    current_request = db.relationship('BookRequest', foreign_keys=current_request_id)


class BookRequest(db.Model):
    __tablename__ = 'book_requests'

    id = db.Column(db.Integer, primary_key=True)

    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
    book = db.relationship('Book', foreign_keys=book_id)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', foreign_keys=user_id)

    created_at = db.Column(db.DateTime(), default=datetime.now())
    deleted_at = db.Column(db.DateTime(), default=None)
