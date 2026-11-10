
from dataclasses import dataclass


@dataclass
class Producto:
    codigo: str
    nombre: str
    categoria: str
    precio: float
    cantidad: int
    stock_minimo: int = 5
