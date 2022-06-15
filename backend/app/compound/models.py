from datetime import datetime
from uuid import uuid4

from app.extensions import db
from sqlalchemy.dialects.postgresql import UUID

class Compound(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    iupac = db.Column(db.String(80), unique=True, nullable=False)
    method_id = db.Column(UUID())

    def __init__(self, id=None, name=None, iupac=None, method_id=None):
        if not id:
            id = uuid4()
        self.id = id
        self.created_at = datetime.utcnow()
        self.last_modified_at = self.created_at
        self.name = name
        self.iupac = iupac
        self.method_id = method_id

    def __repr__(self):
        return "<Compound %r>" % self.name
