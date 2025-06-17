from src.clase_especialidad import Especialidad
from typing import List, Dict

class Medico: 
    def __init__(self, nombre_medico : str, matricula : str, especialidad: List[Especialidad] = None):
        self.__nombre_medico__ = nombre_medico
        self.__matricula__ = matricula
        self.__especialidad__ = especialidad if especialidad else []
        
    def agregar_especialidad(self, especialidad: Especialidad):
        self.__especialidad__.append(especialidad)

    def obtener_matricula(self)-> str:
        return self.__matricula__
    
    def obtener_nombre_medico(self)-> str:
        return self.__nombre_medico__

    def obtener_especialidades(self) -> List[Especialidad]:
        return self.__especialidad__
    def obtener_especialidad_para_dia(self, dia: str) -> str | None:
        for especialidad in self.__especialidad__:
            if especialidad.verificar_dia(dia):
                return especialidad.obtener_especialidad() 
        return None
    
    def __str__(self)-> str:
        especialidades_str = ",\n".join([str(esp) for esp in self.__especialidad__])
        return f"{self.__nombre_medico__}, {self.__matricula__}, [{especialidades_str}]"
