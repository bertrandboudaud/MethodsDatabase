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

    def __init__(self, 
                id=None,
                name=None, 
                technique=None, 
                comment=None, 
                analysis_method=None,
                eluent_a_id=None,
                eluent_b_id=None,
                instrument_id=None,
                column_id=None):
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

    def __repr__(self):
        return "<Method %r>" % self.name
