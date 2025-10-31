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
from tkinter import messagebox, Tk
import sys


def verificar_dependencias() -> bool:
    """Verifica que las dependencias críticas (spaCy y modelo) estén instaladas.

    Si falta algo, muestra un mensaje con instrucciones y retorna False.
    """
    try:
        import spacy
    except Exception:
        # Mostrar un mensaje claro y terminar
        root = Tk()
        root.withdraw()
        messagebox.showerror(
            "Dependencias faltantes",
            "Falta la librería 'spacy'.\nInstálala con:\n  pip install -r requirements.txt"
        )
        root.destroy()
        return False

    # Intentar cargar el modelo md, fallback a sm; si ninguno está, mostrar instrucción
    try:
        spacy.load('es_core_news_md')
    except Exception:
        try:
            spacy.load('es_core_news_sm')
        except Exception:
            root = Tk()
            root.withdraw()
            messagebox.showerror(
                "Modelo spaCy no encontrado",
                "No se encontró un modelo de spaCy en español.\nEjecuta:\n  python -m spacy download es_core_news_md\n(o: python -m spacy download es_core_news_sm)"
            )
            root.destroy()
            return False
    return True

if __name__ == "__main__":
    try:
        # Verificar dependencias críticas antes de iniciar la UI
        if not verificar_dependencias():
            sys.exit(1)

        # Crear y ejecutar la aplicación
        app = InterfazAgente()
        app.iniciar()
    except Exception as e:
        # Mostrar error en un cuadro de diálogo
        root = Tk()
        root.withdraw()
        messagebox.showerror("Error", f"Ha ocurrido un error: {str(e)}")
        root.destroy()