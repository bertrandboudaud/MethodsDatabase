"""Compound API."""
from app.extensions import db
from app.utils.types import JSON
from flask_smorest import Blueprint, abort

from .models import Compound
from .serializers import CompoundSchema
from .serializers import CompoundFilterSchema

blueprint = Blueprint(
    "compounds", "compounds", url_prefix="/api/compounds", description="Operations on compounds"
)


@blueprint.route("/", methods=["GET"])
@blueprint.arguments(CompoundFilterSchema, location="query")
@blueprint.response(200, CompoundSchema(many=True))
def compounds_get(args):
    name = args.get("name", "")
    if (name != ""):
        return Compound.query.filter(Compound.name.contains(name)).all()
    else:
        return Compound.query.all()


@blueprint.route("/<string:id>", methods=["GET"])
@blueprint.response(200, CompoundSchema())
def compound_get(id: str):
    compound = Compound.query.get(id)
    if compound is None:
        abort(404, message="Compound not found.")
    return compound


@blueprint.route("/", methods=["POST"])
@blueprint.arguments(CompoundSchema())
@blueprint.response(201, CompoundSchema())
def compound_create(user_data: JSON):
    compound = Compound(**user_data)
    db.session.add(compound)
    db.session.commit()
    return compound


@blueprint.route("/<string:id>", methods=["POST"])
@blueprint.arguments(CompoundSchema())
@blueprint.response(200, CompoundSchema())
def compound_update(user_data: JSON, id: str):
    compound = Compound.query.get(id)
    if not compound:
        abort(404, message="Compound not found.")

    # Assign validated attributes to the model.
    for attr, value in user_data.items():
        setattr(compound, attr, value)

    db.session.add(compound)
    db.session.commit()
    return compound


@blueprint.route("/<string:id>", methods=["DELETE"])
@blueprint.response(200, CompoundSchema())
def compound_delete(id: str):
    compound = Compound.query.get(id)
    if not compound:
        abort(404, message="Compound not found.")

    db.session.delete(compound)
    db.session.commit()
    return compound
