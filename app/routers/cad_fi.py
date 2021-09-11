from fastapi import APIRouter, HTTPException, Query
import bson
from pymongo import MongoClient
from ..config import settings
from ..models.cad_fi_model import CadFIModel
from ..db import client
from typing import List

db = client[settings.cvm_mongodb_db_name]

router = APIRouter(
    prefix="/api/v1/fi/cad",
    tags=["cadastro_fi"],
    responses={404: {"description": "Not found"}}
)

@router.get("/nome/", response_description="Pega um, ou mais, cadastros FI pelo nome", response_model=List[CadFIModel])
async def read_cad_fis_by_nome(
    q: str = Query(
        ...,
        title="Query string",
        description="Nome do FI a buscar (entre aspas duplas)",
        min_length=3,
        regex='^"[^"]+"$'
    )
    ):
    with MongoClient(settings.cvm_mongodb_url) as client:
        fis = await db.cvm_cad_fi.find({'$text': { '$search': q }}, {'_id': 0, 'CNPJ_FUNDO': 1, 'DENOM_SOCIAL': 1}).to_list(length=1000)

    if not fis:
        raise HTTPException(status_code=404) 
    
    return fis

@router.get("/cnpj/", response_description="Pega um cadastro FI pelo CNPJ", response_model=CadFIModel)
async def read_cad_fis_by_cnpj(
    q: str = Query(
        ...,
        title="Query string",
        description="CNPJ do FI a buscar no formato 00.000.000/0000-00",
        min_length=18,
        max_length=18,
        regex='^\d{2}\.\d{3}\.\d{3}\/\d{4}\-\d{2}$'
    )
    ):
    fi = await db.cvm_cad_fi.find_one({'CNPJ_FUNDO': q}, {'_id': 0, 'CNPJ_FUNDO': 1, 'DENOM_SOCIAL': 1})

    if not fi:
        raise HTTPException(status_code=404)

    return fi

    # Estudar https://www.mongodb.com/developer/quickstart/python-quickstart-fastapi/