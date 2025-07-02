from conexion import conectar_mongo
from alumno import Alumno
import json
import os

class AlumnoUI:
    def __init__(self, alumnos=None, archivo='alumnos.json'):
        self.archivo = archivo 
        self.guardar = False    

        if alumnos is not None:
            self.alumnos = alumnos if isinstance(alumnos, Alumno) else Alumno()
            print("Usando clase Alumno.")
        elif archivo and os.path.exists(archivo):
            print(f"Cargando alumnos desde archivo '{archivo}'.")
            self.alumnos = Alumno()
            self.alumnos.cargarArchivo(archivo, Alumno)
            self.guardar = True
        else:
            print("No se proporcionó archivo ni objeto con datos. Creando lista vacía.")
            self.alumnos = Alumno()

        self.alumnos_offline = Alumno()
        if os.path.exists('alumnos_offline.json'):
            print("Cargando alumnos offline...")
            self.alumnos_offline.cargarArchivo('alumnos_offline.json', Alumno)

    def menu(self):
        while True:
            print("\n--- Menú de Alumnos ---")
            print("1. Mostrar alumnos")
            print("2. Agregar alumno")
            print("3. Eliminar alumno")
            print("4. Actualizar alumno")
            print("5. Mostrar alumnos offline")
            print("6. Salir")

            opcion = input("Seleccione una opción: ")
            if opcion == "1":
                print(json.dumps(self.alumnos.convertir_diccionario(), indent=4, ensure_ascii=False))
            elif opcion == "2":
                self.agregar_alumno()
            elif opcion == "3":
                self.eliminar_alumno()
            elif opcion == "4":
                self.actualizar_alumno()
            elif opcion == "5":
                print(json.dumps(self.alumnos_offline.convertir_diccionario(), indent=4, ensure_ascii=False))
            elif opcion == "6":
                print("Saliendo del sistema.")
                break
            else:
                print("Opción no válida.")

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
            self.alumnos_offline.agregar(alumno)

        datos_para_guardar = self.alumnos_offline.convertir_diccionario()
        self.guardar_en_mongo_o_local(datos_para_guardar)

    def eliminar_alumno(self):
        try:
            indice = int(input("Índice del alumno a eliminar: "))
            if self.alumnos.eliminar(indice=indice):
                if self.guardar:
                    self.alumnos.guardarArchivo(self.archivo)
                print("Alumno eliminado correctamente.")
            else:
                print("No se pudo eliminar.")
        except ValueError:
            print("Índice inválido.")

    def actualizar_alumno(self):
        try:
            indice = int(input("Índice del alumno a actualizar: "))
            if 0 <= indice < len(self.alumnos.items):
                alumno = self.alumnos.items[indice]
                print("Deja en blanco si no quieres cambiar un campo.")

                nombre = input(f"Nombre ({alumno.nombre}): ") or alumno.nombre
                apellido = input(f"Apellido ({alumno.apellido}): ") or alumno.apellido
                edad = input(f"Edad ({alumno.edad}): ") or alumno.edad
                matricula = input(f"Matrícula ({alumno.matricula}): ") or alumno.matricula
                sexo = input(f"Sexo ({alumno.sexo}): ") or alumno.sexo

                self.alumnos.actualizar(
                    alumno,
                    nombre=nombre,
                    apellido=apellido,
                    edad=int(edad),
                    matricula=matricula,
                    sexo=sexo
                )

                if self.guardar:
                    self.alumnos.guardarArchivo(self.archivo)
                print("Alumno actualizado correctamente.")
            else:
                print("Índice fuera de rango.")
        except ValueError:
            print("Entrada inválida.")

    def guardar_en_mongo_o_local(self, datos):
        client = conectar_mongo()

        if client:
            db = client["Escuela"]
            coleccion = db["Alumnos"]

            try:
                if len(datos) == 1:
                    coleccion.insert_one(datos[0])
                    print("✅ Alumno guardado en MongoDB.")
                else:
                    coleccion.insert_many(datos)
                    print(f"✅ Se sincronizaron {len(datos)} alumnos con MongoDB.")

                self.alumnos_offline.items.clear()
                self.alumnos_offline.guardarArchivo("alumnos_offline.json")
                print("🗑️ Alumnos offline limpiados después de sincronización.")
            except Exception as e:
                print(f"❌ Error al guardar en MongoDB: {e}")
        else:
            self.alumnos_offline.guardarArchivo("alumnos_offline.json")
            print("⚠️ No hay conexión. Alumno guardado localmente.")