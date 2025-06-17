import unittest
from src.clase_especialidad import Especialidad  


class TestEspecialidad(unittest.TestCase):

    def test_creacion_valida(self):
        especialidad = Especialidad("Pediatría", ["lunes", "miércoles"])
        self.assertEqual(especialidad.obtener_especialidad(), "Pediatría")
        self.assertTrue(especialidad.verificar_dia("lunes"))
        self.assertIn("lunes", str(especialidad))

    def test_dia_no_disponible(self):
        especialidad = Especialidad("Clínica", ["martes"])
        self.assertFalse(especialidad.verificar_dia("jueves"))

    def test_str_representacion(self):
        especialidad = Especialidad("Cardiología", ["lunes", "viernes"])
        resultado = str(especialidad)
        self.assertIn("Cardiología", resultado)
        self.assertIn("lunes", resultado)


if __name__ == '__main__':
    unittest.main()