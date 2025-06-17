
class PacienteNoEncontradoException(Exception): 
    pass
class MedicoNoDisponibleException(Exception):
    pass
class TurnoNoDisponibleException(Exception):
    pass

class RecetaInvalidaException(Exception):
    pass

class MedicoNoEncontradoException(Exception):
    pass

class EspecialidadNoEncontradaException(Exception):
    pass

class PacienteDuplicadoException(Exception):
    pass
class PacienteYaExisteException(Exception):
    pass
class MedicoYaExisteException(Exception):
    pass
class HistoriaClinicaNoEncontradaException(Exception):
    pass
class TurnoDuplicadoException(Exception):
    pass