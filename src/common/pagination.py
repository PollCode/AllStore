from pydantic import BaseModel, Field
from pydantic.generics import GenericModel
from typing import TypeVar, Generic, List
from fastapi import Query

T = TypeVar('T')


class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1, description="Page number")
    page_size: int = Field(default=10, ge=1, le=100, description="Page size")
    
    @property
    def skip(self):
        return (self.page - 1) * self.page_size
    
    @property
    def limit(self):
        return self.page_size

class PaginatedResponse(GenericModel, Generic[T]):
    data: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool