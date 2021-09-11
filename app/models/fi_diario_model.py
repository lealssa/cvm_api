from typing import List
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List
from datetime import date

class FiDiarioModel(BaseModel):
    DT_COMPTC: date = Field(...)
    VL_QUOTA: float = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "DT_COMPTC": "2021-09-11",
                "VL_QUOTA": 10.00
            }
        }        