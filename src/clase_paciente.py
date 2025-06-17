class Paciente:
    def __init__(self, DNI: str, nombre_paciente: str, fecha_nacimiento: str):
        self.__DNI__ = DNI
        self.__nombre_paciente__ = nombre_paciente
        self.__fecha_nacimiento__ = fecha_nacimiento

    def obtener_dni(self)-> str:
        return self.__DNI__

    def obtener_nombre_paciente(self)-> str:
        return self.__nombre_paciente__
    
    def obtener_fecha_nacimiento(self)-> str:
        return self.__fecha_nacimiento__
    
    def __str__(self):
        return f"Paciente: {self.__nombre_paciente__}, DNI: {self.__DNI__}, Fecha de Nacimiento: {self.__fecha_nacimiento__}"



