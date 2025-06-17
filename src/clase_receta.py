from src.clase_paciente import Paciente
from src.clase_medico import Medico
from datetime import datetime
from typing import List

class Receta:
    def __init__(self, paciente: Paciente, medico: Medico, medicamentos: List[str], fecha: datetime = None):
        if not isinstance(paciente, Paciente) or not isinstance(medico, Medico):
            raise TypeError("Paciente y médico deben ser objetos válidos")

        if not medicamentos or not all(isinstance(m, str) and m.strip() for m in medicamentos):
            raise ValueError("Debe incluir al menos un medicamento válido")

        self.__paciente__ = paciente
        self.__medico__ = medico
        self.__fecha__ = datetime.now() 
        self.__medicamentos__ = medicamentos

    def obtener_fecha(self) -> datetime:
        return self.__fecha__

    def agregar_medicamento(self, medicamento: str):
        self.__medicamentos__.append(medicamento)
        
    def __str__(self) -> str:
        return f"Receta(Paciente({self.__paciente__}), Medico: ({self.__medico__}), Medicamentos: [{self.__medicamentos__}], Fecha: {self.__fecha__.strftime('%Y-%m-%d %H:%M:%S')})"
