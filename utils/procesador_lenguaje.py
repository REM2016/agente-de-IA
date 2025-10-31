"""
Funciones para el procesamiento de lenguaje natural
"""
import re, string
from typing import Optional, Tuple, List
import spacy
from textblob import TextBlob
from config.constantes import ESTADOS_ANIMO_KEYWORDS, PATRONES_TIEMPO

# Cargar el modelo de spaCy en español
try:
    nlp = spacy.load('es_core_news_md')
except OSError:
    # Si el modelo md no está instalado, intentar cargar el modelo pequeño vía spacy
    try:
        nlp = spacy.load('es_core_news_sm')
    except OSError:
        # Dejar que la excepción suba: el entorno debe tener al menos un modelo spaCy instalado
        raise

def procesar_entrada(texto: str) -> Tuple[bool, str, str]:
    """
    Procesa el texto de entrada y detecta saludos/intenciones
    Retorna: (es_saludo, texto_limpio, tipo_mensaje)
    """
    texto = texto.lower().strip()
    doc = nlp(texto)
    
    # Lista de saludos comunes en español
    SALUDOS = {
        'hola', 'buenos días', 'buenas tardes', 'buenas noches',
        'hey', 'saludos', 'qué tal', 'cómo estás', 'qué hay'
    }
    
    # Detectar saludos
    es_saludo = False
    for saludo in SALUDOS:
        if saludo in texto:
            es_saludo = True
            break
    
    # Identificar el tipo de mensaje principal (después del saludo si existe)
    tipo_mensaje = "desconocido"
    texto_limpio = texto
    
    # Si hay saludo, removerlo del texto para análisis
    if es_saludo:
        for saludo in SALUDOS:
            if texto.startswith(saludo):
                texto_limpio = texto[len(saludo):].strip()
                break
    
    # Detectar tipo de mensaje
    palabras_estado = {'siento', 'estoy', 'ando', 'soy', 'tengo'}
    palabras_tiempo = {'minutos', 'horas', 'hora', 'min', 'tiempo'}
    
    for token in doc:
        if token.text in palabras_estado or token.lemma_ in palabras_estado:
            tipo_mensaje = "estado_animo"
            break
        elif token.text in palabras_tiempo or token.lemma_ in palabras_tiempo:
            tipo_mensaje = "tiempo"
            break
    
    return es_saludo, texto_limpio, tipo_mensaje

def tiene_negacion(doc) -> bool:
    """
    Detecta si hay una negación que afecte al estado de ánimo
    """
    for token in doc:
        # Detectar palabras de negación
        if token.dep_ == "neg" or token.text in ["no", "ni", "tampoco", "nunca"]:
            return True
        # Buscar frases de negación comunes
        if token.text + " " + token.head.text in [
            "para nada", "en absoluto", "ya no", "ni siquiera"
        ]:
            return True
    return False

def detectar_intensidad(texto: str) -> float:
    """
    Detecta la intensidad del estado de ánimo basado en modificadores
    Retorna un multiplicador de intensidad (0.5 - 2.0)
    """
    doc = nlp(texto.lower())
    
    # Palabras que indican intensidad
    intensificadores = {
        'muy': 1.5, 'super': 2.0, 'bastante': 1.3,
        'demasiado': 1.8, 'extremadamente': 2.0,
        'poco': 0.7, 'algo': 0.8, 'un poco': 0.6
    }
    
    # Buscar intensificadores en el texto
    for token in doc:
        if token.text in intensificadores:
            return intensificadores[token.text]
        # Detectar repeticiones (ej: "muy muy cansado")
        if token.text == "muy" and token.i + 1 < len(doc) and doc[token.i + 1].text == "muy":
            return 2.0
    
    return 1.0

def invertir_estado(estado: str) -> str:
    """
    Invierte el estado de ánimo cuando hay una negación
    """
    mapeo = {
        "motivado": "cansado",
        "cansado": "normal",
        "normal": "normal"  # estado neutral no se invierte
    }
    return mapeo.get(estado, estado)

def ajustar_por_contexto(texto: str, estado_inicial: str) -> str:
    """
    Ajusta el estado según el contexto y las negaciones
    """
    doc = nlp(texto.lower())
    if tiene_negacion(doc):
        return invertir_estado(estado_inicial)
    return estado_inicial

