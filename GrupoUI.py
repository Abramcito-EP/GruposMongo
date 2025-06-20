from grupo import Grupo
from maestro import Maestro
from MaestroUI import MaestroUI
from AlumnoUI import AlumnoUI
import json
import os

class GrupoUI:
    def __init__(self, grupos=None, archivo="grupos.json"):
        self.archivo = archivo
        self.guardar = False

        if grupos is not None and len(grupos.items) > 0:
            self.grupos = grupos
            print("Usando clase Grupo.")
        elif archivo and os.path.exists(archivo):
            print(f"Cargando grupos desde archivo '{archivo}'.")
            self.grupos = Grupo()
            self.grupos.cargarArchivo(archivo, Grupo)
            self.guardar = True
        else:
            print("No se proporcionó archivo ni objeto con datos. Creando lista vacía.")
            self.grupos = Grupo()

        self.interfaz_maestro = MaestroUI()
        self.interfaz_alumno = AlumnoUI()

    def menu(self):
        while True:
            print("\n--- Menú de Grupos ---")
            print("1. Mostrar grupos")
            print("2. Agregar grupo")
            print("3. Eliminar grupo")
            print("4. Actualizar grupo")
            print("5. Salir")

            opcion = input("Seleccione una opción: ")
            if opcion == "1":
                self.mostrar_grupos()
            elif opcion == "2":
                self.agregar_grupo()
            elif opcion == "3":
                self.eliminar_grupo()
            elif opcion == "4":
                self.actualizar_grupo()
            elif opcion == "5":
                print("Saliendo...")
                if self.guardar:
                    self.grupos.guardarArchivo(self.archivo)
                break
            else:
                print("Opción no válida.")

    def mostrar_grupos(self):
        print(json.dumps(self.grupos.convertir_diccionario(), indent=4, ensure_ascii=False))

    def agregar_grupo(self):
        nombre = input("Nombre del grupo: ")
        grado = input("Grado: ")
        seccion = input("Sección: ")

        print("\n--- Creando un nuevo maestro ---")
        self.interfaz_maestro.agregar()
        if len(self.interfaz_maestro.maestros.items) > 0:
            maestro = self.interfaz_maestro.maestros.items[-1]
        else:
            print("No se pudo crear el maestro.")
            return

        grupo = Grupo(nombre, grado, seccion, maestro)

        agregar_mas = input("¿Deseas agregar alumnos? (s/n): ").lower()
        if agregar_mas == "s":
            print("\n--- Gestionando alumnos para el grupo ---")
            temp_alumnos = grupo.alumnos
            
            interfaz_alumno = AlumnoUI(temp_alumnos)
            interfaz_alumno.menu()

            grupo.alumnos = self.interfaz_alumno.alumnos

        self.grupos.agregar(grupo)

        if self.guardar:
            self.grupos.guardarArchivo(self.archivo)
            print("Grupo agregado y guardado en archivo.")
        else:
            print("Grupo agregado (modo objeto).")

    def eliminar_grupo(self):
        try:
            indice = int(input("Índice del grupo a eliminar: "))
            if self.grupos.eliminar(indice=indice):
                if self.guardar:
                    self.grupos.guardarArchivo(self.archivo)
                print("Grupo eliminado.")
            else:
                print("No se pudo eliminar el grupo.")
        except ValueError:
            print("Índice inválido.")

    def actualizar_grupo(self):
        try:
            indice = int(input("Índice del grupo a actualizar: "))
            if 0 <= indice < len(self.grupos.items):
                grupo = self.grupos.items[indice]
                print("Deja en blanco si no deseas cambiar un campo.")

                nombre = input(f"Nombre ({grupo.nombre}): ") or grupo.nombre
                grado = input(f"Grado ({grupo.grado}): ") or grupo.grado
                seccion = input(f"Sección ({grupo.seccion}): ") or grupo.seccion

                grupo.nombre = nombre
                grupo.grado = grado
                grupo.seccion = seccion

                actualizar_maestro = input("¿Deseas actualizar al maestro? (s/n): ").lower()
                if actualizar_maestro == "s":
                    print("\n--- Actualizando maestro ---")
                    temp_maestros = Maestro()
                    temp_maestros.agregar(grupo.maestro)
                    self.interfaz_maestro.maestros = temp_maestros
                    self.interfaz_maestro.menu()
                    if len(self.interfaz_maestro.maestros.items) > 0:
                        grupo.maestro = self.interfaz_maestro.maestros.items[0]
                    else:
                        print("No se pudo actualizar el maestro, manteniendo el original.")

                actualizar_alumnos = input("¿Deseas gestionar los alumnos del grupo? (s/n): ").lower()
                if actualizar_alumnos == "s":
                    print("\n--- Gestionando alumnos del grupo ---")
                    temp_alumnos = grupo.alumnos
                    self.interfaz_alumno.alumnos = temp_alumnos
                    self.interfaz_alumno.menu()
                    grupo.alumnos = self.interfaz_alumno.alumnos

                if self.guardar:
                    self.grupos.guardarArchivo(self.archivo)
                print("Grupo actualizado.")
            else:
                print("Índice fuera de rango.")
        except ValueError:
            print("Entrada inválida.")