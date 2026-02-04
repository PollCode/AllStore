import sqlmodel as sm
import fastapi as fa
from typing import Annotated, Optional
from common.pagination import PaginatedResponse, PaginationParams
from core.database import get_session
from .schemas import CompanyResponse, CompanyFilterSchema
from .filters import get_company_filter
from .services import CompanyService

router = fa.APIRouter(prefix='/users', tags=['Users'])

@router.get('/companies', response_model=PaginatedResponse[CompanyResponse], status_code=fa.status.HTTP_200_OK)
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