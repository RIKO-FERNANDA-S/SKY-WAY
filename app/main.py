from fastapi import FastAPI
from app.api.routes import router


app = FastAPI(
    tittle="VTOL Backend API",
    version="1.0.0",
    description="Backend skywa VTOL Competition"
)

app.include_router(router)