import sqlmodel as sm
from datetime import datetime
from typing import Optional
from uuid import UUID
from sqlalchemy.exc import DataError, IntegrityError, NoResultFound
from common.pagination import PaginationParams
from common.services import BaseService
from .models import Company, User
from .schemas import *


class CompanyService(BaseService):
    
    def __init__(self, db: sm.Session):
        self.db = db
        super().__init__(db, Company)
    
    def get_companies_with_advanced_filters(
        self,
        name: str | None = None,
        email: str | None = None,
        created_after: Optional[datetime] = None,
        created_before: Optional[datetime] = None,
        pagination: Optional[PaginationParams] = None
    ):
        query = sm.select(self.model_class)
        
        conditions = []
        
        if name:
            conditions.append(self.model_class.name.contains(name))
        if email:
            conditions.append(self.model_class.email.contains(email))
        if created_after:
            conditions.append(self.model_class.created_at >= created_after)
        if created_before:
            conditions.append(self.model_class.created_at <= created_before)
        
        if conditions:
            query = query.where(sm.and_(*conditions))
        
        # Contar total
        count_query = sm.select(sm.func.count()).select_from(self.model_class)
        if conditions:
            count_query = count_query.where(sm.and_(*conditions))
        
        # Aplicar paginación
        if pagination:
            query = query.offset(pagination.skip).limit(pagination.limit)
        
        total = self.db.exec(count_query).one()
        items = self.db.exec(query).all()
        
        return items, total
    
    def get_company_by_id(self, id: UUID) -> CompanyResponse:
        try:
            company = self.db.get(self.model_class, id)
            
            if not company:
                raise NoResultFound
            
            return CompanyResponse(**company.model_dump())    
            
        except NoResultFound:
            raise ValueError('Company not found')
        except Exception as e:
            raise ValueError(f'Internal Server Error: {e}')
        
    def add_company(self, data: CreateCompanySchema) -> CompanyResponse:
        try:
            comp_data = data.model_dump()
            company = self.model_class(**comp_data)
            self.db.add(company)
            self.db.commit()
            self.db.refresh(company)
            
            return CompanyResponse(**company.model_dump())
        
        except IntegrityError:
            raise ValueError(f'Already exists company with this name or email')
            
        except Exception as e:
            raise ValueError(f'Internal Server Error: {e}')
        
    def edit_company(self, id: UUID, data: UpdateCompanySchema) -> CompanyResponse:
        try:
            comp = self.db.get(self.model_class, id)
            
            if not comp:
                raise NoResultFound
            
            for key, value in data.model_dump(exclude_unset=True).items():
                setattr(comp, key, value)
            
            comp.updated_at = datetime.now()
            self.db.commit()
            self.db.refresh(comp)
            
            return CompanyResponse(**comp.model_dump())
        
        except NoResultFound:
            raise ValueError(f'Company not found')
            
        except IntegrityError:
            raise ValueError(f'Already exists company with this name or email')
        
        except Exception as e:
            raise ValueError(f'Internal Server Error: {e}')
        
    
    def delete_company(self, id: UUID) -> None:
        try:
            comp = self.db.get(self.model_class, id)
            
            if not comp:
                raise NoResultFound
            
            self.db.delete(comp)
            self.db.commit()
            
            
        except NoResultFound:
            raise ValueError('Company not found')
        
        except Exception as e:
            raise ValueError(f'Internal Server Error: {e}')