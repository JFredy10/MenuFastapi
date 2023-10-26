from fastapi import APIRouter, Depends, Request, UploadFile
from fastapi.responses import HTMLResponse
from app.schemas import ProductCreate, ProductUpdate
from app.db.database import SessionLocal
from sqlalchemy.orm import Session
from app.db.models import Product
from app.db.database import get_db
from templates import templates
import os

router = APIRouter(
    prefix="/product",
    tags=["Products"]
)

@router.get("/", response_class=HTMLResponse)
def index(request: Request, db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return templates.TemplateResponse("index.html", {"request": request, "products": products})

@router.get("/page_principal", response_class=HTMLResponse)
def page_principal(request: Request):
    return templates.TemplateResponse("page_principal.html", {"request": request})

@router.post("/create")
async def create(product: ProductCreate, db: Session = Depends(get_db)):
    if db.query(Product).filter_by(imagen=product.imagen.filename).first():
        return {"message": "El nombre de la imagen ya está en uso"}

    imagen_nombre = product.imagen.filename
    imagen_path = f"static/archivos/{imagen_nombre}"
    with open(imagen_path, "wb") as f:
        f.write(await product.imagen.read())

    product_data = Product(
        imagen=imagen_nombre,
        nombre=product.nombre,
        descripcion=product.descripcion,
        precio=product.precio
    )
    db.add(product_data)
    db.commit()

    return {"message": "Producto agregado con éxito"}

@router.get("/list_products", response_class=HTMLResponse)
def list_products(request: Request, db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return templates.TemplateResponse("list_products.html", {"request": request, "products": products})

@router.get("/read/{product_id}", response_class=HTMLResponse)
def read(request: Request, product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).get(product_id)
    return templates.TemplateResponse("read.html", {"request": request, "product": product})

@router.put("/update/{product_id}")
async def update(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    existing_product = db.query(Product).get(product_id)

    if not existing_product:
        return {"message": "Producto no encontrado"}

    existing_product.nombre = product.nombre
    existing_product.descripcion = product.descripcion
    existing_product.precio = product.precio

    if product.imagen:
        imagen_nombre = product.imagen.filename
        imagen_path = f"static/archivos/{imagen_nombre}"
        with open(imagen_path, "wb") as f:
            f.write(await product.imagen.read())
        existing_product.imagen = imagen_nombre

    db.commit()

    return {"message": "Producto editado con éxito"}

@router.delete("/delete/{product_id}")
def delete(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).get(product_id)

    if not product:
        return {"message": "Producto no encontrado"}

    imagen_path = f"static/archivos/{product.imagen}"
    if os.path.exists(imagen_path):
        os.remove(imagen_path)

    db.delete(product)
    db.commit()

    return {"message": "Producto eliminado con éxito"}