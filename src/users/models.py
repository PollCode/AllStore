import sqlmodel as sm
import sqlalchemy as sa
from uuid import uuid4, UUID
from typing import List, Optional
from .enums import UserRole, Permission 
from ..common.models.api_base_model import ApiBaseModel

class Company(ApiBaseModel, table=True):
    __tablename__ = "companies"
    
    id: UUID = sm.Field(default_factory=uuid4, primary_key=True)
    name: str = sm.Field(index=True, unique=True)
    email: str = sm.Field(index=True, unique=True)
    description: str = sm.Field(nullable=True, max_length=255)
    is_active: bool = sm.Field(default=True)
    
    # Relaciones
    users: List["User"] = sm.Relationship(back_populates="company")
    roles: List["Role"] = sm.Relationship(back_populates="company")
    

class User(ApiBaseModel, table=True):
    __tablename__ = "users"
    
    id: UUID = sm.Field(default_factory=uuid4, primary_key=True)
    email: str = sm.Field(index=True, unique=True)
    username: str = sm.Field(index=True)
    password: str = sm.Field()
    is_active: bool = sm.Field(default=True)
    global_role: UserRole = sm.Field(default=UserRole.CUSTOMER)
    
    # Relación con compañía
    company_id: Optional[UUID] = sm.Field(default=None, foreign_key="companies.id")
    company: Optional[Company] = sm.Relationship(back_populates="users")
    
    # Relación con roles específicos
    user_roles: List["UserRoleAssignment"] = sm.Relationship(back_populates="user")
    
    
class Role(ApiBaseModel, table=True):
    __tablename__ = "roles"
    
    id: UUID = sm.Field(default_factory=uuid4, primary_key=True)
    name: str = sm.Field(index=True)
    description: str = sm.Field(nullable=True, max_length=255)
    permissions: List[Permission] = sm.Field(default=[], sa_column=sa.Column(sa.JSON))
    is_system_role: bool = sm.Field(default=False)
    
    # Relación con compañía
    company_id: UUID = sm.Field(foreign_key="companies.id")
    company: Company = sm.Relationship(back_populates="roles")
    
    # Relación con usuarios
    user_assignments: List["UserRoleAssignment"] = sm.Relationship(back_populates="role")
    
    
class UserRoleAssignment(ApiBaseModel, table=True):
    __tablename__ = "user_role_assignments"
    
    id: UUID = sm.Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = sm.Field(foreign_key="users.id")
    role_id: UUID = sm.Field(foreign_key="roles.id")
    company_id: UUID = sm.Field(foreign_key="companies.id")
    
    # Relaciones
    user: User = sm.Relationship(back_populates="user_roles")
    role: Role = sm.Relationship(back_populates="user_assignments")