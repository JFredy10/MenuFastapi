import os
from fastapi import UploadFile
from pydantic import BaseModel

class ProductCreate(BaseModel):
    nombre: str
    descripcion: str
    precio: float
    imagen: UploadFile


class ProductUpdate(BaseModel):
    nombre: str
    descripcion: str
    precio: float
    imagen: UploadFile = None