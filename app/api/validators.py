from http import HTTPStatus

from fastapi import HTTPException

from app.core.db import AsyncSession
from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject


async def check_project_exists(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    project = await charity_project_crud.get(project_id, session)
    if project is None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект не найден!'
        )
    return project


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession,
) -> None:
    project_id = await charity_project_crud.get_project_id_by_name(project_name, session)
    if project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def check_project_before_delete(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    project = await check_project_exists(project_id, session)
    project = await charity_project_crud.get(project_id, session)
    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!')
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )
    return project


async def check_project_before_update(
    project_id: int,
    object_in: CharityProject,
    session: AsyncSession
) -> CharityProject:
    project = await check_project_exists(project_id, session)
    if object_in.name is not None:
        await check_name_duplicate(object_in.name, session)
    project = await charity_project_crud.get(project.id, session)
    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!'
        )
    if object_in.full_amount and object_in.full_amount < project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Нельзя установить требуемую сумму меньше уже вложенной!'
        )
    return project
