# agente-de-IA

Agente de Estudio — aplicación que sugiere recomendaciones de estudio según tu estado de ánimo y tiempo disponible.

Autor: Celso Antonio Pérez Salguero

## Requisitos

- Python 3.8+
- Paquetes: ver `requirements.txt`
- Modelo de spaCy en español (ver pasos abajo)

## Instalación rápida (Windows / PowerShell)

1. Crear un entorno virtual (opcional pero recomendado):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Instalar dependencias:

```powershell
pip install -r requirements.txt
```

3. Instalar el modelo de spaCy en español (recomendado `es_core_news_md`):

```powershell
python -m spacy download es_core_news_md
```

Si prefieres el modelo pequeño (menor tamaño):

```powershell
python -m spacy download es_core_news_sm
```

## Ejecutar la aplicación

Recomendado (modo paquete):

```powershell
python -m interfaz.ventana
```

O ejecutar directamente (si ya estás en la carpeta del proyecto):

```powershell
python agente_estudio.py
```

## Notas
- Si al iniciar aparece un mensaje indicando que falta el modelo spaCy, siga las instrucciones mostradas o ejecute el comando de instalación anterior.
- Para pruebas rápidas de parseo de tiempo hay un script en `tests/test_time_parse.py`.
