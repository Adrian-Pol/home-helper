from pydantic import Field,field_validator
from app.schemas.main_schem import RequestModel
from datetime import date, datetime

class MeasurmentQuery(RequestModel):
    waga: float = Field(...,ge=1)
    pas: int = Field(...,ge=1)
    posladek: int = Field(...,ge=1)
    klatka: int = Field(...,ge=1)
    udo_l: int = Field(...,ge=1)
    udo_p: int = Field(...,ge=1)
    lydka_l: int = Field(...,ge=1)
    lydka_p: int = Field(...,ge=1)
    entry_date: date = Field(...)

    @field_validator('entry_date',mode="before")
    def parse_date(cls,v):
        if isinstance (v,str):
            return datetime.strptime(v,"%d-%m-%y").date()
        return v