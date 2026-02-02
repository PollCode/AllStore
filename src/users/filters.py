from fastapi import Query
from typing import Optional
from pydantic import EmailStr
from .schemas import CompanyFilterSchema

def get_company_filter(
    name: str | None = Query(None, description="Filter by name"),
    email: EmailStr | None = Query(None, description="Filter by email"),
    full_name: str | None = Query(None, description="Filter by full_name"),
    is_superuser: bool | None = Query(None, description="Filter by is_superuser"),
    is_active: Optional[bool] = Query(None, description="Filter by is_active"),
    sort_by: str | None = Query(None, description="Field for order"),
    sort_order: str = Query("asc", regex="^(asc|desc)$", description="Order direction")
):
    if all(v is None for v in locals().values()):
        return None
    return CompanyFilterSchema(**locals())