def analizar_estado_animo(texto: str) -> Optional[str]:
    """Analiza el texto del usuario para determinar su estado de ánimo"""
    # Normalizar el texto
    texto = texto.lower()
    texto = ''.join(c for c in texto if c not in string.punctuation)
    
    # Crear un TextBlob para análisis de sentimiento
    # Procesar con spaCy
    doc = nlp(texto)
    
    # Detectar negaciones y ajustar el análisis
    tiene_neg = tiene_negacion(doc)
    intensidad = detectar_intensidad(texto)
    
    blob = TextBlob(texto)
    
    # Obtener polaridad del sentimiento (-1 muy negativo, 1 muy positivo)
    polaridad = blob.sentiment.polarity
    
    # Primero intentar con análisis de sentimiento
    if polaridad > 0.3:  # Sentimiento positivo
        estado_por_sentimiento = "motivado"
    elif polaridad < -0.2:  # Sentimiento negativo
        estado_por_sentimiento = "cansado"
    else:  # Sentimiento neutral
        estado_por_sentimiento = "normal"
    
    # Analizar palabras clave específicas
    estado_por_keywords = None
    max_coincidencias = 0
    
    # Dividir el texto en palabras y lemmatizar
    palabras = set(texto.split())
    
    for estado, keywords in ESTADOS_ANIMO_KEYWORDS.items():
        coincidencias = sum(1 for kw in keywords if kw in texto)
        if coincidencias > max_coincidencias:
            max_coincidencias = coincidencias
            estado_por_keywords = estado
    
    # Combinar los resultados
    if max_coincidencias >= 2:  # Si hay al menos 2 palabras clave, priorizar keywords
        return estado_por_keywords
    elif max_coincidencias == 1:  # Si hay 1 palabra clave, combinar con sentimiento
        if estado_por_keywords == estado_por_sentimiento:
            return estado_por_keywords
        # Si no coinciden, dar más peso a las palabras clave específicas
        return estado_por_keywords
    
    # Ajustar el resultado final según negaciones y contexto
    estado_final = estado_por_sentimiento
    if tiene_neg:
        estado_final = invertir_estado(estado_final)
    
    return estado_final

def obtener_descripcion_animo(texto: str) -> tuple[str, str, float]:
    """Analiza el texto y devuelve (estado, descripcion, confianza)"""
    blob = TextBlob(texto)
    estado = analizar_estado_animo(texto)
    polaridad = blob.sentiment.polarity
    confianza = abs(polaridad) if estado in ["motivado", "cansado"] else 0.5
    return estado, f"Detectado estado de ánimo: {estado} (confianza: {confianza:.2f})", confianza

def analizar_tiempo(texto: str) -> Optional[str]:
    """Analiza el texto del usuario para determinar el tiempo disponible.

    Ahora delega en `obtener_descripcion_tiempo` y devuelve solo la categoría
    ("poco"|"medio"|"mucho") o None.
    """
    _, _, minutos = obtener_descripcion_tiempo(texto)
    if minutos is None:
        return None
    if minutos <= 30:
        return "poco"
    elif minutos <= 90:
        return "medio"
    else:
        return "mucho"


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

    # Buscar 'X dias' o 'X día' o 'X d'
    m = re.search(r"(\d{1,3})\s*(?:dias|días|dia|día|d)\b", texto)
    if m:
        dias = int(m.group(1))
        minutos = dias * 24 * 60
        if dias < 0:
            return None, None, None
        if minutos <= 30:
            cat = "poco"
        elif minutos <= 90:
            cat = "medio"
        else:
            cat = "mucho"
        descripcion = f"{dias} dia(s)"
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

    # Buscar números sueltos (interpreta según palabras cercanas o por defecto minutos)
    numeros = re.findall(r"\d{1,3}", texto)
    if numeros:
        valor = int(numeros[0])
        # Si el texto menciona 'dia' cerca del número, interpretarlo como días
        if re.search(r"\bdia(s)?\b|\bdías?\b|\bd\b", texto):
            minutos = valor * 24 * 60
        # Si el texto menciona 'hora' cerca del número, interpretarlo como horas
        elif re.search(r"\bhora(s)?\b", texto) or re.search(r"\b\d{1,2}\s*h\b", texto):
            minutos = valor * 60
        else:
            # Por defecto, interpretar como minutos (si el usuario solo escribe '5', asumimos minutos)
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