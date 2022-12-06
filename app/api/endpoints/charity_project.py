from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_name_duplicate,
                                check_project_before_delete,
                                check_project_before_update)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.services.Investments import investmens

router = APIRouter()


@router.get(
    '/',
    summary='Получить список всех проектов',
    response_model_exclude_none=True,
    response_model=List[CharityProjectDB],
)
async def get_all_projects(
    session: AsyncSession = Depends(get_async_session)
):
    '''Получить список проектов может любоой пользователь'''
    projects = await charity_project_crud.get_multi(session)
    return projects


@router.post(
    '/',
    summary='Создать новый проект',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    response_model_exclude_none=True
)
async def create_new_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session)
):
    '''
    Только для суперюзеров.
    Для создания проекта необходимо ввести:

    - **name**: Название
    - **description**: Описание
    - **full_amount**: Сумму, которую необходимо собрать
    '''
    await check_name_duplicate(charity_project.name, session)
    new_project = await charity_project_crud.create(charity_project, session)
    await investmens(session)
    await session.refresh(new_project)
    return new_project


@router.patch(
    '/{project_id}',
    summary='Редактировать проект',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def partially_update_project(
    project_id: int,
    object_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Только для суперюзеров. Все поля опциональны.
    """
    db_object = await check_project_before_update(project_id, object_in, session)
    project = await charity_project_crud.update(db_object, object_in, session)
    return project


@router.delete(
    '/{project_id}',
    summary='Удалить проект',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def delete_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров."""
    project = await check_project_before_delete(project_id, session)
    project = await charity_project_crud.remove(project, session)
    return project
