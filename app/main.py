from fastapi import FastAPI
from .routers import cad_fi

app = FastAPI(
    title="CVM API",
    description="API de acesso aos dados da CVM",
    version="0.0.1",
    contact={
        "name": "Tiago S. Leal",
        "email": "tiagoleal.ssa@gmail.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://spdx.org/licenses/MIT.html",
    },    

)

app.include_router(cad_fi.router)
