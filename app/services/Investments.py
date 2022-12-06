from datetime import datetime
from typing import Union

from app.core.db import AsyncSession
from app.crud import charity_project_crud, donation_crud
from app.models import CharityProject, Donation


async def close_object(object: Union[CharityProject, Donation]) -> None:
    object.close_date = datetime.now()
    object.fully_invested = True
    object.invested_amount = object.full_amount


async def investmens(session: AsyncSession):
    opend_projects = await charity_project_crud.get_opend_or_undistributed_objects(session)
    undistributed_donations = await donation_crud.get_opend_or_undistributed_objects(session)
    if not opend_projects or not undistributed_donations:
        return
    for project in opend_projects:
        for donation in undistributed_donations:
            left_to_invest = project.full_amount - project.invested_amount
            left_donation = donation.full_amount - donation.invested_amount
            difference = left_to_invest - left_donation
            if difference == 0:
                await close_object(project)
                await close_object(donation)
            if difference > 0:
                project.invested_amount += left_donation
                await close_object(donation)
            if difference < 0:
                donation.invested_amount = left_donation - abs(difference)
                await close_object(project)
    await session.commit()
