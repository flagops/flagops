from pydantic import UUID4
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from ...common.featureflags.models import (
    FeatureFlag as FeatureFlagModel, TagValue as TagValueModel,
    FeatureFlagTagValueThrough as FeatureFlagTagValueThroughModel,
    FeatureFlagValue as FeatureFlagValueModel,
    TagType as TagTypeModel, Environment as EnvironmentModel,
    TagValue as TagValueModel,
    IdGroup as IdGroupModel
)
from .schemas import (
    FeatureFlag as FeatureFlagSchema, FeatureFlagCreate, FeatureFlagPatch, FeatureFlagValueUpdate,
    TagType as TagTypeSchema, Environment as EnvironmentSchema,
    NestedTagValue as TagValueSchema, TagValueCreate,
    IdGroup as IdGroupSchema
)

def _get_feature_flag_joins():
    return (
        joinedload(FeatureFlagModel.tags).joinedload(FeatureFlagTagValueThroughModel.tag_value).joinedload(TagValueModel.tag_type),
        joinedload(FeatureFlagModel.values).joinedload(FeatureFlagValueModel.environment)
    )

async def get_feature_flags(db: AsyncSession, tenant_id: UUID4) -> list[FeatureFlagSchema]:
    stmt = select(FeatureFlagModel).where(FeatureFlagModel.tenant_id==tenant_id)\
        .options(*_get_feature_flag_joins())\
        .order_by(FeatureFlagModel.name.asc())
    feature_flags_orm = (await db.execute(stmt)).unique().scalars()
    feature_flags = [FeatureFlagSchema.from_orm(f) for f in feature_flags_orm]
    return feature_flags

async def get_feature_flag_by_id(db: AsyncSession, tenant_id: UUID4, feature_flag_id: UUID4) -> FeatureFlagSchema:
    stmt = select(FeatureFlagModel)\
        .options(*_get_feature_flag_joins())\
        .where(
            FeatureFlagModel.id==feature_flag_id,
            FeatureFlagModel.tenant_id==tenant_id
        )
    feature_flag_orm_obj = (await db.execute(stmt)).scalar()
    return FeatureFlagSchema.from_orm(feature_flag_orm_obj)

async def create_feature_flag(db: AsyncSession, tenant_id: UUID4, feature_flag_obj: FeatureFlagCreate) -> FeatureFlagSchema:
    obj = feature_flag_obj.dict()
    obj.pop("tags", None)
    feature_flag_model = FeatureFlagModel(
        **obj, tenant_id=tenant_id,
        tags=[
            FeatureFlagTagValueThroughModel(
                tag_value_id=t,
                tenant_id=tenant_id
            ) for t in feature_flag_obj.tags
        ]
    )
    async with db.begin():
        db.add_all([
            feature_flag_model
        ])
    feature_flag = await get_feature_flag_by_id(db, tenant_id, feature_flag_model.id)
    return feature_flag

async def update_feature_flag(db: AsyncSession, tenant_id: UUID4, feature_flag_id: UUID4, feature_flag_obj: FeatureFlagPatch) -> FeatureFlagSchema:
    # tags = feature_flag_obj.pop("tags", None)
    obj = feature_flag_obj.dict()
    obj.pop("tags", None)
    async with db.begin():
        stmt = update(FeatureFlagModel)\
            .where(FeatureFlagModel.id==feature_flag_id, FeatureFlagModel.tenant_id==tenant_id)\
            .values(**obj)
        await db.execute(stmt)
        if feature_flag_obj.tags:
            stmt = delete(FeatureFlagTagValueThroughModel).where(FeatureFlagTagValueThroughModel.feature_flag_id==feature_flag_id)
            await db.execute(stmt)
            db.add_all([
                FeatureFlagTagValueThroughModel(feature_flag_id=feature_flag_id, tenant_id=tenant_id, tag_value_id=t) for t in feature_flag_obj.tags
            ])
    feature_flag = await get_feature_flag_by_id(db, tenant_id, feature_flag_id)
    return feature_flag

async def get_tag_types(db: AsyncSession, tenant_id: UUID4) -> list[TagTypeSchema]:
    stmt = select(TagTypeModel).where(TagTypeModel.tenant_id==tenant_id).order_by(TagTypeModel.name.asc())
    tag_types_orm = (await db.execute(stmt)).scalars()
    tag_types = [TagTypeSchema.from_orm(f) for f in tag_types_orm]
    return tag_types

async def create_tag_type(db: AsyncSession, tenant_id: UUID4, tag_type_obj: TagTypeSchema)->TagTypeSchema:
    async with db.begin():
        db.add_all([
            TagTypeModel(**tag_type_obj.dict(), tenant_id=tenant_id)
        ])
    stmt = select(TagTypeModel).where(TagTypeModel.name==tag_type_obj.name, TagTypeModel.tenant_id==tenant_id)
    tag_type = (await db.execute(stmt)).scalar()
    return TagTypeSchema.from_orm(tag_type)

