import unittest
from src.clase_paciente import Paciente

class TestPaciente(unittest.TestCase):
    
    def test_creacion_paciente_valido(self):
        paciente = Paciente("12345678", "Juan Pérez", "01/01/1990")
        self.assertEqual(paciente.obtener_dni(), "12345678")
        self.assertIn("Juan Pérez", str(paciente))

    def test_str_representacion(self):
        paciente = Paciente("12345678", "Ana Torres", "02/02/1985")
        resultado = str(paciente)
        self.assertIn("Ana Torres", resultado)
        self.assertIn("12345678", resultado)

    def test_obtener_nombre(self):
        paciente = Paciente("98765432", "Carlos López", "03/03/1980")
        self.assertEqual(paciente.obtener_nombre_paciente(), "Carlos López")

    def test_obtener_fecha_nacimiento(self):
        paciente = Paciente("11223344", "Lucía Gómez", "04/04/1995")
        self.assertEqual(paciente.obtener_fecha_nacimiento(), "04/04/1995")

    def test_dni_es_cadena(self):
        paciente = Paciente("44556677", "Nicolás Ruiz", "05/05/1988")
        self.assertIsInstance(paciente.obtener_dni(), str)

    def test_nombre_no_vacio(self):
        paciente = Paciente("55667788", "María Fernández", "06/06/1992")
        self.assertNotEqual(paciente.obtener_nombre_paciente(), "")

    


if __name__ == '__main__':
    unittest.main()
