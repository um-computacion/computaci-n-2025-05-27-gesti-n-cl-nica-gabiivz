import unittest
from datetime import datetime
from src.clase_turno import Turno
from src.clase_paciente import Paciente
from src.clase_medico import Medico
from src.clase_especialidad import Especialidad
from src.clase_historiaclinica import HistoriaClinica

class TestTurno(unittest.TestCase):

    def setUp(self):
        self.paciente = Paciente("12345678", "Ana Gómez", "10/04/1985")
        self.especialidad = Especialidad("Pediatría", ["Lunes", "Miércoles"])
        self.medico = Medico("Dr. Martínez", "M456", [self.especialidad])
        self.fecha_hora = datetime(2025, 6, 25, 10, 0)
        self.historia_clinica = HistoriaClinica(self.paciente)

    def test_creacion_turno_completo(self):
        turno = Turno(self.paciente, self.medico, self.fecha_hora, self.especialidad)
        self.assertEqual(turno.obtener_paciente(), self.paciente)
        self.assertEqual(turno.obtener_medico(), self.medico)
        self.assertEqual(turno.obtener_fecha(), self.fecha_hora)
        self.assertEqual(turno.obtener_especialidad(), self.especialidad)

    def test_turno_sin_especialidad(self):
        turno = Turno(self.paciente, self.medico, self.fecha_hora)
        self.assertIsNone(turno.obtener_especialidad())

    def test_obtener_paciente(self):
        turno = Turno(self.paciente, self.medico, self.fecha_hora)
        self.assertEqual(turno.obtener_paciente().obtener_nombre_paciente(), "Ana Gómez")

    def test_obtener_medico(self):
        turno = Turno(self.paciente, self.medico, self.fecha_hora)
        self.assertEqual(turno.obtener_medico().obtener_matricula(), "M456")

    def test_obtener_fecha(self):
        turno = Turno(self.paciente, self.medico, self.fecha_hora)
        self.assertEqual(turno.obtener_fecha(), self.fecha_hora)

    def test_str_turno_completo(self):
        turno = Turno(self.paciente, self.medico, self.fecha_hora, self.especialidad)
        resultado = str(turno)
        self.assertIn("Paciente: Ana Gómez", resultado)
        self.assertIn("Especialidad: Pediatría", resultado)
        self.assertIn("2025-06-25", resultado)

    def test_str_turno_sin_especialidad(self):
        turno = Turno(self.paciente, self.medico, self.fecha_hora)
        resultado = str(turno)
        self.assertIn("Especialidad: None", resultado)

    def test_turno_con_fecha_pasada(self):
        fecha_pasada = datetime(2020, 1, 1, 9, 0)
        turno = Turno(self.paciente, self.medico, fecha_pasada)
        self.assertEqual(turno.obtener_fecha(), fecha_pasada)

    def test_turno_sin_paciente_lanza_error(self):
        with self.assertRaises(AttributeError):
            turno = Turno(None, self.medico, self.fecha_hora)
            turno.obtener_paciente().obtener_dni()

    def test_turno_sin_medico_lanza_error(self):
        with self.assertRaises(AttributeError):
            turno = Turno(self.paciente, None, self.fecha_hora)
            turno.obtener_medico().obtener_nombre_medico()

if __name__ == '__main__':
    unittest.main()
