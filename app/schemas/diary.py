from pydantic import BaseModel
from typing import Optional
from fastapi import Depends
from fastapi import Query as FastAPIQuery
from app.schemas.main_schem import RequestModel

class DiaryQuery(RequestModel):
    query: Optional[str] = None
    @classmethod
    def as_query(
        cls,
        query: Optional[str] = FastAPIQuery(None)
    ):
        return cls(query=query)