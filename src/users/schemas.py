from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime
from common.filters import BaseFilter

# Company Schemas
class CompanyResponse(BaseModel):
    id: UUID 
    name: str
    email: str
    description: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
       
class CompanyFilterSchema(BaseFilter):
    name: str | None = None
    email: str | None = None
    description: str | None = None
    is_active: bool | None = None
    name__contains: str | None = None
    email__contains: str | None = None
    sort_by: str | None = NotImplemented
    sort_order: str | None = None

class CreateCompanySchema(BaseModel):
    name: str
    email: EmailStr
    description: str | None 
    
class UpdateCompanySchema(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    description: str | None = None
    is_active: bool | None = None