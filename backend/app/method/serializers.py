from uuid import UUID
from typing import Optional

from marshmallow import fields, validates_schema, ValidationError

from app.utils.serializers import WrapDataSchema
from app.utils.types import JSON
from .models import Method


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
    query = Method.query.filter(getattr(Method, name) == value)
    if id is not None:
        # Allow updating username or email for the user to the
        # same value.
        query = query.filter(Method.id != id)
    if query.first():
        raise ValidationError("{} should be unique: {}".format(name, value), name)

class MethodSchema(WrapDataSchema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    technique = fields.Str(required=True)
    comment = fields.Str()
    analysis_method = fields.Str(required=True)
    eluent_a_id = fields.Str()
    eluent_b_id = fields.Str()

    @validates_schema
    def validate_unique_fields(self, data: JSON, partial: bool, many: bool) -> None:
        id = None
        if "method" in self.context:
            id = self.context["method"].id

        name = data.get("name")
        validate_unique_field("name", name, id)
