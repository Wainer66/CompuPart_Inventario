
from database.conexion import crear_tablas
from services.inventario import GestorInventario


def main():
    crear_tablas()

    gestor = GestorInventario()

    producto = gestor.buscar_producto("USB001")

    if producto is None:
        print("No se encontró el producto USB001.")
        return

    print("PRODUCTO:", producto["nombre"])
    print("Existencias iniciales:", producto["cantidad"])

    try:
        nuevo_stock = gestor.registrar_movimiento(
            codigo="USB001",
            tipo="SALIDA",
            cantidad=3
        )

        print("Entrada registrada: 3 unidades")
        print("Existencias actuales:", nuevo_stock)

    except ValueError as error:
        print("Error:", error)


if __name__ == "__main__":
    main()
