"""
Schemas for API requests / responses
"""

from ..lib.schema import BaseSchema
from marshmallow import fields
from ..models.models import User, Book, BookRequest
# from ..extensions import schemas


class UserSchema(BaseSchema):
    """User Schema"""

    email = fields.Str()

    class Meta:
        model = User


class BookSchema(BaseSchema):
    """Book Schema"""

    title = fields.Str()

    class Meta:
        model = Book


class BookRequestSchema(BaseSchema):
    """BookRequest Schema"""

    user = fields.Nested(UserSchema)
    book = fields.Nested(BookSchema)
    created_at = fields.DateTime(required=True)
    deleted_at = fields.DateTime(required=False)

    class Meta:
        model = BookRequest
