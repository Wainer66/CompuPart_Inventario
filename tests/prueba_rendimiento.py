
import sqlite3
import tempfile
import time
from pathlib import Path


def probar_rendimiento(cantidad):
    """Mide el registro y la consulta de productos."""

    with tempfile.TemporaryDirectory() as carpeta:
        ruta = Path(carpeta) / "rendimiento.db"

        conexion = sqlite3.connect(ruta)

        try:
            conexion.execute("""
                CREATE TABLE productos (
                    id INTEGER PRIMARY KEY,
                    codigo TEXT UNIQUE NOT NULL,
                    nombre TEXT NOT NULL,
                    precio REAL NOT NULL,
                    cantidad INTEGER NOT NULL
                )
            """)

            productos = [
                (
                    f"PROD{i:05d}",
                    f"Producto {i}",
                    15000.0,
                    10
                )
                for i in range(cantidad)
            ]

            inicio = time.perf_counter()

            conexion.executemany("""
                INSERT INTO productos
                (codigo, nombre, precio, cantidad)
                VALUES (?, ?, ?, ?)
            """, productos)

            conexion.commit()

            tiempo_registro = time.perf_counter() - inicio

            inicio = time.perf_counter()

            resultados = conexion.execute(
                "SELECT * FROM productos"
            ).fetchall()

            tiempo_consulta = time.perf_counter() - inicio

            print(f"\nProductos: {cantidad}")
            print(f"Registros consultados: {len(resultados)}")
            print(f"Tiempo de registro: {tiempo_registro:.6f} segundos")
            print(f"Tiempo de consulta: {tiempo_consulta:.6f} segundos")

        finally:
            conexion.close()


def main():
    print("PRUEBAS DE RENDIMIENTO - COMPUPART")

    for cantidad in [100, 1000, 10000]:
        probar_rendimiento(cantidad)


if __name__ == "__main__":
    main()
