"""
Funciones para el procesamiento de lenguaje natural
"""
import re
import string
from typing import Optional
from config.constantes import ESTADOS_ANIMO_KEYWORDS, PATRONES_TIEMPO

def analizar_estado_animo(texto: str) -> Optional[str]:
    """Analiza el texto del usuario para determinar su estado de ánimo"""
    # Normalizar el texto
    texto = texto.lower()
    texto = ''.join(c for c in texto if c not in string.punctuation)
    
    # Buscar coincidencias en las palabras clave
    mejor_match = None
    max_coincidencias = 0
    
    for estado, keywords in ESTADOS_ANIMO_KEYWORDS.items():
        coincidencias = sum(1 for kw in keywords if kw in texto)
        if coincidencias > max_coincidencias:
            max_coincidencias = coincidencias
            mejor_match = estado
            
    return mejor_match

def analizar_tiempo(texto: str) -> Optional[str]:
    """Analiza el texto del usuario para determinar el tiempo disponible"""
    texto = texto.lower()
    
    # Primero intentar encontrar patrones específicos
    for categoria, patrones in PATRONES_TIEMPO.items():
        for patron in patrones:
            if re.search(patron, texto):
                return categoria
    
    # Si no hay patrones específicos, buscar números
    numeros = re.findall(r'\d+', texto)
    if numeros:
        minutos = int(numeros[0])
        if 'hora' in texto:
            minutos *= 60
        
        if minutos <= 45:
            return "poco"
        elif minutos <= 120:
            return "medio"
        else:
            return "mucho"
            
    # Si no hay números, buscar palabras clave generales
    if any(palabra in texto for palabra in ["poco", "breve", "corto", "rapido"]):
        return "poco"
    elif any(palabra in texto for palabra in ["medio", "regular", "moderado"]):
        return "medio"
    elif any(palabra in texto for palabra in ["mucho", "bastante", "largo"]):
        return "mucho"
        
    return None


def obtener_descripcion_tiempo(texto: str) -> tuple:
    """Parsea el texto y devuelve una tupla (categoria, descripcion, minutos).

    - Acepta formatos como:
      * '30 minutos', '5 min', '45'
      * '1:30', '2:15'
      * '2 horas', '3 h'
      * palabras 'poco', 'medio', 'mucho'
    - Devuelve ('poco'|'medio'|'mucho', descripcion_str, minutos_int) o
      (None, None, None) si no se pudo parsear.
    """
    texto_original = texto
    texto = texto.lower().strip()

    # Si el usuario usa directamente las categorías
    if texto in ("poco", "medio", "mucho"):
        defaults = {"poco": 25, "medio": 60, "mucho": 120}
        minutos = defaults[texto]
        descripcion = f"{minutos} minutos (estimado para '{texto}')"
        return texto, descripcion, minutos

    # Buscar formato hh:mm o h:mm
    m = re.search(r"(\d{1,2})[:](\d{1,2})", texto)
    if m:
        h = int(m.group(1))
        mm = int(m.group(2))
        minutos = h * 60 + mm
        minutos = max(0, minutos)
        # validar rango
        if minutos == 0:
            return None, None, None
        # Categorizar
        if minutos <= 30:
            cat = "poco"
        elif minutos <= 90:
            cat = "medio"
        else:
            cat = "mucho"
        descripcion = f"{h}h {mm}m"
        return cat, descripcion, minutos

    # Buscar 'X horas' o 'X hora' o 'X h'
    m = re.search(r"(\d{1,2})\s*(?:horas|hora|h)\b", texto)
    if m:
        horas = int(m.group(1))
        minutos = horas * 60
        if horas < 0:
            return None, None, None
        if minutos <= 30:
            cat = "poco"
        elif minutos <= 90:
            cat = "medio"
        else:
            cat = "mucho"
        descripcion = f"{horas} hora(s)"
        return cat, descripcion, minutos

    # Buscar 'X minutos' o 'X min'
    m = re.search(r"(\d{1,3})\s*(?:minutos|min)\b", texto)
    if m:
        minutos = int(m.group(1))
        if minutos < 0:
            return None, None, None
        if minutos <= 30:
            cat = "poco"
        elif minutos <= 90:
            cat = "medio"
        else:
            cat = "mucho"
        descripcion = f"{minutos} minutos"
        return cat, descripcion, minutos

    # Buscar números sueltos (asumir minutos si <= 60, si >60 asumir minutos también)
    numeros = re.findall(r"\d{1,3}", texto)
    if numeros:
        valor = int(numeros[0])
        # Si el texto menciona 'hora' cerca del número, interpretarlo como horas
        if re.search(r"\bhora(s)?\b", texto):
            minutos = valor * 60
        else:
            # Si el número está acompañado por 'h' (ej. '2h') lo interpretamos como horas
            if re.search(r"\b\d{1,2}\s*h\b", texto):
                minutos = valor * 60
            else:
                minutos = valor

        if minutos <= 0:
            return None, None, None
        if minutos <= 30:
            cat = "poco"
        elif minutos <= 90:
            cat = "medio"
        else:
            cat = "mucho"
        descripcion = f"{minutos} minutos (interpretado de '{texto_original}')"
        return cat, descripcion, minutos

    # Palabras generales
    if any(palabra in texto for palabra in ["poco", "breve", "corto", "rápido", "rapido"]):
        return "poco", "poco tiempo (estimado)", 25
    if any(palabra in texto for palabra in ["medio", "regular", "moderado"]):
        return "medio", "tiempo medio (estimado)", 60
    if any(palabra in texto for palabra in ["mucho", "bastante", "largo"]):
        return "mucho", "mucho tiempo (estimado)", 120

    return None, None, None