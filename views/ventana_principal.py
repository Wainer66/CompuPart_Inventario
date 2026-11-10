
import tkinter as tk
from tkinter import ttk
from services.inventario import GestorInventario
from tkinter import messagebox
from tkinter import simpledialog
from models.producto import Producto


class VentanaPrincipal:

    def __init__(self, root):
        self.root = root
        self.root.title("CompuPart - Sistema de Inventarios")
        self.root.geometry("900x550")
        self.root.minsize(700, 450)

        titulo = ttk.Label(
            self.root,
            text="Sistema de Inventarios CompuPart",
            font=("Arial", 20, "bold")
        )

        titulo.pack(pady=30)

        subtitulo = ttk.Label(
            self.root,
            text="Administración y control de productos",
            font=("Arial", 12)
        )

        subtitulo.pack(pady=10)

        # Formulario para registrar productos
        formulario = ttk.LabelFrame(
            self.root,
            text="Registrar nuevo producto",
            padding=10
        )

        formulario.pack(
            fill="x",
            padx=20,
            pady=10
        )

        ttk.Label(
            formulario,
            text="Código:"
        ).grid(row=0, column=0, padx=5, pady=5)

        self.entrada_codigo = ttk.Entry(
            formulario,
            width=15
        )
        self.entrada_codigo.grid(
            row=0, column=1, padx=5, pady=5
        )

        ttk.Label(
            formulario,
            text="Nombre:"
        ).grid(row=0, column=2, padx=5, pady=5)

        self.entrada_nombre = ttk.Entry(
            formulario,
            width=25
        )
        self.entrada_nombre.grid(
            row=0, column=3, padx=5, pady=5
        )

        # Campo categoría
        ttk.Label(
            formulario,
            text="Categoría:"
        ).grid(row=1, column=0, padx=5, pady=5)

        self.entrada_categoria = ttk.Entry(
            formulario,
            width=15
        )
        self.entrada_categoria.grid(
            row=1, column=1, padx=5, pady=5
        )

        # Campo precio
        ttk.Label(
            formulario,
            text="Precio:"
        ).grid(row=1, column=2, padx=5, pady=5)

        self.entrada_precio = ttk.Entry(
            formulario,
            width=25
        )
        self.entrada_precio.grid(
            row=1, column=3, padx=5, pady=5
        )

        # Campo cantidad
        ttk.Label(
            formulario,
            text="Cantidad:"
        ).grid(row=2, column=0, padx=5, pady=5)

        self.entrada_cantidad = ttk.Entry(
            formulario,
            width=15
        )
        self.entrada_cantidad.grid(
            row=2, column=1, padx=5, pady=5
        )

        # Campo stock mínimo
        ttk.Label(
            formulario,
            text="Stock mínimo:"
        ).grid(row=2, column=2, padx=5, pady=5)

        self.entrada_stock_minimo = ttk.Entry(
            formulario,
            width=25
        )
        self.entrada_stock_minimo.grid(
            row=2, column=3, padx=5, pady=5
        )

        # Botón para guardar productos
        self.boton_guardar = ttk.Button(
            formulario,
            text="Guardar producto",
            command=self.guardar_producto
        )

        # Botón para consultar productos con stock bajo
        self.boton_stock = ttk.Button(
            formulario,
            text="Consultar stock bajo",
            command=self.mostrar_stock_bajo
        )

        self.boton_stock.grid(
            row=4,
            column=0,
            columnspan=4,
            pady=5
        )


        # Botones para movimientos de inventario
        self.boton_entrada = ttk.Button(
            formulario,
            text="Registrar entrada",
            command=self.registrar_entrada
        )

        self.boton_entrada.grid(
            row=5,
            column=1,
            padx=5,
            pady=10
        )

        self.boton_salida = ttk.Button(
            formulario,
            text="Registrar salida",
            command=self.registrar_salida
        )

        self.boton_salida.grid(
            row=5,
            column=3,
            padx=5,
            pady=10
        )
        # Botón para consultar el historial
        self.boton_historial = ttk.Button(
            formulario,
            text="Ver historial",
            command=self.ver_historial
        )

        self.boton_historial.grid(
            row=6,
            column=0,
            columnspan=4,
            pady=10
        )

        self.boton_guardar.grid(
            row=3,
            column=0,
            columnspan=4,
            pady=15
        )

        # Buscador de productos por código o nombre
        buscador = ttk.Frame(self.root)
        buscador.pack(fill="x", padx=20, pady=5)

        ttk.Label(
            buscador,
            text="Buscar producto:"
        ).pack(side="left", padx=5)

        self.entrada_busqueda = ttk.Entry(
            buscador,
            width=35
        )
        self.entrada_busqueda.pack(side="left", padx=5)

        ttk.Button(
            buscador,
            text="Buscar",
            command=self.buscar_productos
        ).pack(side="left", padx=5)

        ttk.Button(
            buscador,
            text="Mostrar todos",
            command=self.mostrar_todos
        ).pack(side="left", padx=5)


        # Tabla para visualizar los productos
        columnas = (
            "codigo", "nombre", "categoria",
            "precio", "cantidad"
        )

        self.tabla = ttk.Treeview(
            self.root,
            columns=columnas,
            show="headings"
        )

        self.tabla.heading("codigo", text="Código")
        self.tabla.heading("nombre", text="Nombre")
        self.tabla.heading("categoria", text="Categoría")
        self.tabla.heading("precio", text="Precio")
        self.tabla.heading("cantidad", text="Cantidad")


        self.tabla.column("codigo", width=100, minwidth=80)
        self.tabla.column("nombre", width=250, minwidth=150)
        self.tabla.column("categoria", width=150, minwidth=100)
        self.tabla.column("precio", width=120, minwidth=100)
        self.tabla.column("cantidad", width=90, minwidth=70)


        self.tabla.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )
        self.cargar_productos()

    
    def registrar_entrada(self):
        """Registra una entrada de inventario."""
        self.realizar_movimiento("ENTRADA")

    def registrar_salida(self):
        """Registra una salida de inventario."""
        self.realizar_movimiento("SALIDA")

    def realizar_movimiento(self, tipo):
        """Solicita los datos y actualiza el inventario."""

        codigo = simpledialog.askstring(
            "Movimiento de inventario",
            "Ingrese el código del producto:",
            parent=self.root
        )

        if codigo is None:
            return

        codigo = codigo.strip().upper()

        if not codigo:
            messagebox.showerror(
                "Error",
                "Debe ingresar un código."
            )
            return

        cantidad = simpledialog.askinteger(
            "Movimiento de inventario",
            "Ingrese la cantidad:",
            parent=self.root,
            minvalue=1
        )

        if cantidad is None:
            return

        try:
            gestor = GestorInventario()

            nuevo_stock = gestor.registrar_movimiento(
                codigo,
                tipo,
                cantidad
            )

            messagebox.showinfo(
                "Movimiento registrado",
                f"{tipo} registrada correctamente.\n"
                f"Existencias actuales: {nuevo_stock}"
            )

            # Actualizar la tabla
            for fila in self.tabla.get_children():
                self.tabla.delete(fila)

            self.cargar_productos()

        except ValueError as error:
            messagebox.showerror(
                "Error de inventario",
                str(error)
            )




    def mostrar_stock_bajo(self):
        """Muestra los productos con existencias bajas."""

        gestor = GestorInventario()
        productos = gestor.productos_stock_bajo()

        if not productos:
            messagebox.showinfo(
                "Control de inventario",
                "No hay productos con stock bajo."
            )
            return

        mensaje = "Productos que necesitan reabastecimiento:\n\n"

        for producto in productos:
            mensaje += (
                f"{producto['nombre']}\n"
                f"Cantidad disponible: {producto['cantidad']}\n"
                f"Stock mínimo: {producto['stock_minimo']}\n\n"
            )

        messagebox.showwarning(
            "Alerta de stock bajo",
            mensaje
        )


    
    def cargar_productos(self):
        """Muestra los productos guardados en SQLite."""

        gestor = GestorInventario()
        productos = gestor.listar_productos()

        for producto in productos:
            self.tabla.insert(
                "",
                "end",
                values=(
                    producto["codigo"],
                    producto["nombre"],
                    producto["categoria"],
                    f"₡{producto['precio']:,.2f}",
                    producto["cantidad"]
                )
            )

    
    def guardar_producto(self):
        """Registra un producto desde el formulario."""

        try:
            producto = Producto(
                codigo=self.entrada_codigo.get().strip(),
                nombre=self.entrada_nombre.get().strip(),
                categoria=self.entrada_categoria.get().strip(),
                precio=float(self.entrada_precio.get()),
                cantidad=int(self.entrada_cantidad.get()),
                stock_minimo=int(self.entrada_stock_minimo.get())
            )

            gestor = GestorInventario()
            gestor.registrar_producto(producto)

            messagebox.showinfo(
                "Registro exitoso",
                "El producto se registró correctamente."
            )

            self.tabla.insert(
                "",
                "end",
                values=(
                    producto.codigo,
                    producto.nombre,
                    producto.categoria,
                    f"₡{producto.precio:,.2f}",
                    producto.cantidad
                )
            )


            # Limpiar los campos después del registro
            self.entrada_codigo.delete(0, tk.END)
            self.entrada_nombre.delete(0, tk.END)
            self.entrada_categoria.delete(0, tk.END)
            self.entrada_precio.delete(0, tk.END)
            self.entrada_cantidad.delete(0, tk.END)
            self.entrada_stock_minimo.delete(0, tk.END)

            # Colocar el cursor en el primer campo
            self.entrada_codigo.focus()


        except ValueError as error:
            messagebox.showerror(
                "Error de registro",
                f"Revisá los datos ingresados.\n{error}"
            )

    def ver_historial(self):
        """Muestra el historial de movimientos."""

        gestor = GestorInventario()
        movimientos = gestor.consultar_movimientos()

        ventana = tk.Toplevel(self.root)
        ventana.title("CompuPart - Historial de movimientos")
        ventana.geometry("850x400")

        columnas = (
            "codigo", "nombre", "tipo",
            "cantidad", "fecha"
        )

        tabla = ttk.Treeview(
            ventana,
            columns=columnas,
            show="headings"
        )

        encabezados = {
            "codigo": "Código",
            "nombre": "Producto",
            "tipo": "Movimiento",
            "cantidad": "Cantidad",
            "fecha": "Fecha"
        }

        for columna, titulo in encabezados.items():
            tabla.heading(columna, text=titulo)

        tabla.column("codigo", width=100)
        tabla.column("nombre", width=230)
        tabla.column("tipo", width=120)
        tabla.column("cantidad", width=100)
        tabla.column("fecha", width=180)

        tabla.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        for movimiento in movimientos:
            tabla.insert(
                "",
                "end",
                values=(
                    movimiento["codigo"],
                    movimiento["nombre"],
                    movimiento["tipo"],
                    movimiento["cantidad"],
                    movimiento["fecha"]
                )
            )


    def buscar_productos(self):
        """Busca productos por código o nombre."""

        texto = self.entrada_busqueda.get().strip().lower()

        gestor = GestorInventario()
        productos = gestor.listar_productos()

        # Limpiar la tabla
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        # Mostrar únicamente las coincidencias
        for producto in productos:
            if (
                texto in producto["codigo"].lower()
                or texto in producto["nombre"].lower()
            ):
                self.tabla.insert(
                    "",
                    "end",
                    values=(
                        producto["codigo"],
                        producto["nombre"],
                        producto["categoria"],
                        f"₡{producto['precio']:,.2f}",
                        producto["cantidad"]
                    )
                )

    def mostrar_todos(self):
        """Vuelve a mostrar todos los productos."""

        self.entrada_busqueda.delete(0, tk.END)

        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        self.cargar_productos()
