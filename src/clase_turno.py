from datetime import datetime
from src.clase_paciente import Paciente
from src.clase_medico import Medico
from src.clase_especialidad import Especialidad

class Turno:
    def __init__(self, paciente: Paciente, medico: Medico, fecha_hora: datetime, especialidad: Especialidad = None):
        self.__paciente__ = paciente    
        self.__medico__ = medico
        self.__fecha_hora__ = fecha_hora
        self.__especialidad__ = especialidad

    def obtener_paciente(self) -> Paciente:
        return self.__paciente__

    def obtener_medico(self) -> Medico:
        return self.__medico__

    def obtener_fecha(self):    
        return self.__fecha_hora__

    def obtener_especialidad(self) -> Especialidad:
        return self.__especialidad__

    def __str__(self) -> str:
        return (
            f"Turno asignado - Paciente: {self.__paciente__}, "
            f"Médico: {self.__medico__}, "
            f"Especialidad: {self.__especialidad__}, "
            f"Fecha y hora: {self.__fecha_hora__}"
        )