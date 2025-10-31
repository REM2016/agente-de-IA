from modelos.agente import AgenteEstudio


def test_obtener_recomendacion():
    agente = AgenteEstudio()
    recs = agente.obtener_recomendacion('motivado', 'poco')
    assert isinstance(recs, list)
    assert len(recs) > 0


def test_tip_aleatorio():
    agente = AgenteEstudio()
    tip = agente.obtener_tip_aleatorio()
    assert isinstance(tip, str)
    assert len(tip) > 0
