from datetime import datetime
from uuid import uuid4

from app.extensions import db
from sqlalchemy.dialects.postgresql import UUID

class Method(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    technique = db.Column(db.String(80), unique=True, nullable=False)
    comment = db.Column(db.String(80), unique=True, nullable=False)
    analysis_method = db.Column(db.String(80), unique=True, nullable=False)
    eluent_a_id = db.Column(UUID())
    eluent_b_id = db.Column(UUID())
    instrument_id = db.Column(UUID())
    column_id = db.Column(UUID())
    lod = db.Column(db.Integer())
    lloq = db.Column(db.Integer())
    uloq = db.Column(db.Integer())
    precision = db.Column(db.Integer())
    preferred_sample_volume = db.Column(db.Integer())
    runtime = db.Column(db.Integer())
    price = db.Column(db.Integer())

    def __init__(self, 
                id=None,
                name=None, 
                technique=None, 
                comment=None, 
                analysis_method=None,
                eluent_a_id=None,
                eluent_b_id=None,
                instrument_id=None,
                column_id=None,
                lod=0,
                lloq=0,
                uloq=0,
                precision=0,
                preferred_sample_volume=0,
                runtime=0,
                price=0):
        if not id:
            id = uuid4()
        self.id = id
        self.created_at = datetime.utcnow()
        self.last_modified_at = self.created_at
        self.name = name
        self.technique = technique
        self.comment = comment
        self.analysis_method = analysis_method
        self.eluent_a_id = eluent_a_id
        self.eluent_b_id = eluent_b_id
        self.instrument_id = instrument_id
        self.column_id = column_id
        self.lod = lod
        self.lloq = lloq
        self.uloq = uloq
        self.precision = precision
        self.preferred_sample_volume = preferred_sample_volume
        self.runtime = runtime
        self.price = price

    def __repr__(self):
        return "<Method %r>" % self.name
