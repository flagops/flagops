from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from ..config import BaseSQLModel

class FeatureFlag(BaseSQLModel):
    __tablename__ = "feature_flags"

    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String(50))

