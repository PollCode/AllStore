from fastapi import Query
from typing import Optional
from pydantic import EmailStr
from .schemas import CompanyFilterSchema

def get_company_filter(
    name: str | None = Query(None, description="Filter by name"),
    email: EmailStr | None = Query(None, description="Filter by email"),
    is_active: Optional[bool] = Query(None, description="Filter by is_active"),
    sort_by: str | None = Query(None, description="Field for order"),
    sort_order: str = Query("asc", pattern="^(asc|desc)$", description="Order direction")
):
    if all(v is None for v in locals().values()):
        return None
    return CompanyFilterSchema(**locals())