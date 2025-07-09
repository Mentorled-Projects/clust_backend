from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from api.v1.models.group import Group
from api.v1.models.user import User
from api.v1.schemas.group import GroupCreate
from uuid import UUID
from fastapi import HTTPException, status
from typing import List


class GroupService:
    @staticmethod
    async def create_group(data: GroupCreate, user: User, db: AsyncSession) -> Group:
        group = Group(
            name=data.name,
            description=data.description,
            is_private=data.is_private,
            organizer_id=user.id
        )
        group.members.append(user)
        db.add(group)
        await db.commit()
        await db.refresh(group)
        return group

    @staticmethod
    async def join_group(group_id: UUID, user: User, db: AsyncSession):
        result = await db.execute(
            select(Group)
            .options(selectinload(Group.members))  # eager load members to avoid lazy loading
            .where(Group.id == group_id)
        )
        group = result.scalar_one_or_none()

        if not group:
            raise HTTPException(status_code=404, detail="Group not found")

        if group.is_private:
            raise HTTPException(status_code=403, detail="This group is private. You must be invited.")

        if user in group.members:
            raise HTTPException(status_code=400, detail="You are already a member of this group")

        group.members.append(user)
        await db.commit()
        return {"message": "Joined group successfully"}
    

    @staticmethod
    async def list_groups(db: AsyncSession) -> List[Group]:
        result = await db.execute(select(Group))
        return result.scalars().all()

    @staticmethod
    async def get_group_members(group_id: UUID, db: AsyncSession) -> List[User]:
        result = await db.execute(select(Group).where(Group.id == group_id))
        group = result.scalar_one_or_none()
        if not group:
            raise HTTPException(status_code=404, detail="Group not found")
        return group.members

    @staticmethod
    async def get_my_groups(user: User, db: AsyncSession) -> List[Group]:
        # Assuming relationship is loaded or will be loaded by selectinload
        return user.member_groups

    @staticmethod
    async def leave_group(group_id: UUID, user: User, db: AsyncSession):
        result = await db.execute(select(Group).where(Group.id == group_id))
        group = result.scalar_one_or_none()
        if not group:
            raise HTTPException(status_code=404, detail="Group not found")

        if user not in group.members:
            raise HTTPException(status_code=400, detail="You are not a member of this group")

        group.members.remove(user)
        await db.commit()
        return {"message": "You have left the group"}

    @staticmethod
    async def remove_member(group_id: UUID, target_user_id: UUID, current_user: User, db: AsyncSession):
        result = await db.execute(select(Group).where(Group.id == group_id))
        group = result.scalar_one_or_none()
        if not group:
            raise HTTPException(status_code=404, detail="Group not found")

        if group.organizer_id != current_user.id:
            raise HTTPException(status_code=403, detail="Only the organizer can remove members")

        target_user_result = await db.execute(select(User).where(User.id == target_user_id))
        target_user = target_user_result.scalar_one_or_none()

        if not target_user or target_user not in group.members:
            raise HTTPException(status_code=404, detail="User not found in this group")

        group.members.remove(target_user)
        await db.commit()
        return {"message": f"{target_user.first_name} has been removed from the group"}
