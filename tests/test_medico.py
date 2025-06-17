import unittest
from src.clase_medico import Medico
from src.clase_especialidad import Especialidad

class TestMedico(unittest.TestCase):

    def test_registro_exitoso_medico_con_datos_validos(self):
        medico = Medico("Dra. López", "M001")
        self.assertEqual(medico.obtener_matricula(), "M001")
        self.assertEqual(medico.obtener_nombre_medico(), "Dra. López")
        self.assertIn("Dra. López", str(medico))
        self.assertIn("M001", str(medico))

    def test_medico_sin_especialidades_iniciales(self):
        medico = Medico("Dr. García", "M002")
        self.assertEqual(len(medico.obtener_especialidades()), 0)

    def test_agregar_especialidad(self):
        medico = Medico("Dr. Pérez", "M003")
        especialidad = Especialidad("Cardiología", ["lunes", "miércoles"])
        medico.agregar_especialidad(especialidad)
        self.assertEqual(len(medico.obtener_especialidades()), 1)
        self.assertIn(especialidad, medico.obtener_especialidades())

    def test_obtener_especialidad_para_dia_disponible(self):
        medico = Medico("Dra. Martínez", "M004")
        especialidad = Especialidad("Neurología", ["martes", "jueves"])
        medico.agregar_especialidad(especialidad)
        
        resultado = medico.obtener_especialidad_para_dia("martes")
        self.assertEqual(resultado, "Neurología")

    def test_obtener_especialidad_para_dia_no_disponible(self):
        medico = Medico("Dr. Rodríguez", "M005")
        especialidad = Especialidad("Dermatología", ["lunes"])
        medico.agregar_especialidad(especialidad)
        
        resultado = medico.obtener_especialidad_para_dia("viernes")
        self.assertIsNone(resultado)

    def test_medico_con_multiple_especialidades(self):
        medico = Medico("Dr. González", "M006")
        esp1 = Especialidad("Cardiología", ["lunes", "miércoles"])
        esp2 = Especialidad("Medicina General", ["martes", "jueves"])
        
        medico.agregar_especialidad(esp1)
        medico.agregar_especialidad(esp2)
        
        self.assertEqual(len(medico.obtener_especialidades()), 2)
        self.assertEqual(medico.obtener_especialidad_para_dia("lunes"), "Cardiología")
        self.assertEqual(medico.obtener_especialidad_para_dia("martes"), "Medicina General")

    def test_str_medico_con_especialidades(self):
        medico = Medico("Dra. López", "M007")
        especialidad = Especialidad("Pediatría", ["lunes", "miércoles"])
        medico.agregar_especialidad(especialidad)
        
        str_medico = str(medico)
        self.assertIn("Dra. López", str_medico)
        self.assertIn("M007", str_medico)
        self.assertIn("Pediatría", str_medico)

if __name__ == '__main__':
    unittest.main()
