from datetime import datetime
from uuid import uuid4

from app.extensions import db
from sqlalchemy.dialects.postgresql import UUID

class Method(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    iupac = db.Column(db.String(80), unique=True, nullable=False)

    def __init__(self, id=None, name=None, iupac=None):
        if not id:
            id = uuid4()
        self.id = id
        self.created_at = datetime.utcnow()
        self.last_modified_at = self.created_at
        self.name = name
        self.iupac = iupac

    def __repr__(self):
        return "<Method %r>" % self.name
