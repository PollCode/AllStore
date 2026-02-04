import sqlmodel as sm
import fastapi as fa
from typing import Annotated, Optional
from uuid import UUID
from common.pagination import PaginatedResponse, PaginationParams
from core.database import get_session
from .schemas import CompanyResponse, CompanyFilterSchema, CreateCompanySchema, UpdateCompanySchema
from .filters import get_company_filter
from .services import CompanyService

router = fa.APIRouter(prefix='/users', tags=['Users'])

@router.get(
    '/companies', 
    response_model=PaginatedResponse[CompanyResponse], 
    status_code=fa.status.HTTP_200_OK)
async def read_companies(
    db: sm.Session = fa.Depends(get_session),
    pagination: PaginationParams = fa.Depends(),
    filters: Annotated[Optional[CompanyFilterSchema], fa.Depends(get_company_filter)] = None,
):
    try:
        service = CompanyService(db)
        filter_params = CompanyFilterSchema(**filters.model_dump())
        result = service.get_all_paginated(
            filter_params=filter_params,
            pagination=pagination,
            sort_by=filter_params.sort_by,
            sort_order=filter_params.sort_order
        )
        return result
    except Exception as e:
        raise fa.HTTPException(status_code=400, detail=f'{e}')

@router.get(
    '/companies/{id}',
    response_model=CompanyResponse,
    status_code=fa.status.HTTP_200_OK)
async def read_company_by_id(
     id: UUID,
     db: sm.Session = fa.Depends(get_session)
 ):
    try:
        service = CompanyService(db)
        return service.get_company_by_id(id)
    except Exception as e:
        raise fa.HTTPException(status_code=400, detail=f'{e}')
    
@router.post(
    '/companies', 
    response_model=CompanyResponse, 
    status_code=fa.status.HTTP_201_CREATED)
async def add_company(
    data: CreateCompanySchema,
    db: sm.Session = fa.Depends(get_session)
):
    try:
        service = CompanyService(db)
        return service.add_company(data)
    except Exception as e:
        raise fa.HTTPException(status_code=400, detail=f'{e}')
    
@router.put(
    '/companies/{id}',
    response_model=CompanyResponse,
    status_code=fa.status.HTTP_200_OK)
@router.patch(
    '/companies/{id}',
    response_model=CompanyResponse,
    status_code=fa.status.HTTP_200_OK)
async def edit_company(
    id: UUID,
    data: UpdateCompanySchema,
    db: sm.Session = fa.Depends(get_session)
):
    try:
        service = CompanyService(db)
        return service.edit_company(id, data)
    except Exception as e:
        raise fa.HTTPException(status_code=400, detail=f'{e}')
    
@router.delete(
    '/companies/{id}', 
    response_model=None, 
    status_code=fa.status.HTTP_204_NO_CONTENT)
async def delete_user(
    id: UUID, 
    db: sm.Session = fa.Depends(get_session)
):
    try:
        service = CompanyService(db)
        return service.delete_company(id)
    except Exception as e:
        raise fa.HTTPException(status_code=400, detail=f'{e}')