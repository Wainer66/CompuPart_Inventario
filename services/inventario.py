
import sqlite3

from database.conexion import obtener_conexion
from models.producto import Producto


class GestorInventario:

    def registrar_producto(self, producto: Producto):
        """Registra un producto en la base de datos."""

        if not producto.codigo.strip():
            raise ValueError("El código es obligatorio.")

        if not producto.nombre.strip():
            raise ValueError("El nombre es obligatorio.")

        if not producto.categoria.strip():
            raise ValueError("La categoría es obligatoria.")

        if producto.precio < 0:
            raise ValueError("El precio no puede ser negativo.")

        if producto.cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa.")

        if producto.stock_minimo < 0:
            raise ValueError("El stock mínimo no puede ser negativo.")

        try:
            with obtener_conexion() as conexion:
                conexion.execute("""
                    INSERT INTO productos
                    (codigo, nombre, categoria, precio,
                     cantidad, stock_minimo)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    producto.codigo.strip(),
                    producto.nombre.strip(),
                    producto.categoria.strip(),
                    producto.precio,
                    producto.cantidad,
                    producto.stock_minimo
                ))

        except sqlite3.IntegrityError as error:
            raise ValueError(
                "No se pudo registrar el producto. "
                "Verificá que el código no esté repetido."
            ) from error

        return True


    def listar_productos(self):
        """Consulta todos los productos registrados."""

        conexion = obtener_conexion()

        try:
            conexion.row_factory = sqlite3.Row

            cursor = conexion.execute("""
                SELECT id, codigo, nombre, categoria,
                       precio, cantidad, stock_minimo
                FROM productos
                ORDER BY nombre
            """)

            productos = [
                dict(fila) for fila in cursor.fetchall()
            ]

            return productos

        finally:
            conexion.close()

    
    def buscar_producto(self, codigo):
        """Busca un producto mediante su código."""

        conexion = obtener_conexion()

        try:
            conexion.row_factory = sqlite3.Row

            cursor = conexion.execute("""
                SELECT id, codigo, nombre, categoria,
                       precio, cantidad, stock_minimo
                FROM productos
                WHERE codigo = ?
            """, (codigo,))

            fila = cursor.fetchone()

            if fila:
                return dict(fila)

            return None

        finally:
            conexion.close()
        

    def productos_stock_bajo(self):
        """Obtiene los productos con existencias bajas."""

        productos = self.listar_productos()

        productos_bajos = [
            producto
            for producto in productos
            if producto["cantidad"] <= producto["stock_minimo"]
        ]

        return productos_bajos



    def registrar_movimiento(self, codigo, tipo, cantidad):
        """Registra una entrada o salida de inventario."""

        codigo = codigo.strip().upper()
        tipo = tipo.strip().upper()

        if tipo not in ("ENTRADA", "SALIDA"):
            raise ValueError("El movimiento debe ser ENTRADA o SALIDA.")

        if type(cantidad) is not int or cantidad <= 0:
            raise ValueError("La cantidad debe ser un entero positivo.")

        conexion = obtener_conexion()

        try:
            conexion.execute("BEGIN IMMEDIATE")

            cursor = conexion.execute(
                "SELECT id, cantidad FROM productos WHERE codigo = ?",
                (codigo,)
            )

            producto = cursor.fetchone()

            if producto is None:
                raise ValueError("El producto no existe.")

            producto_id, stock_actual = producto

            if tipo == "ENTRADA":
                nuevo_stock = stock_actual + cantidad
            else:
                if cantidad > stock_actual:
                    raise ValueError("No hay suficientes existencias.")

                nuevo_stock = stock_actual - cantidad

            conexion.execute(
                "UPDATE productos SET cantidad = ? WHERE id = ?",
                (nuevo_stock, producto_id)
            )

            conexion.execute("""
                INSERT INTO movimientos
                (producto_id, tipo, cantidad)
                VALUES (?, ?, ?)
            """, (producto_id, tipo, cantidad))

            conexion.commit()

            return nuevo_stock

        except Exception:
            conexion.rollback()
            raise

        finally:
            conexion.close()


    def consultar_movimientos(self):
        """Consulta el historial de entradas y salidas."""

        conexion = obtener_conexion()

        try:
            conexion.row_factory = sqlite3.Row

            cursor = conexion.execute("""
                SELECT
                    m.id,
                    p.codigo,
                    p.nombre,
                    m.tipo,
                    m.cantidad,
                    m.fecha
                FROM movimientos AS m
                INNER JOIN productos AS p
                    ON m.producto_id = p.id
                ORDER BY m.id DESC
            """)

            movimientos = [
                dict(fila) for fila in cursor.fetchall()
            ]

            return movimientos

        finally:
            conexion.close()

