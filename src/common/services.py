import math
from typing import Type, TypeVar, Generic, Optional, List, Any, Dict
from sqlmodel import Session, select, func, and_, or_
from sqlmodel.sql.expression import Select
from .pagination import PaginationParams
from .filters import BaseFilter


T = TypeVar('T')

class BaseService(Generic[T]):
    def __init__(self, session: Session, model_class: Type[T]):
        self.session = session
        self.model_class = model_class
    
    def _apply_filters(self, query: Select, filters: Dict[str, Any]) -> Select:
        """Aplica filtros dinámicos a la consulta"""
        conditions = []
        
        for key, value in filters.items():
            if value is None:
                continue
                
            # Manejo de operadores especiales
            if '__contains' in key:
                field_name = key.replace('__contains', '')
                field = getattr(self.model_class, field_name, None)
                if field:
                    conditions.append(field.contains(value))
            elif '__gt' in key:
                field_name = key.replace('__gt', '')
                field = getattr(self.model_class, field_name, None)
                if field:
                    conditions.append(field > value)
            elif '__lt' in key:
                field_name = key.replace('__lt', '')
                field = getattr(self.model_class, field_name, None)
                if field:
                    conditions.append(field < value)
            elif '__gte' in key:
                field_name = key.replace('__gte', '')
                field = getattr(self.model_class, field_name, None)
                if field:
                    conditions.append(field >= value)
            elif '__lte' in key:
                field_name = key.replace('__lte', '')
                field = getattr(self.model_class, field_name, None)
                if field:
                    conditions.append(field <= value)
            elif '__in' in key:
                field_name = key.replace('__in', '')
                field = getattr(self.model_class, field_name, None)
                if field and isinstance(value, list):
                    conditions.append(field.in_(value))
            else:
                # Filtro exacto
                field = getattr(self.model_class, key, None)
                if field:
                    conditions.append(field == value)
        
        if conditions:
            query = query.where(and_(*conditions))
        
        return query
    
    def _apply_sorting(self, query: Select, sort_by: Optional[str] = None, 
                      sort_order: str = "asc") -> Select:
        """Aplica ordenamiento a la consulta"""
        if sort_by:
            field = getattr(self.model_class, sort_by, None)
            if field:
                if sort_order.lower() == "desc":
                    query = query.order_by(field.desc())
                else:
                    query = query.order_by(field.asc())
        return query
    
    def get_all_paginated(self, 
                         filter_params: Optional[BaseFilter] = None,
                         pagination: Optional[PaginationParams] = None,
                         sort_by: Optional[str] = None,
                         sort_order: str = "asc") -> Dict[str, Any]:
        """Obtiene todos los registros con paginación y filtros"""
        
        # Valores por defecto
        if pagination is None:
            pagination = PaginationParams(page=1, page_size=10)
        
        # Consulta para contar total
        count_query = select(func.count()).select_from(self.model_class)
        
        # Consulta para obtener datos
        data_query = select(self.model_class)
        
        # Aplicar filtros si existen
        if filter_params:
            filters = filter_params.get_filter_dict()
            count_query = self._apply_filters(count_query, filters)
            data_query = self._apply_filters(data_query, filters)
        
        # Aplicar ordenamiento
        data_query = self._apply_sorting(data_query, sort_by, sort_order)
        
        # Aplicar paginación
        data_query = data_query.offset(pagination.skip).limit(pagination.limit)
        
        # Ejecutar consultas
        total = self.session.exec(count_query).one()
        items = self.session.exec(data_query).all()
        
        # Calcular metadatos de paginación
        total_pages = math.ceil(total / pagination.page_size) if pagination.page_size > 0 else 0
        
        return {
            "data": items,
            "total": total,
            "page": pagination.page,
            "page_size": pagination.page_size,
            "total_pages": total_pages,
            "has_next": pagination.page < total_pages,
            "has_prev": pagination.page > 1
        }
    
    def get_by_filters(self, 
                      filter_params: BaseFilter,
                      sort_by: Optional[str] = None,
                      sort_order: str = "asc") -> List[T]:
        """Obtiene registros por filtros sin paginación"""
        query = select(self.model_class)
        
        filters = filter_params.get_filter_dict()
        query = self._apply_filters(query, filters)
        query = self._apply_sorting(query, sort_by, sort_order)
        
        return self.session.exec(query).all()