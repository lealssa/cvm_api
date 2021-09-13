from fastapi import APIRouter, HTTPException, Query
import bson
from pymongo import MongoClient
from ..config import settings
from ..models.fi_diario_model import FiDiarioModel
from ..db import client
from typing import List
from datetime import datetime, date

db = client[settings.cvm_mongodb_db_name]

router = APIRouter(
    prefix="/api/v1/fi/diario",
    tags=["fi_diario"],
    responses={404: {"description": "Not found"}}
)

@router.get("/", response_description="Pega registros diarios de um FI", response_model=List[FiDiarioModel])
async def read_fi_diario_by_cnpj(
    q: str = Query(
        ...,
        title="Query string",
        description="CNPJ do FI a buscar no formato 00.000.000/0000-00",
        min_length=18,
        max_length=18,
        regex='^\d{2}\.\d{3}\.\d{3}\/\d{4}\-\d{2}$'
    ),
    dt_init: date = Query(
        ...,
        title="Data Inicial",
        description="Data inicial dos registros no formato ISO 8601"
    ),
    dt_end: date = Query(
        date.today(),
        title="Data Final (opcional)",
        description="Data final dos registros no formato ISO 8601"
    )
    ):    
    mongo_qry = {'$and': [ { 'CNPJ_FUNDO': q }, { 'DT_COMPTC': { '$gte': datetime.combine(dt_init, datetime.min.time()) } }, { 'DT_COMPTC': { '$lte': datetime.combine(dt_end, datetime.min.time()) } } ]}
    fi_diario = await db.cvm_fi_diario.find(mongo_qry, {'_id': 0, 'DT_COMPTC': 1, 'VL_QUOTA': 1}).sort('DT_COMPTC').to_list(length=1000)

    if not fi_diario:
        raise HTTPException(status_code=404)

    return fi_diario

@router.get("/aggr", response_description="Pega registros mensais de um FI")
async def read_fi_diario_by_cnpj(
    q: str = Query(
        ...,
        title="Query string",
        description="CNPJ do FI a buscar no formato 00.000.000/0000-00",
        min_length=18,
        max_length=18,
        regex='^\d{2}\.\d{3}\.\d{3}\/\d{4}\-\d{2}$'
    ),
    dt_init: date = Query(
        ...,
        title="Data Inicial",
        description="Data inicial dos registros no formato ISO 8601"
    ),
    dt_end: date = Query(
        date.today(),
        title="Data Final (opcional)",
        description="Data final dos registros no formato ISO 8601"
    )
    ):    
    mongo_qry = {'$and': [ { 'CNPJ_FUNDO': q }, { 'DT_COMPTC': { '$gte': datetime.combine(dt_init, datetime.min.time()) } }, { 'DT_COMPTC': { '$lte': datetime.combine(dt_end, datetime.min.time()) } } ]}
    mongo_aggr = [{ "$match": mongo_qry }, { "$group": { "_id": { "mes": { "$substr": ["$DT_COMPTC", 0, 7] }}, "vl_medio": { "$avg": "$VL_QUOTA" } } }]
    fi_mensal = await db.cvm_fi_diario.aggregate(mongo_aggr).to_list(length=1000)

    if not fi_mensal:
        raise HTTPException(status_code=404)

    return fi_mensal


# TODO
# 1 - Falta estudar como agregar por mes de modo que pegue o valor do ultimo dia do mes
# 2 - Alterar o cvm_extractor pra salvar o DT_COMPTC em Date - OK
# 3 - Ajustar a saida pra conseguir retornar em response_model


# Estudar https://www.mongodb.com/developer/quickstart/python-quickstart-fastapi/
