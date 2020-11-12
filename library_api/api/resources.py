from flask import Blueprint, jsonify, request, current_app
from webargs import fields, validate
from webargs.flaskparser import parser
from datetime import datetime

from .schema import BookRequestSchema
from ..models.models import User, Book, BookRequest
from ..lib.resource import ModelResource
from ..extensions import db

api = Blueprint('api', __name__)


class BookRequestsView(ModelResource):
    schema = BookRequestSchema

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

        if book.current_request is None:  # Book is available
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
                    "timestamp": new_request.created_at,
                }
            ), 201

        else:  # Book is not available
            return jsonify(
                {
                    "id": book.id,
                    "available": False,
                    "title": book.title,
                    "timestamp": datetime.now(),
                }
            ), 200

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
