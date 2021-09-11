from fastapi import FastAPI
from pydantic import BaseModel, Field


class CadFIModel(BaseModel):
    DENOM_SOCIAL: str = Field(...)
    CNPJ_FUNDO: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "DENOM_SOCIAL": "Fundo de Investimento XPTO",
                "CNPJ_FUNDO": "00.000.000/0000-00",
            }
        }