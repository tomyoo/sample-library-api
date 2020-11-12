from flask import Blueprint, jsonify, request, current_app
from webargs import fields, validate
from webargs.flaskparser import parser
from datetime import datetime
from sqlalchemy import exists

from .schema import BookRequestSchema
from ..models.models import User, Book, BookRequest
from ..lib.resource import ModelResource
from ..extensions import db

api = Blueprint('api', __name__)


class BookRequestsView(ModelResource):
    schema = BookRequestSchema
    route_base = '/request'

    def index(self):
        query = BookRequest.query.filter_by(deleted_at=None)
        return self.schema(many=True).jsonify(query.all())

    def post(self):
        input_args = {
            "email": fields.Str(required=True, validate=validate.Email()),
            "title": fields.Str(required=True)
        }

        args = parser.parse(input_args, request)

        user = User.query.filter_by(email=args["email"]).first_or_404()
        book = Book.query.filter_by(title=args["title"]).first_or_404()
        request_exists = db.session.query(
            db.session.query(BookRequest).filter(
                BookRequest.book == book and BookRequest.deleted_at is None
            ).exists()).scalar()

        if not request_exists:  # Book is available
            new_request = BookRequest(
                book=book,
                user=user
            )
            db.session.add(new_request)
            db.session.commit()

            return jsonify(
                {
                    "id": book.id,
                    "available": True,
                    "title": book.title,
                    "timestamp": new_request.created_at.strftime('%Y-%m-%dT%H:%M:%S.%f'),
                }
            ), 201

        else:  # Book is not available
            return jsonify(
                {
                    "id": book.id,
                    "available": False,
                    "title": book.title,
                    "timestamp": datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f'),
                }
            ), 400

    def delete(self, _id):
        request_obj = self._model.query.get_or_404(_id)
        book = request_obj.book

        if request_obj.deleted_at is None:
            request_obj.deleted_at = datetime.now()
            book.current_request = None
            db.session.commit()
            return "", 204
        else:
            return jsonify({"error": "This book request has already been deleted."}), 400


BookRequestsView.register(api)
