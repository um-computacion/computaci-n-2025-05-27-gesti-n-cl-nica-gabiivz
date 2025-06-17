from typing import List, Dict
class Especialidad: 
    def __init__(self, tipo: str, dias: List[str]):
        self.__tipo__ = tipo
        self.__dias__ = dias 

    def obtener_especialidad(self) -> str:
        return self.__tipo__
    def obtener_dias(self) -> List[str]:
        return self.__dias__
    def verificar_dia(self, dia: str) -> bool:
        if not self.__dias__:
            return False

        for d in self.__dias__:
            if d.lower() == dia.lower():
                return True
        return False
    def __str__(self) -> str:
        return f"Especialidad: {self.__tipo__}, Días: {', '.join(self.__dias__)}"
