"""
Configuraciones y constantes para el Agente de Estudio
"""

ESTADOS_ANIMO_KEYWORDS = {
    "motivado": [
        # Estados positivos
        "motiva", "anima", "energia", "entusiasmo", "ganas", "alegr",
        "positiv", "bien", "excelente", "dispuesto", "list", "feliz",
        "content", "activ", "inspira", "optimi", "empuje", "animo",
        "fuerza", "poder", "capaz", "preparad", "listo", "energetic",
        "dinamico", "vital", "despierto", "estimulado", "fuerte"
    ],
    "normal": [
        # Estados neutrales
        "normal", "regular", "mas o menos", "neutral", "tranquil",
        "ordinario", "comun", "usual", "tipico", "okay", "ok", 
        "estandar", "promedio", "asi asi", "intermedio", "estable",
        "moderado", "equilibrado", "balanceado", "ni bien ni mal",
        "aceptable", "pasable", "natural"
    ],
    "cansado": [
        # Estados negativos
        "cansa", "agota", "fatiga", "sueno", "dormir", "pesad",
        "agobia", "exhaust", "mal", "desanima", "triste", "deprimi",
        "estres", "preocupa", "nervios", "ansie", "inquiet", "abruma",
        "frustra", "irrita", "molest", "desespera", "angustia", "tedio",
        "aburri", "desinteres", "perez", "floj", "desgan", "somnolien",
        "adormil", "apatic", "desconcentra", "distra", "confundi"
    ]
}

PATRONES_TIEMPO = {
    "poco": [
        r"(\d{1,2})\s*min",  # 30 min, 15 minutos
        r"media\s*hora",      # media hora
        r"poco\s*tiempo",     # poco tiempo
        r"corto",             # corto tiempo
        r"rapido",            # algo rápido
    ],
    "medio": [
        r"(\d{1})\s*hora",    # 1 hora, 2 horas
        r"hora\s*y\s*media",  # hora y media
        r"90\s*min",          # 90 minutos
    ],
    "mucho": [
        r"(\d{1,2})\s*horas", # 3 horas o más
        r"toda\s*la\s*tarde", # toda la tarde
        r"todo\s*el\s*dia",   # todo el día
        r"bastante",          # bastante tiempo
        r"mucho",             # mucho tiempo
    ]
}

RECOMENDACIONES = {
    "motivado": {
        "poco": ["Repasa un tema complejo durante 30 minutos", 
                "Haz 3 ejercicios de práctica"],
        "medio": ["Estudia un tema nuevo durante 1 hora", 
                 "Completa una tarea pendiente"],
        "mucho": ["Prepara una presentación completa", 
                 "Realiza un proyecto práctico"]
    },
    "normal": {
        "poco": ["Lee un artículo corto", 
                "Revisa tus apuntes"],
        "medio": ["Haz un resumen de un tema", 
                 "Practica con ejercicios básicos"],
        "mucho": ["Estudia dos temas relacionados", 
                 "Prepara un ensayo"]
    },
    "cansado": {
        "poco": ["Toma un descanso de 15 minutos y luego repasa algo ligero", 
                "Escucha una clase grabada"],
        "medio": ["Alterna entre estudio y descansos", 
                 "Haz ejercicios sencillos"],
        "mucho": ["Divide tu estudio en bloques de 30 minutos", 
                 "Combina teoría con práctica ligera"]
    }
}

TIPS_MOTIVACIONALES = [
    "💡 Recuerda tomar descansos cortos cada 25-30 minutos",
    "💪 La constancia es más importante que la intensidad",
    "🎯 Establece metas pequeñas y alcanzables",
    "📚 Alterna entre diferentes materias para mantener el interés",
    "🌟 Celebra tus pequeños logros"
]