from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api.v1.schemas.group import (
    GroupCreate,
    GroupResponse,
    JoinGroupResponse,
    GroupListResponse,
    GroupMemberResponse,
)
from api.v1.services.group_service import GroupService
from api.v1.services.auth import get_db, get_current_user
from api.v1.models.user import User
from uuid import UUID
from typing import List

group = APIRouter(prefix="/groups", tags=["Groups"])


@group.post("/create_group", response_model=GroupResponse)
async def create_group(
    data: GroupCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):  
    return await GroupService.create_group(data, current_user, db)


@group.post("/{group_id}/join", response_model=JoinGroupResponse)
async def join_group(
    group_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await GroupService.join_group(group_id, current_user, db)


@group.get("/group_list", response_model=List[GroupListResponse])
async def get_all_groups(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await GroupService.list_groups(db)


@group.get("/{group_id}/members", response_model=List[GroupMemberResponse])
async def get_group_members(
    group_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await GroupService.get_group_members(group_id, db)


@group.get("/my_groups", response_model=List[GroupListResponse])
async def get_my_groups(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await GroupService.get_my_groups(current_user, db)


@group.post("/{group_id}/leave")
async def leave_group(
    group_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await GroupService.leave_group(group_id, current_user, db)


@group.delete("/{group_id}/members/{user_id}")
async def remove_member(
    group_id: UUID,
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await GroupService.remove_member(group_id, user_id, current_user, db)
