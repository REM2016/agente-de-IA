"""
Interfaz gráfica del Agente de Estudio
"""
import tkinter as tk
from tkinter import scrolledtext, ttk
from datetime import datetime
import json
from pathlib import Path
import os
import sys

# Asegurar que el directorio raíz del proyecto esté en sys.path cuando se ejecute
# este archivo directamente. Esto evita ModuleNotFoundError al importar paquetes
# como `modelos` o `utils` si se ejecuta `python interfaz/ventana.py` desde la carpeta
# del propio módulo.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from modelos.agente import AgenteEstudio
from utils.procesador_lenguaje import analizar_estado_animo, analizar_tiempo

class InterfazAgente:
    def __init__(self):
        self.agente = AgenteEstudio()
        self.ventana = tk.Tk()
        self.ventana.title("🎓 Agente de Estudio - UMG")
        self.ventana.geometry("500x600")
        self.ventana.resizable(False, False)
        
        # Configurar estilo
        self.style = ttk.Style()
        self.style.configure("Custom.TButton", 
                           padding=5, 
                           font=("Arial", 9))
        
        # Cargar datos guardados
        self._cargar_datos()
        
        # Configurar la interfaz
        self._configurar_chat()
        self._configurar_entrada()
        self._iniciar_conversacion()
        
    def _configurar_chat(self):
        """Configura el área de chat"""
        # Frame principal
        self.chat_frame = tk.Frame(self.ventana)
        self.chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Área de chat
        self.chat_area = scrolledtext.ScrolledText(
            self.chat_frame, 
            wrap=tk.WORD, 
            state='disabled',
            width=55, 
            height=20,
            font=("Arial", 11),
            padx=10,
            pady=10
        )
        self.chat_area.pack(pady=5)
        
        # Frame para botones de estado de ánimo
        self.botones_animo = tk.Frame(self.chat_frame)
        self.botones_animo.pack(pady=5)
        
        for estado in ["😊 Motivado", "😐 Normal", "😫 Cansado"]:
            ttk.Button(
                self.botones_animo,
                text=estado,
                style="Custom.TButton",
                command=lambda e=estado: self._procesar_animo(e.split()[1].lower())
            ).pack(side=tk.LEFT, padx=5)
            
        # Frame para botones de tiempo
        self.botones_tiempo = tk.Frame(self.chat_frame)
        self.botones_tiempo.pack(pady=5)
        
        for tiempo in ["⏱️ Poco", "⏲️ Medio", "⌛ Mucho"]:
            ttk.Button(
                self.botones_tiempo,
                text=tiempo,
                style="Custom.TButton",
                command=lambda t=tiempo: self._procesar_tiempo(t.split()[1].lower())
            ).pack(side=tk.LEFT, padx=5)
        
        # Ocultar botones de tiempo inicialmente
        self.botones_tiempo.pack_forget()

    def _configurar_entrada(self):
        """Configura el área de entrada de texto"""
        self.frame_input = tk.Frame(self.ventana)
        self.frame_input.pack(pady=5)

        self.entrada_usuario = tk.Entry(
            self.frame_input,
            width=30,
            font=("Arial", 10)
        )
        self.entrada_usuario.pack(side=tk.LEFT, padx=5)
        self.entrada_usuario.bind("<Return>", lambda e: self._procesar_entrada())

        self.boton_enviar = tk.Button(
            self.frame_input,
            text="Enviar",
            command=self._procesar_entrada
        )
        self.boton_enviar.pack(side=tk.LEFT)

    def mostrar_mensaje(self, texto: str, remitente: str = "Agente 🤖"):
        """Muestra un mensaje en el área de chat"""
        self.chat_area.config(state='normal')
        timestamp = datetime.now().strftime("%H:%M")
        
        # Agregar línea separadora si es un mensaje del agente
        if remitente.startswith("Agente"):
            self.chat_area.insert(tk.END, "\n")
            
        self.chat_area.insert(tk.END, f"[{timestamp}] {remitente}:\n   {texto}\n")
        
        # Agregar espacio extra después de cada mensaje
        self.chat_area.insert(tk.END, "\n")
        
        self.chat_area.config(state='disabled')
        self.chat_area.yview(tk.END)

    def _iniciar_conversacion(self):
        """Inicia la conversación con el mensaje de bienvenida"""
        self.estado_conversacion = "esperar_animo"
        self.mostrar_mensaje("¡Hola! Soy tu Agente de Estudio 🎓")
        self.mostrar_mensaje("Cuéntame, ¿cómo te sientes hoy?")

    def _procesar_entrada(self):
        """Procesa la entrada del usuario"""
        texto = self.entrada_usuario.get().strip()
        if not texto:
            return

        self.mostrar_mensaje(texto, "Tú 👤")
        self.entrada_usuario.delete(0, tk.END)

        if self.estado_conversacion == "esperar_animo":
            self._procesar_animo(texto)
        elif self.estado_conversacion == "esperar_tiempo":
            self._procesar_tiempo(texto)

    def _procesar_animo(self, texto: str):
        """Procesa la respuesta del estado de ánimo"""
        from utils.procesador_lenguaje import obtener_descripcion_animo
        estado_animo, descripcion, confianza = obtener_descripcion_animo(texto)
        
        if not estado_animo:
            self.mostrar_mensaje("Disculpa, no pude entender bien cómo te sientes. ¿Podrías decirlo de otra forma?")
            self.mostrar_mensaje("Puedes decirme si te sientes motivado, normal, cansado, o describir tu estado en tus propias palabras.")
            return

        self.agente.estado_animo = estado_animo
        self.estado_conversacion = "esperar_tiempo"
        
        # Si la confianza es alta (>0.6), dar una respuesta más específica
        if confianza > 0.6:
            respuestas = {
                "motivado": "¡Excelente! Me alegra mucho ver que estás tan motivado. ",
                "normal": "Entiendo, estás en un estado neutral y equilibrado. ",
                "cansado": "Comprendo perfectamente que estés cansado, es normal sentirse así. "
            }
        else:
            respuestas = {
                "motivado": "¡Me alegro que tengas algo de motivación! ",
                "normal": "Entiendo que te sientas así. ",
                "cansado": "Comprendo que no estés en tu mejor momento. "
            }
        
        self.mostrar_mensaje(f"{respuestas[estado_animo]}¿Cuánto tiempo tienes para estudiar?")
        
        # Mostrar/ocultar botones según el estado
        self.botones_animo.pack_forget()
        self.botones_tiempo.pack(pady=5)

    def _procesar_tiempo(self, texto: str):
        """Procesa la respuesta del tiempo disponible"""
        from utils.procesador_lenguaje import obtener_descripcion_tiempo

        # Obtener categoría (poco/medio/mucho), descripción y minutos totales
        categoria, descripcion, minutos = obtener_descripcion_tiempo(texto)

        if not categoria or minutos is None:
            self.mostrar_mensaje("Disculpa, no pude entender bien cuánto tiempo tienes. ¿Podrías decirlo de otra forma?")
            self.mostrar_mensaje("Puedes decirlo en minutos (ej: 30 minutos) o en horas (ej: 1:30, 2 horas)")
            return

        if minutos > 24 * 60:  # Más de 24 horas
            self.mostrar_mensaje("¡Wow! Ese es mucho tiempo. Te sugiero dividirlo en sesiones más cortas para ser más efectivo.")
            self.mostrar_mensaje("¿Qué te parece si empezamos con una sesión más corta?")
            return

        # Guardar categoría en el agente y obtener recomendaciones generales
        self.agente.tiempo_disponible = categoria
        recomendaciones = self.agente.obtener_recomendacion(self.agente.estado_animo, categoria)

        # Agregar recomendaciones específicas basadas en el tiempo exacto
        recomendaciones_tiempo = []
        if minutos <= 30:
            recomendaciones_tiempo = [
                f"💡 {minutos} minutos son ideales para una sesión de repaso rápido",
                "🔍 Enfócate en un solo tema específico"
            ]
        elif minutos <= 90:
            recomendaciones_tiempo = [
                f"💡 Con {minutos} minutos puedes hacer una sesión completa",
                "⏱️ Considera tomar un descanso de 5 minutos a la mitad"
            ]
        else:
            horas = minutos / 60
            recomendaciones_tiempo = [
                f"💡 {horas:.1f} horas te permiten cubrir varios temas",
                "⏱️ Recuerda tomar descansos de 10-15 minutos cada hora",
                "📋 Haz una lista de temas para aprovechar mejor el tiempo"
            ]

        # Guardar en el historial
        registro = {
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "estado_animo": self.agente.estado_animo,
            "tiempo": self.agente.tiempo_disponible,
            "recomendaciones": recomendaciones
        }
        self.agente.agregar_al_historial(registro)
        self._guardar_datos()

        # Mostrar recomendaciones
        self.mostrar_mensaje("🎯 Basado en tu estado de ánimo y tiempo disponible, te recomiendo:")

        # Combinar y mostrar todas las recomendaciones
        todas_recomendaciones = recomendaciones + recomendaciones_tiempo
        recomendaciones_texto = "\n".join(f"   {i}. {rec}" for i, rec in enumerate(todas_recomendaciones, 1))
        self.mostrar_mensaje(recomendaciones_texto)

        # Mostrar un tip motivacional aleatorio
        tip = self.agente.obtener_tip_aleatorio()
        self.mostrar_mensaje(tip)

        self.estado_conversacion = "esperar_animo"
        self.mostrar_mensaje("¿Cómo te sientes ahora?")

        # Mostrar/ocultar botones según el estado
        self.botones_tiempo.pack_forget()
        self.botones_animo.pack(pady=5)
        


    def _cargar_datos(self):
        """Carga los datos del agente desde archivos"""
        try:
            ruta = Path("datos_agente.json")
            if ruta.exists():
                with open(ruta, "r", encoding="utf-8") as f:
                    datos = json.load(f)
                    self.agente.historial = datos.get("historial", [])
        except Exception as e:
            print(f"Error al cargar datos: {e}")
            self.agente.historial = []
    
    def _guardar_datos(self):
        """Guarda los datos del agente en archivos"""
        try:
            datos = {
                "historial": self.agente.historial
            }
            with open("datos_agente.json", "w", encoding="utf-8") as f:
                json.dump(datos, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error al guardar datos: {e}")

    def iniciar(self):
        """Inicia la aplicación"""
        self.ventana.mainloop()