from uuid import UUID
from pydantic import BaseModel
from datetime import datetime

class BaseFilter(BaseModel):
    id: UUID | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    
    # Métodos para construir filtros dinámicos
    def get_filter_dict(self):
        """Retorna un diccionario con los filtros no nulos"""
        return {k: v for k, v in self.model_dump().items() if v is not None}