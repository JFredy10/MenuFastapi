from app.db.database import Base
from sqlalchemy import Column, Integer, String, Text, Float
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    imagen = Column(String(255), unique=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=False)
    precio = Column(Float, nullable=False)