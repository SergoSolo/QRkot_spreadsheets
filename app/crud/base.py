from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


class CRUDBase:

    def __init__(self, model):
        self.model = model

    async def get(
        self,
        object_id: int,
        session: AsyncSession
    ):
        db_object = await session.execute(
            select(self.model).where(
                self.model.id == object_id
            )
        )
        return db_object.scalars().first()

    async def get_multi(
            self,
            session: AsyncSession
    ):
        db_objects = await session.execute(select(self.model))
        return db_objects.scalars().all()

    async def create(
        self,
        object_in,
        session: AsyncSession,
        user: Optional[User] = None
    ):
        object_in_data = object_in.dict()
        if user is not None:
            object_in_data['user_id'] = user.id
        db_object = self.model(**object_in_data)
        session.add(db_object)
        await session.commit()
        await session.refresh(db_object)
        return db_object

    async def update(
            self,
            db_object,
            object_in,
            session: AsyncSession,
    ):
        object_data = jsonable_encoder(db_object)
        update_data = object_in.dict(exclude_unset=True)
        for field in object_data:
            if field in update_data:
                setattr(db_object, field, update_data[field])
        session.add(db_object)
        await session.commit()
        await session.refresh(db_object)
        return db_object

    async def remove(
            self,
            db_object,
            session: AsyncSession,
    ):
        await session.delete(db_object)
        await session.commit()
        return db_object

    async def get_opend_or_undistributed_objects(
        self,
        session: AsyncSession
    ):
        projects = await session.execute(
            select(self.model).where(
                self.model.full_amount > self.model.invested_amount
            ).order_by(self.model.create_date)
        )
        return projects.scalars().all()
