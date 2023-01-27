import uuid
from sqlalchemy import Column, String, Boolean, ForeignKey, Integer, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from ..config import BaseSQLModel

class FeatureFlag(BaseSQLModel):
    __tablename__ = "feature_flags"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), nullable=False)
    description = Column(Text(), nullable=True)

    tags = relationship("FeatureFlagTagValueThrough", back_populates="feature_flag", lazy="select")
    values = relationship("FeatureFlagValue", back_populates="feature_flag", lazy="select")

    __table_args__ = (
        UniqueConstraint("tenant_id", "name", name="_flagname_tenant_id_unique_together"),
    )

class TagType(BaseSQLModel):
    __tablename__ = "tag_types"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), nullable=False)

    tag_values = relationship("TagValue", back_populates="tag_type", lazy="select")

    __table_args__ = (
        UniqueConstraint("tenant_id", "name", name="_tagname_tenant_id_unique_together"),
    )

class FeatureFlagTagValueThrough(BaseSQLModel):
    __tablename__ = "feature_flag_tag_value_through"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    feature_flag_id = Column(ForeignKey("feature_flags.id"), nullable=False)
    tag_value_id = Column(ForeignKey("tag_values.id"), nullable=False)

    feature_flag = relationship("FeatureFlag", back_populates="tags")
    tag_value = relationship("TagValue", back_populates="feature_flags")

    __table_args__ = (
        UniqueConstraint("feature_flag_id", "tag_value_id", name="_feature_flag_tag_value_unique_together"),
    )

class TagValue(BaseSQLModel):
    __tablename__ = "tag_values"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tag_type_id = Column(ForeignKey("tag_types.id"), nullable=False)

    tag_type = relationship("TagType", back_populates="tag_values", lazy="select")
    feature_flags = relationship("FeatureFlagTagValueThrough", back_populates="tag_value", lazy="select")

    value = Column(String(100), nullable=False)

    __table_args__ = (
        UniqueConstraint("tag_type_id", "value", name="_tag_type_value_unique_together"),
    )

class Environment(BaseSQLModel):
    __tablename__ = "environments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), nullable=False)

    values = relationship("FeatureFlagValue", back_populates="environment", lazy="select")

    __table_args__ = (
        UniqueConstraint("tenant_id", "name", name="_envname_tenant_id_unique_together"),
    )

class FeatureFlagValue(BaseSQLModel):
    __tablename__ = "feature_flag_values"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    feature_flag_id = Column(ForeignKey("feature_flags.id"), nullable=False)
    environment_id = Column(ForeignKey("environments.id"), nullable=False)
    enabled = Column(Boolean, default=False, nullable=False)
    rollout_percent = Column(Integer, default=100, nullable=True)
    enabled_only_for_ids = Column(ARRAY(String(50)), default=list, nullable=False)
    enabled_only_for_id_groups = Column(ARRAY(UUID(as_uuid=True)), default=list, nullable=False)

    feature_flag = relationship("FeatureFlag", back_populates="values", lazy="select")
    environment = relationship("Environment", back_populates="values", lazy="select")

    __table_args__ = (
        UniqueConstraint("feature_flag_id", "environment_id", name="_feature_flag_environment_unique_together"),
    )

class IdGroup(BaseSQLModel):
    __tablename__ = "id_groups"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), nullable=False)
    id_list = Column(ARRAY(String(50)), default=list, nullable=False)

    __table_args__ = (
        UniqueConstraint("tenant_id", "name", name="_idgroupname_tenant_id_unique_together"),
    )
