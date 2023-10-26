from fastapi import FastAPI
import uvicorn
from app.routers import product
from app.db.database import Base,engine

from typing import Optional

def create_tables():
    Base.metadata.create_all(bind=engine)
create_tables()

app= FastAPI()
app.include_router(product.router)

if __name__ == '__main__':
    uvicorn.run('main:app',port=8000,reload=True)