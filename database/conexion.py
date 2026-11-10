
import sqlite3
from pathlib import Path

# Ubicación de la base de datos
RUTA_BD = Path(__file__).resolve().parent / "compupart.db"


def obtener_conexion():
    """Establece una conexión con SQLite."""
    conexion = sqlite3.connect(RUTA_BD)
    conexion.execute("PRAGMA foreign_keys = ON")
    return conexion


def crear_tablas():
    """Crea las tablas necesarias si todavía no existen."""
    with obtener_conexion() as conexion:

        conexion.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo TEXT NOT NULL UNIQUE,
                nombre TEXT NOT NULL,
                categoria TEXT NOT NULL,
                precio REAL NOT NULL CHECK (precio >= 0),
                cantidad INTEGER NOT NULL DEFAULT 0
                    CHECK (cantidad >= 0),
                stock_minimo INTEGER NOT NULL DEFAULT 5
                    CHECK (stock_minimo >= 0)
            )
        """)

        conexion.execute("""
            CREATE TABLE IF NOT EXISTS movimientos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                producto_id INTEGER NOT NULL,
                tipo TEXT NOT NULL
                    CHECK (tipo IN ('ENTRADA', 'SALIDA')),
                cantidad INTEGER NOT NULL CHECK (cantidad > 0),
                fecha TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (producto_id)
                    REFERENCES productos(id)
            )
        """)

    print("Base de datos inicializada correctamente.")
