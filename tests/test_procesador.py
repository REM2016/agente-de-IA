import pytest

from utils.procesador_lenguaje import obtener_descripcion_tiempo, analizar_estado_animo


@pytest.mark.parametrize("texto,esperado_cat,esperado_minutos", [
    ("5 dias", "mucho", 5 * 24 * 60),
    ("5 horas", "mucho", 5 * 60),
    ("30 minutos", "poco", 30),
    ("1:30", "medio", 90),
    ("45", "medio", 45),
])
def test_obtener_descripcion_tiempo(texto, esperado_cat, esperado_minutos):
    cat, desc, minutos = obtener_descripcion_tiempo(texto)
    assert cat == esperado_cat
    assert minutos == esperado_minutos


def test_analizar_estado_animo_basico():
    # Casos simples que no requieren modelo sofisticado
    estado, desc, conf = analizar_estado_animo("Me siento muy feliz y con muchas ganas de estudiar")
    assert estado in ("motivado", "normal")

    estado2, desc2, conf2 = analizar_estado_animo("Estoy cansado y sin energía")
    assert estado2 in ("cansado", "normal")
