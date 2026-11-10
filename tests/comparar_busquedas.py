
import statistics
import time
import tracemalloc
import random
import sys
import platform


def buscar_en_lista(productos, codigo):
    for producto in productos:
        if producto["codigo"] == codigo:
            return producto
    return None


def buscar_en_diccionario(productos, codigo):
    return productos.get(codigo)


def medir_busquedas(estructura, codigos, funcion):
    tiempos = []

    for _ in range(5):
        inicio = time.perf_counter()

        for codigo in codigos:
            funcion(estructura, codigo)

        duracion = time.perf_counter() - inicio
        tiempos.append(duracion / len(codigos))

    return statistics.median(tiempos)


def ejecutar_prueba(cantidad):
    lista = [
        {
            "codigo": f"PROD{i:05d}",
            "nombre": f"Producto {i}"
        }
        for i in range(cantidad)
    ]

    diccionario = {
        producto["codigo"]: producto
        for producto in lista
    }

    # Medir memoria de las estructuras en esta prueba
    tracemalloc.start()

    copia_lista = list(lista)
    copia_diccionario = dict(diccionario)

    memoria_actual, memoria_maxima = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # Consultas existentes y no existentes
    aleatorio = random.Random(42)

    codigos = [
        f"PROD{aleatorio.randrange(cantidad):05d}"
        for _ in range(500)
    ]

    codigos += [
        f"NOEXISTE{i:05d}"
        for i in range(500)
    ]

    aleatorio.shuffle(codigos)

    tiempo_lista = medir_busquedas(
        lista, codigos, buscar_en_lista
    )

    tiempo_diccionario = medir_busquedas(
        diccionario, codigos, buscar_en_diccionario
    )

    print(f"\nCantidad de productos: {cantidad}")
    print(f"Lista: {tiempo_lista:.9f} segundos por consulta")
    print(f"Diccionario: {tiempo_diccionario:.9f} segundos por consulta")
    print(f"Memoria adicional observada: {memoria_maxima / 1024:.2f} KiB")


def main():
    print("COMPARACION DE ESTRUCTURAS - COMPUPART")
    print(f"Python: {sys.version.split()[0]}")
    print(f"Sistema operativo: {platform.system()} {platform.release()}")

    for cantidad in [100, 1000, 10000]:
        ejecutar_prueba(cantidad)


if __name__ == "__main__":
    main()
