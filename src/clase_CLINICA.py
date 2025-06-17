from src.clase_paciente import Paciente
from src.clase_medico import Medico
from src.clase_turno import Turno
from src.clase_historiaclinica import HistoriaClinica
from src.clase_especialidad import Especialidad
from src.clase_receta import Receta
from typing import List, Dict
from datetime import datetime
from src.exceptions import PacienteYaExisteException
from src.exceptions import MedicoYaExisteException
from src.exceptions import MedicoNoEncontradoException
from src.exceptions import HistoriaClinicaNoEncontradaException
from src.exceptions import PacienteNoEncontradoException
from src.exceptions import TurnoNoDisponibleException
from src.exceptions import TurnoDuplicadoException

class Clinica:
    def __init__(self): 
        self.__pacientes__: Dict[str, Paciente] = {}
        self.__medicos__: Dict[str, Medico] = {}
        self.__turnos__: List[Turno] = []  
        self.__historias_clinicas__: Dict[str, HistoriaClinica] = {}

    def agregar_paciente(self, paciente: Paciente):
        dni = paciente.obtener_dni()
        if dni in self.__pacientes__:  
            raise PacienteYaExisteException(f"El paciente con DNI {dni} ya está registrado") 
        self.__pacientes__[dni] = paciente  
        self.__historias_clinicas__[dni] = HistoriaClinica(paciente)  

    def agregar_medico(self, medico: Medico):
        matricula = medico.obtener_matricula()  
        if matricula in self.__medicos__:
            raise MedicoYaExisteException(f"El médico con matrícula {matricula} ya está registrado")
        self.__medicos__[matricula] = medico

    def obtener_pacientes(self) -> List[Paciente]:
        return list(self.__pacientes__.values())

    def obtener_medicos(self) -> List[Medico]:
        return list(self.__medicos__.values())

    def obtener_medico_por_matricula(self, matricula: str) -> Medico:
        if matricula not in self.__medicos__:
            raise MedicoNoEncontradoException(f"No existe médico con matrícula {matricula}")
        return self.__medicos__[matricula]
    
    def agendar_turno(self, dni: str, matricula: str, fecha_hora: datetime, especialidad_solicitada: str = None):
        if dni not in self.__pacientes__:
            raise PacienteNoEncontradoException(f"Paciente con DNI {dni} no encontrado")
        if matricula not in self.__medicos__:
            raise MedicoNoEncontradoException(f"Médico con matrícula {matricula} no encontrado")

        paciente = self.__pacientes__[dni]
        medico = self.__medicos__[matricula]
        
        dia_semana = self.obtener_dia_semana_en_espanol(fecha_hora)

        self.validar_turno_no_duplicado(matricula, fecha_hora)

        especialidad_disponible = medico.obtener_especialidad_para_dia(dia_semana)
        if not especialidad_disponible:
            raise TurnoNoDisponibleException(f"El médico no atiende el día {dia_semana}")
        
        if especialidad_solicitada:
            if not self.validar_especialidad_en_dia(medico, especialidad_solicitada, dia_semana):
                raise TurnoNoDisponibleException(f"El médico no atiende {especialidad_solicitada} el día {dia_semana}")
            especialidad_a_usar = especialidad_solicitada
        else:
            especialidad_a_usar = especialidad_disponible

        especialidad_obj = Especialidad(especialidad_a_usar, [dia_semana])

        turno = Turno(paciente, medico, fecha_hora, especialidad_obj)
        self.__turnos__.append(turno)

        self.__historias_clinicas__[dni].agregar_turno(turno)
        
        return turno
    
    def obtener_turnos(self) -> List[Turno]:
        return self.__turnos__.copy()
    
    def emitir_receta(self, dni: str, matricula: str, medicamentos: List[str]):
        if dni not in self.__pacientes__:
            raise PacienteNoEncontradoException(f"Paciente con DNI {dni} no encontrado")
        if matricula not in self.__medicos__:
            raise MedicoNoEncontradoException(f"Médico con matrícula {matricula} no encontrado")
        
        if not medicamentos:
            raise ValueError("Debe incluir al menos un medicamento")
        
        paciente = self.__pacientes__[dni]
        medico = self.__medicos__[matricula]  
        nueva_receta = Receta(paciente, medico, medicamentos)
        
        if dni not in self.__historias_clinicas__:
            self.__historias_clinicas__[dni] = HistoriaClinica(paciente)
        
        self.__historias_clinicas__[dni].agregar_receta(nueva_receta)
        return nueva_receta

    def obtener_historia_clinica(self, dni: str) -> HistoriaClinica:
        if dni not in self.__historias_clinicas__:
            raise HistoriaClinicaNoEncontradaException(f"No existe historia clínica para DNI {dni}")
        return self.__historias_clinicas__[dni]

    def validar_existencia_paciente(self, dni: str) -> bool:
        return dni in self.__pacientes__

    def validar_existencia_medico(self, matricula: str) -> bool:
        return matricula in self.__medicos__
    
    def validar_turno_no_duplicado(self, matricula: str, fecha_hora: datetime):
        for turno in self.__turnos__:
            if (turno.obtener_medico().obtener_matricula() == matricula and 
                turno.obtener_fecha() == fecha_hora):
                raise TurnoDuplicadoException("El médico ya tiene un turno agendado en esa fecha y hora")

    def obtener_dia_semana_en_espanol(self, fecha_hora: datetime) -> str:
        dias_semana = {
            0: "lunes",
            1: "martes", 
            2: "miércoles",
            3: "jueves",
            4: "viernes",
            5: "sábado",
            6: "domingo"
        }
        return dias_semana[fecha_hora.weekday()]

    def obtener_especialidad_disponible(self, medico: Medico, dia_semana: str) -> str:
        especialidad = medico.obtener_especialidad_para_dia(dia_semana)
        if especialidad is None:
            return f"La especialidad no está disponible para el médico {medico} en {dia_semana}."
        return especialidad

    def validar_especialidad_en_dia(self, medico: Medico, especialidad_solicitada: str, dia_semana: str) -> bool:
        especialidades = medico.obtener_especialidades()
        
        for especialidad in especialidades:
            if especialidad.obtener_especialidad().lower() == especialidad_solicitada.lower():
                dias_atencion = especialidad.obtener_dias()
                dias_normalizados = [dia.lower() for dia in dias_atencion]
                if dia_semana.lower() in dias_normalizados:
                    return True
        
        return False
    
    def __str__(self) -> str:
        return f"Clínica - Pacientes: {len(self.__pacientes__)}, Médicos: {len(self.__medicos__)}, Turnos: {len(self.__turnos__)}"



    



