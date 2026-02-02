import sqlmodel as sm
from datetime import datetime
from sqlalchemy import func

class ApiBaseModel(sm.SQLModel):
    created_at: datetime | None = sm.Field(default_factory=lambda: datetime.now())
    created_by: str | None = sm.Field(default=None)
    updated_at: datetime | None = sm.Field(
        default_factory=lambda: datetime.now(),  # Valor inicial
        sa_column_kwargs={"onupdate": func.now()}  # Actualización automática
    )
    updated_by: str | None = sm.Field(default=None)