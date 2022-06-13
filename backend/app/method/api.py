"""Method API."""
from app.extensions import db
from app.utils.types import JSON
from flask_smorest import Blueprint, abort

from .models import Method
from .serializers import MethodSchema

blueprint = Blueprint(
    "methods", "methods", url_prefix="/api/methods", description="Operations on methods"
)


@blueprint.route("/", methods=["GET"])
@blueprint.response(200, MethodSchema(many=True))
def methods_get():
    return Method.query.all()


@blueprint.route("/<string:id>", methods=["GET"])
@blueprint.response(200, MethodSchema())
def method_get(id: str):
    method = Method.query.get(id)
    if method is None:
        abort(404, message="Method not found.")
    return method


@blueprint.route("/", methods=["POST"])
@blueprint.arguments(MethodSchema())
@blueprint.response(201, MethodSchema())
def method_create(user_data: JSON):
    method = Method(**user_data)
    db.session.add(method)
    db.session.commit()
    return method


@blueprint.route("/<string:id>", methods=["POST"])
@blueprint.arguments(MethodSchema())
@blueprint.response(200, MethodSchema())
def method_update(user_data: JSON, id: str):
    method = Method.query.get(id)
    if not method:
        abort(404, message="Method not found.")

    # Assign validated attributes to the model.
    for attr, value in user_data.items():
        setattr(method, attr, value)

    db.session.add(method)
    db.session.commit()
    return method


@blueprint.route("/<string:id>", methods=["DELETE"])
@blueprint.response(200, MethodSchema())
def method_delete(id: str):
    method = Method.query.get(id)
    if not method:
        abort(404, message="Method not found.")

    db.session.delete(method)
    db.session.commit()
    return method
