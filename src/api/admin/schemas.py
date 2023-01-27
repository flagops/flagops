from typing import Optional
from pydantic import BaseModel, Field, UUID4
from collections import namedtuple

class TagType(BaseModel):
    id: Optional[UUID4]
    name: str

    class Config:
        orm_mode = True

class TagValueCreate(BaseModel):
    id: Optional[UUID4]
    tag_type_id: UUID4 = Field(alias="tag_type")
    value: str
    
    class Config:
        orm_mode = True

class NestedTagValue(BaseModel):
    id: UUID4
    tag_type: TagType
    value: str
    
    class Config:
        orm_mode = True

class FeatureFlagCreate(BaseModel):
    id: Optional[UUID4]
    name: str
    description: Optional[str]
    tags: Optional[list[UUID4]]

class FeatureFlagPatch(BaseModel):
    name: Optional[str]
    description: Optional[str]
    tags: Optional[list[UUID4]]

class Environment(BaseModel):
    id: Optional[UUID4]
    name: str

    class Config:
        orm_mode = True

class FeatureFlagValueUpdate(BaseModel):
    enabled: Optional[bool]
    rollout_percent: Optional[int]
    enabled_only_for_ids: Optional[list[str]]
    enabled_only_for_id_groups: Optional[list[str]]

class IdGroup(BaseModel):
    id: UUID4
    name: str
    id_list: list[str]
    
    class Config:
        orm_mode = True

class FeatureFlagValue(BaseModel):
    id: UUID4
    feature_flag: UUID4 = Field(alias="feature_flag_id")
    environment: Environment
    enabled: bool
    rollout_percent: int
    enabled_only_for_ids: list[str] = []
    enabled_only_for_ids_groups: list[IdGroup] = []

    class Config:
        orm_mode = True

class FeatureFlag(BaseModel):
    id: UUID4
    name: str
    description: str
    tags: list[NestedTagValue]
    values: list[FeatureFlagValue]

    class Config:
        orm_mode = True
    
    @classmethod
    def from_orm(cls, obj):
        # obj.tags = [t.tag_value for t in obj.tags]
        keys = FeatureFlag.__fields__.keys()
        FeatureFlagTemp = namedtuple("FeatureFlagTemp", keys)
        new_obj = FeatureFlagTemp(*[getattr(obj, key) if key != "tags" else [t.tag_value for t in obj.tags] for key in keys])
        return super().from_orm(new_obj)
