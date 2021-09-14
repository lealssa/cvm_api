from fastapi import APIRouter, HTTPException, Query
import bson
from pymongo import MongoClient
from ..config import settings
from ..models.fi_diario_model import FiDiarioModel, FiAgregadoModel
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
    fi_diario = await db.cvm_fi_diario.find(mongo_qry, {'_id': 0, 'data': '$DT_COMPTC', 'vl_quota': '$VL_QUOTA'}).sort('DT_COMPTC').to_list(length=1000)

    if not fi_diario:
        raise HTTPException(status_code=404)

    return fi_diario

@router.get("/aggr", response_description="Pega registros agregados por mês e ano de um FI (pega o último dia do mês)", response_model=List[FiAgregadoModel])
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
    mongo_aggr = { "_id": { "ano": { "$year": "$DT_COMPTC" }, "mes": { "$month": "$DT_COMPTC" }}, "dia_ref": { "$last": "$DT_COMPTC" }, "vl_dia_ref": { "$last": "$VL_QUOTA" }  }
    mongo_proj = { "_id": 0, "ano": "$_id.ano", "mes": "$_id.mes", "dia_ref": 1, "vl_dia_ref": 1 }
    full_qry = [{ "$match": mongo_qry }, { "$group": mongo_aggr }, { "$sort" : { "_id.ano": 1, "_id.mes": 1 } }, { "$project": mongo_proj}]
    
    fi_aggr = await db.cvm_fi_diario.aggregate(full_qry).to_list(length=1000)

    if not fi_aggr:
        raise HTTPException(status_code=404)

    return fi_aggr


# TODO
# 1 - Falta estudar como agregar por mes de modo que pegue o valor do ultimo dia do mes - OK
# 2 - Alterar o cvm_extractor pra salvar o DT_COMPTC em Date - OK
# 3 - Ajustar a saida pra conseguir retornar em response_model - OK


# Estudar https://www.mongodb.com/developer/quickstart/python-quickstart-fastapi/
