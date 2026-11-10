import tkinter as tk

from database.conexion import crear_tablas
from views.ventana_principal import VentanaPrincipal


def main():
    crear_tablas()

    root = tk.Tk()
    VentanaPrincipal(root)

    root.mainloop()


if __name__ == "__main__":
    main()