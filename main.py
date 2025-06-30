from AlumnoUI import AlumnoUI
from MaestroUI import MaestroUI
from GrupoUI import GrupoUI
from alumno import Alumno
from maestro import Maestro
from grupo import Grupo

def menu_principal():
    while True:
        print("\n=== SISTEMA DE GESTIÓN ESCOLAR ===")
        print("1. Gestión de Alumnos")
        print("2. Gestión de Maestros") 
        print("3. Gestión de Grupos")
        print("4. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            alumnos = Alumno()
            interfaz = AlumnoUI(alumnos, 'alumnos.json')
            interfaz.menu()
        elif opcion == "2":
            maestros = Maestro()
            interfaz = MaestroUI(maestros, 'maestros.json')
            interfaz.menu()
        elif opcion == "3":
            grupos = Grupo()
            interfaz = GrupoUI(grupos, 'grupos.json')
            interfaz.menu()
        elif opcion == "4":
            print("¡Bai Bai!")
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    menu_principal()