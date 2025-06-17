from src.clase_paciente import Paciente
from src.clase_turno import Turno
from src.clase_receta import Receta
from typing import List, Dict

class HistoriaClinica:
    def __init__(self, paciente: Paciente):
        self.__paciente__ = paciente
        self.__turnos__ : List[Turno] = []
        self.__recetas__ : List[Receta] = []

    def agregar_turno(self, turno: Turno): 
        self.__turnos__.append(turno)

    def agregar_receta(self, receta: Receta):
        self.__recetas__.append(receta)

    def obtener_turnos(self) -> List[Turno]:
        return self.__turnos__
    
    def obtener_recetas(self) -> List[Receta]:
        return self.__recetas__
    def obtener_paciente(self) -> Paciente:
        return self.__paciente__
    
    def __str__(self) -> str:
        if self.__turnos__:
            turnos_str = "\n".join([str(turno) for turno in self.__turnos__])
        else:
            turnos_str = "No hay turnos registrados."
        if self.__recetas__:
            recetas_str = "\n".join([str(receta) for receta in self.__recetas__])
        else:
            recetas_str = "No hay recetas registradas."
            
        return (f"Historia Clínica de {self.__paciente__}:\n"
                f"Turnos:\n{turnos_str}\n"
                f"Recetas:\n{recetas_str}")
    