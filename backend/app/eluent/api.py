"""Eluent API."""
from app.extensions import db
from app.utils.types import JSON
from flask_smorest import Blueprint, abort

from .models import Eluent
from .serializers import EluentSchema

blueprint = Blueprint(
    "eluents", "eluents", url_prefix="/api/eluents", description="Operations on eluents"
)


@blueprint.route("/", methods=["GET"])
@blueprint.response(200, EluentSchema(many=True))
def eluents_get():
    return Eluent.query.all()


@blueprint.route("/<string:id>", methods=["GET"])
@blueprint.response(200, EluentSchema())
def eluent_get(id: str):
    eluent = Eluent.query.get(id)
    if eluent is None:
        abort(404, message="Eluent not found.")
    return eluent


@blueprint.route("/", methods=["POST"])
@blueprint.arguments(EluentSchema())
@blueprint.response(201, EluentSchema())
def eluent_create(user_data: JSON):
    eluent = Eluent(**user_data)
    db.session.add(eluent)
    db.session.commit()
    return eluent


@blueprint.route("/<string:id>", methods=["POST"])
@blueprint.arguments(EluentSchema())
@blueprint.response(200, EluentSchema())
def eluent_update(user_data: JSON, id: str):
    eluent = Eluent.query.get(id)
    if not eluent:
        abort(404, message="Eluent not found.")

    # Assign validated attributes to the model.
    for attr, value in user_data.items():
        setattr(eluent, attr, value)

    db.session.add(eluent)
    db.session.commit()
    return eluent


@blueprint.route("/<string:id>", methods=["DELETE"])
@blueprint.response(200, EluentSchema())
def eluent_delete(id: str):
    eluent = Eluent.query.get(id)
    if not eluent:
        abort(404, message="Eluent not found.")

    db.session.delete(eluent)
    db.session.commit()
    return eluent
