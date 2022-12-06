from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models.user import User
from app.schemas.donation import DonationCreate, DonationDB, DonationUserDB
from app.services.Investments import investmens

router = APIRouter()


@router.get(
    '/',
    summary='Получить список всех пожертвований',
    response_model=List[DonationDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session)
):
    '''Доступно только для авторизованных пользователей.'''
    all_donations = await donation_crud.get_multi(session)
    return all_donations


@router.get(
    '/my',
    summary='Получить список всех личных пожертвований',
    response_model=List[DonationUserDB],
    response_model_exclude_none=True,
    response_model_exclude={'user_id'}
)
async def get_all_current_user_donations(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    '''Доступно только для авторизованных пользователей.'''
    all_donations = await donation_crud.get_by_user(user, session)
    return all_donations


@router.post(
    '/',
    summary='Внести пожертвование',
    response_model_exclude_none=True,
    response_model=DonationUserDB
)
async def creat_donation(
    donation: DonationCreate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    '''
    Доступно только для авторизованных пользователей.
    Для пожертвования необходимо ввести:

    - **full_amount**: Сумму, которую хотите пожертвовать
    - **comment**: Комментарий (Опционально)
    '''
    new_donation = await donation_crud.create(donation, session, user)
    await investmens(session)
    await session.refresh(new_donation)
    return new_donation
