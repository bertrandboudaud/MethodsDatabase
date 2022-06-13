"""Instrument API."""
from app.extensions import db
from app.utils.types import JSON
from flask_smorest import Blueprint, abort

from .models import Instrument
from .serializers import InstrumentSchema

blueprint = Blueprint(
    "instruments", "instruments", url_prefix="/api/instruments", description="Operations on instruments"
)


@blueprint.route("/", methods=["GET"])
@blueprint.response(200, InstrumentSchema(many=True))
def instruments_get():
    return Instrument.query.all()


@blueprint.route("/<string:id>", methods=["GET"])
@blueprint.response(200, InstrumentSchema())
def instrument_get(id: str):
    instrument = Instrument.query.get(id)
    if instrument is None:
        abort(404, message="Instrument not found.")
    return instrument


@blueprint.route("/", methods=["POST"])
@blueprint.arguments(InstrumentSchema())
@blueprint.response(201, InstrumentSchema())
def instrument_create(user_data: JSON):
    instrument = Instrument(**user_data)
    db.session.add(instrument)
    db.session.commit()
    return instrument


@blueprint.route("/<string:id>", methods=["POST"])
@blueprint.arguments(InstrumentSchema())
@blueprint.response(200, InstrumentSchema())
def instrument_update(user_data: JSON, id: str):
    instrument = Instrument.query.get(id)
    if not instrument:
        abort(404, message="Instrument not found.")

    # Assign validated attributes to the model.
    for attr, value in user_data.items():
        setattr(instrument, attr, value)

    db.session.add(instrument)
    db.session.commit()
    return instrument


@blueprint.route("/<string:id>", methods=["DELETE"])
@blueprint.response(200, InstrumentSchema())
def instrument_delete(id: str):
    instrument = Instrument.query.get(id)
    if not instrument:
        abort(404, message="Instrument not found.")

    db.session.delete(instrument)
    db.session.commit()
    return instrument
