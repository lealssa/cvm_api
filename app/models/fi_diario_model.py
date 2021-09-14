from typing import List
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List
from datetime import date

class FiDiarioModel(BaseModel):
    data: date = Field(...)
    vl_quota: float = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "data": "2021-09-11",
                "vl_quota": 10.00
            }
        }        

class FiAgregadoModel(BaseModel):
    dia_ref: date = Field(...)
    vl_dia_ref: float = Field(...)
    ano: int = Field(...)
    mes: int = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "dia_ref": "2021-09-11",
                "vl_dia_ref": 10.00,
                "ano": 2021,
                "mes": 9
            }
        }