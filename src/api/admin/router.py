from fastapi.routing import APIRouter
from fastapi import Depends, Body, Query, Header, Path
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession
from ...common.utils import get_db_session, validate_token
from .schemas import (
    FeatureFlag, FeatureFlagCreate, FeatureFlagPatch, FeatureFlagValueUpdate,
    TagType, Environment, IdGroup, TagValueCreate, NestedTagValue
)
from .db_interactions import (
    get_feature_flags,
    create_feature_flag,
    update_feature_flag,
    get_tag_types,
    create_tag_type,
    get_tag_values,
    create_tag_value,
    get_environments,
    create_environment,
    get_id_groups,
    create_id_group,
    update_feature_flag_value
)

router = APIRouter()

@router.get("/featureflags", response_model=list[FeatureFlag])
async def fetch_feature_flags(db: AsyncSession = Depends(get_db_session), x_tenant_id: UUID4 = Depends(validate_token)):
    feature_flags = await get_feature_flags(db, x_tenant_id)
    return feature_flags

@router.post("/featureflags", response_model=FeatureFlag)
async def post_feature_flag(db: AsyncSession = Depends(get_db_session), x_tenant_id: UUID4 = Depends(validate_token), feature_flag_obj: FeatureFlagCreate = Body()):
    feature_flag = await create_feature_flag(db, x_tenant_id, feature_flag_obj)
    return feature_flag

@router.patch("/featureflags/{feature_flag_id}", response_model=FeatureFlag)
async def modify_feature_flag(db: AsyncSession = Depends(get_db_session), x_tenant_id: UUID4 = Depends(validate_token), feature_flag_id: UUID4 = Path(), feature_flag_obj: FeatureFlagPatch = Body()):
    feature_flag = await update_feature_flag(db, x_tenant_id, feature_flag_id, feature_flag_obj)
    return feature_flag

@router.get("/tagtypes", response_model=list[TagType])
async def fetch_tag_types(db: AsyncSession = Depends(get_db_session), x_tenant_id: UUID4 = Depends(validate_token)):
    tag_types = await get_tag_types(db, x_tenant_id)
    return tag_types

@router.post("/tagtypes", response_model=TagType)
async def post_tag_type(db: AsyncSession = Depends(get_db_session), x_tenant_id: UUID4 = Depends(validate_token), tag_type_obj: TagType = Body()):
    tag_type = await create_tag_type(db, x_tenant_id, tag_type_obj)
    return tag_type

@router.get("/tagvalues", response_model=list[NestedTagValue])
async def fetch_tag_values(db: AsyncSession = Depends(get_db_session), x_tenant_id: UUID4 = Depends(validate_token), tag_type_id: UUID4 = Query(default=None)):
    tag_values = await get_tag_values(db, x_tenant_id, tag_type_id)
    return tag_values

@router.post("/tagvalues", response_model=NestedTagValue)
async def post_tag_value(db: AsyncSession = Depends(get_db_session), x_tenant_id: UUID4 = Depends(validate_token), tag_value_obj: TagValueCreate = Body()):
    tag_value = await create_tag_value(db, x_tenant_id, tag_value_obj)
    return tag_value

@router.get("/environments", response_model=list[Environment])
async def fetch_environments(db: AsyncSession = Depends(get_db_session), x_tenant_id: UUID4 = Depends(validate_token)):
    environments = await get_environments(db, x_tenant_id)
    return environments

@router.post("/environments", response_model=Environment)
async def post_environment(db: AsyncSession = Depends(get_db_session), x_tenant_id: UUID4 = Depends(validate_token), environment_obj: Environment = Body()):
    environment = await create_environment(db, x_tenant_id, environment_obj)
    return environment

@router.get("/idgroups", response_model=list[IdGroup])
async def fetch_id_groups(db: AsyncSession = Depends(get_db_session), x_tenant_id: UUID4 = Depends(validate_token)):
    id_groups = await get_id_groups(db, x_tenant_id)
    return id_groups

@router.post("/idgroups", response_model=IdGroup)
async def post_id_group(db: AsyncSession = Depends(get_db_session), x_tenant_id: UUID4 = Depends(validate_token), id_group_obj: IdGroup = Body()):
    id_group = await create_id_group(db, x_tenant_id, id_group_obj)
    return id_group

@router.patch("/featureflags/{feature_flag_id}/value", response_model=FeatureFlag)
async def change_feature_flag_value(db: AsyncSession = Depends(get_db_session), x_tenant_id: UUID4 = Depends(validate_token), feature_flag_id: UUID4 = Path(), environment_id: UUID4 = Query(), feature_flag_value_obj: FeatureFlagValueUpdate = Body()):
    feature_flag = await update_feature_flag_value(db, x_tenant_id, feature_flag_id, environment_id, feature_flag_value_obj)
    return feature_flag
