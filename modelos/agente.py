"""
Clase principal del Agente de Estudio
"""
from typing import List, Dict, Optional
import json
from pathlib import Path
import random
from config.constantes import RECOMENDACIONES, TIPS_MOTIVACIONALES

class AgenteEstudio:
    def __init__(self):
        self.estado_animo: Optional[str] = None
        self.tiempo_disponible: Optional[str] = None
        self.historial: List[Dict] = []
        self.recomendaciones = RECOMENDACIONES
        self.tips_motivacionales = TIPS_MOTIVACIONALES
        
    def obtener_recomendacion(self, estado_animo: str, tiempo: str) -> List[str]:
        """Obtiene recomendaciones basadas en el estado de ánimo y tiempo disponible"""
        return self.recomendaciones[estado_animo][tiempo]
    
    def obtener_tip_aleatorio(self) -> str:
        """Retorna un tip motivacional aleatorio"""
        return random.choice(self.tips_motivacionales)
    
    def agregar_al_historial(self, registro: Dict) -> None:
        """Agrega un nuevo registro al historial"""
        self.historial.append(registro)
        
    def obtener_estadisticas(self) -> Dict:
        """Obtiene estadísticas del uso del agente"""
        if not self.historial:
            return {}
            
        total_sesiones = len(self.historial)
        estados_animo = {}
        tiempos_estudio = {}
        
        for registro in self.historial:
            estado = registro["estado_animo"]
            tiempo = registro["tiempo"]
            estados_animo[estado] = estados_animo.get(estado, 0) + 1
            tiempos_estudio[tiempo] = tiempos_estudio.get(tiempo, 0) + 1
            
        return {
            "total_sesiones": total_sesiones,
            "estados_animo": estados_animo,
            "tiempos_estudio": tiempos_estudio
        }