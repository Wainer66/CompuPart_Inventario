
# CompuPart - Sistema de Inventarios

## Descripción
CompuPart es un prototipo académico de gestión de inventarios, desarrollado en Python 3 con una interfaz gráfica Tkinter y una base de datos SQLite.

El proyecto fue realizado para el curso Paradigmas de Programación de la Universidad Fidélitas, tomando como referencia un escenario hipotético de una empresa de productos tecnológicos ubicada en Tarrazú, Costa Rica.

## Funcionalidades
- Registro de productos con códigos únicos.
- Consulta de productos por código o nombre.
- Registro de entradas y salidas de inventario.
- Validación de cantidades disponibles.
- Alertas de existencias mínimas.
- Historial de movimientos.
- Almacenamiento persistente mediante SQLite.

## Tecnologías utilizadas
- Python 3
- Tkinter
- SQLite
- Programación orientada a objetos
- Listas y diccionarios

## Cómo ejecutar el programa
1. Descargar el repositorio.
2. Tener Python 3 instalado.
3. Abrir una terminal en la carpeta principal del proyecto.
4. Ejecutar:

```bash
python main.py
```

La base de datos se crea automáticamente al iniciar la aplicación.

## Pruebas
La carpeta `tests` contiene archivos utilizados para comprobar movimientos de inventario, operaciones de SQLite y comparar el rendimiento de búsquedas mediante listas y diccionarios.

Las pruebas de rendimiento utilizan datos simulados y no representan el desempeño completo de la interfaz gráfica.

## Autor
Wainer Marín Fallas  
Ingeniería en Sistemas  
Universidad Fidélitas

## Alcance
Prototipo desarrollado con fines académicos. No incluye facturación, contabilidad ni gestión de órdenes de reparación.