async def get_tag_values(db: AsyncSession, tenant_id: UUID4, tag_type_id: UUID4 = None) -> list[TagValueSchema]:
    stmt = select(TagValueModel).where(TagValueModel.tenant_id==tenant_id).options(joinedload(TagValueModel.tag_type))
    if tag_type_id:
        stmt = stmt.where(TagValueModel.tag_type_id==tag_type_id)
    stmt = stmt.order_by(TagValueModel.value.asc())
    tag_values_orm = (await db.execute(stmt)).scalars()
    tag_values = [TagValueSchema.from_orm(f) for f in tag_values_orm]
    return tag_values

async def create_tag_value(db: AsyncSession, tenant_id: UUID4, tag_value_obj: TagValueCreate)->TagValueSchema:
    tag_value_model = TagValueModel(**tag_value_obj.dict(), tenant_id=tenant_id)
    async with db.begin():
        db.add_all([
            tag_value_model
        ])
    stmt = select(TagValueModel).where(TagValueModel.id==tag_value_model.id, TagValueModel.tenant_id==tenant_id).options(joinedload(TagValueModel.tag_type))
    tag_value = (await db.execute(stmt)).scalar()
    return TagValueSchema.from_orm(tag_value)

async def get_environments(db: AsyncSession, tenant_id: UUID4) -> list[EnvironmentSchema]:
    stmt = select(EnvironmentModel).where(EnvironmentModel.tenant_id==tenant_id).order_by(EnvironmentModel.name.asc())
    environments_orm = (await db.execute(stmt)).scalars()
    environments = [EnvironmentSchema.from_orm(f) for f in environments_orm]
    return environments

async def create_environment(db: AsyncSession, tenant_id: UUID4, environment_obj: EnvironmentSchema)->EnvironmentSchema:
    async with db.begin():
        db.add_all([
            EnvironmentModel(**environment_obj.dict(), tenant_id=tenant_id)
        ])
    stmt = select(EnvironmentModel).where(EnvironmentModel.name==environment_obj.name, EnvironmentModel.tenant_id==tenant_id)
    environment_orm_obj = (await db.execute(stmt)).scalar()
    return EnvironmentSchema.from_orm(environment_orm_obj)

async def get_id_groups(db: AsyncSession, tenant_id: UUID4) -> list[IdGroupSchema]:
    stmt = select(IdGroupModel).where(IdGroupModel.tenant_id==tenant_id)
    id_groups_orm = (await db.execute(stmt)).scalars()
    id_groups = [IdGroupSchema.from_orm(f) for f in id_groups_orm]
    return id_groups

async def create_id_group(db: AsyncSession, tenant_id: UUID4, id_group_obj: IdGroupSchema)->IdGroupSchema:
    async with db.begin():
        db.add_all([
            IdGroupModel(**id_group_obj.dict(), tenant_id=tenant_id)
        ])
    stmt = select(IdGroupModel).where(IdGroupModel.name==id_group_obj.name, IdGroupModel.tenant_id==tenant_id).order_by(IdGroupModel.name.asc())
    id_group_orm_obj = (await db.execute(stmt)).scalar()
    return IdGroupSchema.from_orm(id_group_orm_obj)

async def update_feature_flag_value(db: AsyncSession, tenant_id: UUID4, feature_flag_id: UUID4, environment_id: UUID4, feature_flag_value_obj: FeatureFlagValueUpdate)->FeatureFlagSchema:
    async with db.begin():
        stmt = select(FeatureFlagValueModel).where(FeatureFlagValueModel.feature_flag_id==feature_flag_id, FeatureFlagValueModel.environment_id==environment_id, FeatureFlagValueModel.tenant_id==tenant_id)
        feature_flag_value_orm_obj = (await db.execute(stmt)).scalar()
        if feature_flag_value_orm_obj is None:
            db.add(FeatureFlagValueModel(feature_flag_id=feature_flag_id, environment_id=environment_id, **feature_flag_value_obj.dict(), tenant_id=tenant_id))
        else:
            update_stmt = update(FeatureFlagValueModel)\
                .where(FeatureFlagValueModel.feature_flag_id==feature_flag_id, FeatureFlagValueModel.environment_id==environment_id, FeatureFlagValueModel.tenant_id==tenant_id)\
                .values(**feature_flag_value_obj.dict())
            await db.execute(update_stmt)
    
    feature_flag = await get_feature_flag_by_id(db, tenant_id, feature_flag_id)
    return feature_flag
