import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.clase_CLINICA import Clinica
from src.clase_paciente import Paciente
from src.clase_medico import Medico
from src.clase_especialidad import Especialidad
from src.clase_turno import Turno
from src.clase_receta import Receta
from src.clase_historiaclinica import HistoriaClinica
from datetime import datetime
from src.exceptions import (
    PacienteNoEncontradoException,
    TurnoNoDisponibleException,
    MedicoNoEncontradoException,
    PacienteYaExisteException,
    MedicoYaExisteException,
    HistoriaClinicaNoEncontradaException,
    TurnoDuplicadoException
)

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def pausar():
    input("\nPresione ENTER para continuar...")

class CLI:
    def __init__(self):
        self.clinica = Clinica()
    
    def mostrar_menu(self):
        print("\n--- Menú Clínica ---")
        print("1) Agregar paciente")
        print("2) Agregar médico")
        print("3) Agendar turno")
        print("4) Agregar especialidad")
        print("5) Emitir receta")
        print("6) Ver historia clínica")
        print("7) Ver todos los turnos")
        print("8) Ver todos los pacientes")
        print("9) Ver todos los médicos")
        print("0) Salir")
        print("-" * 25)
    
    def ejecutar(self):
        while True:
            self.mostrar_menu()
            opcion = input("Seleccione una opción: ").strip()
            limpiar_pantalla()
        
            if opcion == "1":
                self.agregar_paciente()
            elif opcion == "2":
                self.agregar_medico()
            elif opcion == "3":
                self.agendar_turno()
            elif opcion == "4":
                self.agregar_especialidad()
            elif opcion == "5":
                self.emitir_receta()
            elif opcion == "6":
                self.ver_historia_clinica()
            elif opcion == "7":
                self.ver_todos_los_turnos()
            elif opcion == "8":
                self.ver_todos_los_pacientes()
            elif opcion == "9":
                self.ver_todos_los_medicos()
            elif opcion == "0":
                print("\nSaliendo del sistema...")
                break
            else:
                print("Opción inválida. Intente nuevamente.")
        
            pausar()

    def agregar_paciente(self):
        try:
            print("\n--- Agregar Paciente ---")
            nombre = input("Ingrese el nombre del paciente: ")
            dni = input("Ingrese el DNI del paciente: ").strip()
            fecha_nacimiento_str = input("Ingrese la fecha de nacimiento (dd/mm/aaaa): ")
            paciente = Paciente(dni, nombre, fecha_nacimiento_str)
            self.clinica.agregar_paciente(paciente)
            print("Paciente agregado exitosamente.")  
        except PacienteYaExisteException as e:
            print(f"Error: {e}")
        except ValueError as e:
            print(f"Error: {e}")
    
    def agregar_medico(self):
        try:
            print("\n--- Agregar Médico ---")
            nombre = input("Nombre del médico: ")
            matricula = input("Matrícula del médico: ").strip()
            medico = Medico(nombre, matricula)
            
            print("Ingrese las especialidades del médico:")
            
            while True:
                especialidad_nombre = input("Especialidad (o 'fin' para terminar): ")
                if especialidad_nombre.lower() == 'fin':
                    break
                    
                dias = input("Días de atención (separados por coma): ")
                dias_lista = [dia.strip().lower() for dia in dias.split(",")]
                especialidad = Especialidad(especialidad_nombre, dias_lista)
                medico.agregar_especialidad(especialidad)
            
            self.clinica.agregar_medico(medico)
            print(f"Médico {nombre} agregado exitosamente.")
            
        except MedicoYaExisteException as e:
            print(f"Error: {e}")

    def agendar_turno(self):
        try:
            print("\n--- Agendar Turno ---")
            dni = input("Ingrese el DNI del paciente: ").strip()
            matricula = input("Ingrese la matrícula del médico: ").strip()
            fecha_hora_str = input("Ingrese fecha y hora (dd/mm/aaaa hh:mm): ")
            fecha_hora = datetime.strptime(fecha_hora_str, "%d/%m/%Y %H:%M")
            
            # Preguntar si quiere especialidad específica
            usar_especialidad = input("¿Desea especificar una especialidad? (s/n): ").lower()
            especialidad_solicitada = None
            if usar_especialidad == 's':
                especialidad_solicitada = input("Ingrese la especialidad deseada: ")
            
            # Corrección: agendar_turno tiene parámetros en orden diferente
            turno = self.clinica.agendar_turno(dni, matricula, fecha_hora, especialidad_solicitada)
            print("Turno agendado exitosamente.")
            print(f"Turno: {turno}")
        
        except (PacienteNoEncontradoException, MedicoNoEncontradoException, 
                TurnoNoDisponibleException, TurnoDuplicadoException) as e:
            print(f"Error: {e}")
        except ValueError:
            print("Error: Formato de fecha/hora incorrecto. Use dd/mm/aaaa hh:mm")
    
    def agregar_especialidad(self):
        try:
            print("\n--- Agregar Especialidad a Médico ---")
            matricula = input("Ingrese la matrícula del médico: ").strip()
            medico = self.clinica.obtener_medico_por_matricula(matricula)
            especialidad_nombre = input("Especialidad: ")
            dias = input("Días de atención (separados por coma): ")
            dias_lista = [dia.strip().lower() for dia in dias.split(",")]
            especialidad = Especialidad(especialidad_nombre, dias_lista)
            medico.agregar_especialidad(especialidad)
            print("Especialidad agregada exitosamente.")
            
        except MedicoNoEncontradoException as e:
            print(f"Error: {e}")
    
    def emitir_receta(self):
        try:
            print("\n--- Emitir Receta ---")
            dni = input("Ingrese el DNI del paciente: ").strip()
            matricula = input("Ingrese la matrícula del médico: ").strip()
            medicamentos = input("Ingrese los medicamentos (separados por coma): ")
            medicamentos_lista = [med.strip() for med in medicamentos.split(",")]
            
            receta = self.clinica.emitir_receta(dni, matricula, medicamentos_lista)
            print("Receta emitida exitosamente.")
            print(f"Receta: {receta}")   
            
        except (PacienteNoEncontradoException, MedicoNoEncontradoException, ValueError) as e:
            print(f"Error: {e}")
    
    def ver_historia_clinica(self):
        try:
            print("\n--- Ver Historia Clínica ---")
            dni = input("Ingrese el DNI del paciente: ").strip()
            historia_clinica = self.clinica.obtener_historia_clinica(dni)
            print(f"\nHistoria Clínica:")
            print(historia_clinica)
        except HistoriaClinicaNoEncontradaException as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error: {e}")
        
    def ver_todos_los_turnos(self):
        print("\n--- Todos los Turnos ---")
        turnos = self.clinica.obtener_turnos()
        
        if not turnos:
            print("No hay turnos registrados.")
        else:
            for i, turno in enumerate(turnos, 1):
                print(f"{i}. {turno}")    
    
    def ver_todos_los_pacientes(self):
        print("\n--- Todos los Pacientes ---")
        pacientes = self.clinica.obtener_pacientes()
        
        if not pacientes:
            print("No hay pacientes registrados.")
        else:
            for i, paciente in enumerate(pacientes, 1):
                print(f"{i}. {paciente}")
    
    def ver_todos_los_medicos(self):
        print("\n--- Todos los Médicos ---")
        medicos = self.clinica.obtener_medicos()
        
        if not medicos:
            print("No hay médicos registrados.")
        else:
            for i, medico in enumerate(medicos, 1):
                print(f"{i}. {medico}")

if __name__ == "__main__":
    cli = CLI()
    cli.ejecutar()