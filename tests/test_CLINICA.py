import unittest
from datetime import datetime
from src.clase_CLINICA import Clinica
from src.clase_paciente import Paciente
from src.clase_medico import Medico
from src.clase_especialidad import Especialidad
from src.exceptions import *

class TestClinica(unittest.TestCase):

    def setUp(self):
        self.clinica = Clinica()
        self.medico = Medico("Dra. García", "M001")  
        self.clinica.agregar_medico(self.medico)
        self.paciente = Paciente("12345678", "Juan Perez", "15/05/1990")
        self.especialidad = Especialidad("Cardiología", ["lunes", "miércoles"])
        self.medico.agregar_especialidad(self.especialidad)
        self.clinica.agregar_paciente(self.paciente)

    def test_agregar_paciente(self):
        nuevo_paciente = Paciente("87654321", "María López", "20/03/1985")
        self.clinica.agregar_paciente(nuevo_paciente)
        self.assertIn(nuevo_paciente, self.clinica.obtener_pacientes())

    def test_agregar_paciente_duplicado(self):
        with self.assertRaises(PacienteYaExisteException):
            self.clinica.agregar_paciente(self.paciente)

    def test_agregar_medico(self):
        nuevo_medico = Medico("Dr. Rodríguez", "M002")
        self.clinica.agregar_medico(nuevo_medico)
        self.assertIn(nuevo_medico, self.clinica.obtener_medicos())

    def test_agregar_medico_duplicado(self):
        with self.assertRaises(MedicoYaExisteException):
            self.clinica.agregar_medico(self.medico)  

    def test_agendar_turno_correcto(self):
        fecha = datetime(2025, 6, 16, 10, 0)  
        turno = self.clinica.agendar_turno("12345678", "M001", fecha, "Cardiología")
        self.assertEqual(turno.obtener_fecha(), fecha)

    def test_agendar_turno_paciente_inexistente(self):
        with self.assertRaises(PacienteNoEncontradoException):
            self.clinica.agendar_turno("99999999", "M001", datetime(2025, 6, 16, 10, 0), "Cardiología")

    def test_agendar_turno_medico_inexistente(self):
        with self.assertRaises(MedicoNoEncontradoException):
            self.clinica.agendar_turno("12345678", "NOEXISTE", datetime(2025, 6, 16, 10, 0), "Cardiología")

    def test_agendar_turno_especialidad_no_disponible(self):
        medico_sin_esp = Medico("Dr. Sin Especialidad", "M003")
        self.clinica.agregar_medico(medico_sin_esp)

        with self.assertRaises(TurnoNoDisponibleException):
            self.clinica.agendar_turno("12345678", "M003", datetime(2025, 6, 16, 10, 0), "Cardiología")

    def test_agendar_turno_dia_no_disponible(self):
        fecha_martes = datetime(2025, 6, 17, 10, 0)  
        with self.assertRaises(TurnoNoDisponibleException):
            self.clinica.agendar_turno("12345678", "M001", fecha_martes, "Cardiología")

    def test_agendar_turno_duplicado(self):
        fecha = datetime(2025, 6, 16, 10, 0)
        self.clinica.agendar_turno("12345678", "M001", fecha, "Cardiología")
        
        paciente2 = Paciente("87654321", "María López", "20/03/1985")
        self.clinica.agregar_paciente(paciente2)

        with self.assertRaises(TurnoDuplicadoException):
            self.clinica.agendar_turno("87654321", "M001", fecha, "Cardiología")

    def test_agendar_turno_sin_especialidad_especifica(self):
        fecha = datetime(2025, 6, 16, 10, 0)  
        turno = self.clinica.agendar_turno("12345678", "M001", fecha)  
        self.assertEqual(turno.obtener_fecha(), fecha)

    def test_emitir_receta_correcta(self):
        receta = self.clinica.emitir_receta("12345678", "M001", ["Paracetamol", "Ibuprofeno"])
        self.assertIn("Paracetamol", str(receta))

    def test_emitir_receta_sin_medicamentos(self):
        with self.assertRaises(ValueError):
            self.clinica.emitir_receta("12345678", "M001", [])

    def test_emitir_receta_paciente_inexistente(self):
        with self.assertRaises(PacienteNoEncontradoException):
            self.clinica.emitir_receta("99999999", "M001", ["Paracetamol"])

    def test_emitir_receta_medico_inexistente(self):
        with self.assertRaises(MedicoNoEncontradoException):
            self.clinica.emitir_receta("12345678", "mmmm", ["Paracetamol"])

    def test_obtener_historia_clinica(self):
        historia = self.clinica.obtener_historia_clinica("12345678")
        self.assertEqual(historia.obtener_paciente(), self.paciente)  

    def test_obtener_historia_clinica_inexistente(self):
        with self.assertRaises(HistoriaClinicaNoEncontradaException):
            self.clinica.obtener_historia_clinica("99999999")

    def test_obtener_medico_por_matricula(self):

        medico_obtenido = self.clinica.obtener_medico_por_matricula("M001")
        self.assertEqual(medico_obtenido.obtener_matricula(), "M001")

    def test_obtener_medico_por_matricula_inexistente(self):
        with self.assertRaises(MedicoNoEncontradoException):
            self.clinica.obtener_medico_por_matricula("NOEXISTE")

    def test_obtener_pacientes_vacio(self):
        clinica_vacia = Clinica()
        self.assertEqual(clinica_vacia.obtener_pacientes(), [])

    def test_obtener_medicos_vacio(self):
        clinica_vacia = Clinica()
        self.assertEqual(clinica_vacia.obtener_medicos(), [])

    def test_obtener_turnos_vacio(self):
        clinica_vacia = Clinica()
        self.assertEqual(clinica_vacia.obtener_turnos(), [])

    def test_obtener_dia_semana_en_espanol(self):
        fecha = datetime(2025, 6, 16)  
        dia = self.clinica.obtener_dia_semana_en_espanol(fecha)
        self.assertEqual(dia, "lunes")

    def test_validar_existencia_paciente(self):

        clinica_test = Clinica()
        self.assertFalse(clinica_test.validar_existencia_paciente("12345678"))
        clinica_test.agregar_paciente(self.paciente)
        self.assertTrue(clinica_test.validar_existencia_paciente("12345678"))

    def test_validar_existencia_medico_robusto(self):

        clinica_test = Clinica()
        matricula_medico = self.medico.obtener_matricula()
        self.assertFalse(clinica_test.validar_existencia_medico(matricula_medico))
        clinica_test.agregar_medico(self.medico)
        self.assertTrue(clinica_test.validar_existencia_medico(matricula_medico))

    def test_obtener_especialidad_disponible(self):
        resultado = self.clinica.obtener_especialidad_disponible(self.medico, "lunes")
        self.assertEqual(resultado, "Cardiología")

    def test_obtener_especialidad_no_disponible(self):
        resultado = self.clinica.obtener_especialidad_disponible(self.medico, "martes")
        self.assertIn("no está disponible", resultado)

    def test_validar_especialidad_en_dia(self):

        self.assertTrue(self.clinica.validar_especialidad_en_dia(self.medico, "Cardiología", "lunes"))

        self.assertFalse(self.clinica.validar_especialidad_en_dia(self.medico, "Cardiología", "martes"))

        self.assertFalse(self.clinica.validar_especialidad_en_dia(self.medico, "Neurología", "lunes"))

    def test_str_clinica(self):
        str_resultado = str(self.clinica)
        self.assertIn("Pacientes: 1", str_resultado)
        self.assertIn("Médicos: 1", str_resultado)
        self.assertIn("Turnos: 0", str_resultado)

    def test_historia_clinica_se_crea_al_agregar_paciente(self):
        
        historia = self.clinica.obtener_historia_clinica("12345678")
        self.assertIsNotNone(historia)
        self.assertEqual(historia.obtener_paciente(), self.paciente)


if __name__ == '__main__':
    unittest.main()