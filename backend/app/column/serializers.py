from uuid import UUID
from typing import Optional

from marshmallow import fields, validates_schema, ValidationError

from app.utils.serializers import WrapDataSchema
from app.utils.types import JSON
from .models import Column


def validate_unique_field(
    name: str, value: Optional[str], id: Optional[UUID] = None
) -> None:
    """Validate unique field.

    Args:
        name: field name to validate ('username' or 'email')
        value: value to validate
        id: optional user id, should be specified on user update

    Returns:
        Nothing, raises ValidationError if validation failed.
    """
    query = Column.query.filter(getattr(Column, name) == value)
    if id is not None:
        # Allow updating username or email for the user to the
        # same value.
        query = query.filter(Column.id != id)
    if query.first():
        raise ValidationError("{} should be unique: {}".format(name, value), name)

class ColumnSchema(WrapDataSchema):
    id = fields.Str()
    name = fields.Str(required=True)

    @validates_schema
    def validate_unique_fields(self, data: JSON, partial: bool, many: bool) -> None:
        id = None
        if "id" in data:
            id = data["id"]

        name = data.get("name")
        validate_unique_field("name", name, id)
