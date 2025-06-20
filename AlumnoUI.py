from alumno import Alumno
import os
import json

class AlumnoUI:
    def _init_(self, alumnos=None, archivo='alumnos.json'):
        self.archivo = archivo 
        self.guardar = False    
        if alumnos is not None:
            if isinstance(alumnos, Alumno):
                self.alumnos = alumnos
            else:
                self.alumnos = Alumno()
                for alumno in alumnos:
                    self.alumnos.agregar(alumno)
            print("Usando clase alumno.")
        elif archivo and os.path.exists(archivo):
            print(f"Cargando alumnos desde archivo '{archivo}'.")
            self.alumnos = Alumno()
            self.alumnos.cargarArchivo(archivo, Alumno)
            self.guardar = True
        else:
            print("No se proporcionó archivo ni objeto con datos. Creando lista vacía.")
            self.alumnos = Alumno()

    def menu(self):
        while True:
            print("\n--- Menú de Alumnos ---")
            print("1. Mostrar alumnos")
            print("2. Agregar alumno")
            print("3. Eliminar alumno")
            print("4. Actualizar alumno")
            print("5. Volver al menú principal")

            opcion = input("Seleccione una opción: ")
            if opcion == "1":
                self.mostrar_alumnos()
            elif opcion == "2":
                self.agregar_alumno()
            elif opcion == "3":
                self.eliminar_alumno()
            elif opcion == "4":
                self.actualizar_alumno()
            elif opcion == "5":
                if self.guardar:
                    self.alumnos.guardarArchivo(self.archivo)
                break
            else:
                print("Opción inválida.")

    def mostrar_alumnos(self):
        if not self.alumnos.items:
            print("No hay alumnos registrados.")
            return
            
        print("\n=== Lista de Alumnos ===")
        for i, alumno in enumerate(self.alumnos.items):
            print(f"{i}. {alumno}")

    def agregar_alumno(self):
        nombre = input("Nombre: ")
        apellido = input("Apellido: ")
        edad = int(input("Edad: "))
        matricula = input("Matrícula: ")
        sexo = input("Sexo (M/F): ")
        alumno = Alumno(nombre, apellido, edad, matricula, sexo)

        self.alumnos.agregar(alumno)

        if self.guardar:
            self.alumnos.guardarArchivo(self.archivo)
            print("Alumno agregado y guardado en archivo.")
        else:
            print("Alumno agregado (modo objeto).")

    def eliminar_alumno(self):
        try:
            if not self.alumnos.items:
                print("No hay alumnos para eliminar.")
                return
                
            self.mostrar_alumnos()
            indice = int(input("Índice del alumno a eliminar: "))
            if self.alumnos.eliminar(indice=indice):
                if self.guardar:
                    self.alumnos.guardarArchivo(self.archivo)
                print("Alumno eliminado.")
            else:
                print("No se pudo eliminar el alumno.")
        except ValueError:
            print("Índice inválido.")

    def actualizar_alumno(self):
        try:
            if not self.alumnos.items:
                print("No hay alumnos para actualizar.")
                return
                
            self.mostrar_alumnos()
            indice = int(input("Índice del alumno a actualizar: "))
            if 0 <= indice < len(self.alumnos.items):
                alumno = self.alumnos.items[indice]
                print("Deja en blanco si no deseas cambiar un campo.")
                
                nombre = input(f"Nombre ({alumno.nombre}): ") or alumno.nombre
                apellido = input(f"Apellido ({alumno.apellido}): ") or alumno.apellido
                edad_str = input(f"Edad ({alumno.edad}): ")
                edad = int(edad_str) if edad_str else alumno.edad
                matricula = input(f"Matrícula ({alumno.matricula}): ") or alumno.matricula
                sexo = input(f"Sexo ({alumno.sexo}): ") or alumno.sexo
                
                alumno.nombre = nombre
                alumno.apellido = apellido
                alumno.edad = edad
                alumno.matricula = matricula
                alumno.sexo = sexo
                
                if self.guardar:
                    self.alumnos.guardarArchivo(self.archivo)
                print("Alumno actualizado.")
            else:
                print("Índice fuera de rango.")
        except ValueError:
            print("Entrada inválida.")