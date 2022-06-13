"""Column API."""
from app.extensions import db
from app.utils.types import JSON
from flask_smorest import Blueprint, abort

from .models import Column
from .serializers import ColumnSchema

blueprint = Blueprint(
    "columns", "columns", url_prefix="/api/columns", description="Operations on columns"
)


@blueprint.route("/", methods=["GET"])
@blueprint.response(200, ColumnSchema(many=True))
def columns_get():
    return Column.query.all()


@blueprint.route("/<string:id>", methods=["GET"])
@blueprint.response(200, ColumnSchema())
def column_get(id: str):
    column = Column.query.get(id)
    if column is None:
        abort(404, message="Column not found.")
    return column


@blueprint.route("/", methods=["POST"])
@blueprint.arguments(ColumnSchema())
@blueprint.response(201, ColumnSchema())
def column_create(user_data: JSON):
    column = Column(**user_data)
    db.session.add(column)
    db.session.commit()
    return column


@blueprint.route("/<string:id>", methods=["POST"])
@blueprint.arguments(ColumnSchema())
@blueprint.response(200, ColumnSchema())
def column_update(user_data: JSON, id: str):
    column = Column.query.get(id)
    if not column:
        abort(404, message="Column not found.")

    # Assign validated attributes to the model.
    for attr, value in user_data.items():
        setattr(column, attr, value)

    db.session.add(column)
    db.session.commit()
    return column


@blueprint.route("/<string:id>", methods=["DELETE"])
@blueprint.response(200, ColumnSchema())
def column_delete(id: str):
    column = Column.query.get(id)
    if not column:
        abort(404, message="Column not found.")

    db.session.delete(column)
    db.session.commit()
    return column
