"""
Agente de Estudio - Programa Principal
Universidad Mariano Gálvez de Guatemala
Autor: Celso Antonio Pérez Salguero
Fecha: Octubre 2025

Este es el archivo principal que inicia la aplicación.
La lógica del agente y la interfaz se encuentran en los módulos correspondientes:
- modelos/agente.py: Clase principal del agente
- interfaz/ventana.py: Interfaz gráfica
- utils/procesador_lenguaje.py: Procesamiento de texto
- config/constantes.py: Configuraciones y constantes
"""

from interfaz.ventana import InterfazAgente
from tkinter import messagebox

if __name__ == "__main__":
    try:
        # Crear y ejecutar la aplicación
        app = InterfazAgente()
        app.iniciar()
    except Exception as e:
        messagebox.showerror("Error", f"Ha ocurrido un error: {str(e)}")