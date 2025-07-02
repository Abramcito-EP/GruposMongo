from maestro import Maestro
from conexion import conectar_mongo
import json
import os

class MaestroUI:
    def __init__(self, maestros=None, archivo='maestros.json'):
        self.archivo = archivo
        self.guardar = False

        if maestros is not None and len(maestros.items) > 0:
            self.maestros = maestros
            print("Usando clase maestros.")
        elif archivo and os.path.exists(archivo):
            print(f"Cargando maestros desde archivo '{archivo}'.")
            self.maestros = Maestro()
            self.maestros.cargarArchivo(archivo, Maestro)
            self.guardar = True
        else:
            print("No se proporcionó archivo ni objeto con datos. Creando lista vacía.")
            self.maestros = Maestro()

        self.maestros_offline = Maestro()
        if os.path.exists('maestros_offline.json'):
            print("Cargando maestros offline...")
            self.maestros_offline.cargarArchivo('maestros_offline.json', Maestro)

    def menu(self):
        while True:
            print("\n--- Menú de Maestros ---")
            print("1. Mostrar maestros")
            print("2. Agregar maestros")
            print("3. Eliminar maestros")
            print("4. Actualizar maestros")
            print("5. Mostrar maestros offline")
            print("6. Salir")

            opcion = input("Seleccione una opción: ")
            if opcion == "1":
                print(json.dumps(self.maestros.convertir_diccionario(), indent=4, ensure_ascii=False))
            elif opcion == "2":
                self.agregar()
            elif opcion == "3":
                self.eliminar()
            elif opcion == "4":
                self.actualizar()
            elif opcion == "5":
                print(json.dumps(self.maestros_offline.convertir_diccionario(), indent=4, ensure_ascii=False))
            elif opcion == "6":
                print("Saliendo del sistema.")
                break
            else:
                print("Opción no válida.")

    def agregar(self):
        nombre = input("Nombre: ")
        apellido = input("Apellido: ")
        edad = int(input("Edad: "))
        matricula = input("Matrícula: ")
        especialidad = input("Especialidad: ")
        maestro= Maestro(nombre, apellido, edad, matricula, especialidad)

        self.maestros.agregar(maestro)

        if self.guardar:
            self.maestros.guardarArchivo(self.archivo)
            self.maestros_offline.agregar(maestro)

        datos_para_guardar = self.maestros_offline.convertir_diccionario()
        self.guardar_en_mongo_o_local(datos_para_guardar)

    def eliminar(self):
        try:
            indice = int(input("Índice del maestro a eliminar: "))
            if self.maestros.eliminar(indice=indice):
                if self.guardar:
                    self.maestros.guardarArchivo(self.archivo)
                print("Maestro eliminado correctamente.")
            else:
                print("No se pudo eliminar.")
        except ValueError:
            print("Índice inválido.")

    def actualizar(self):
        try:
            indice = int(input("Índice del maestro a actualizar: "))
            if 0 <= indice < len(self.maestros.items):
                maestro = self.maestros.items[indice]
                print("Deja en blanco si no quieres cambiar un campo.")

                nombre = input(f"Nombre ({maestro.nombre}): ") or maestro.nombre
                apellido = input(f"Apellido ({maestro.apellido}): ") or maestro.apellido
                edad_input = input(f"Edad ({maestro.edad}): ")
                edad = int(edad_input) if edad_input else maestro.edad
                matricula = input(f"Matrícula ({maestro.matricula}): ") or maestro.matricula
                especialidad = input(f"Especialidad ({maestro.especialidad}): ") or maestro.especialidad

                self.maestros.actualizar(
                    maestro,
                    nombre=nombre,
                    apellido=apellido,
                    edad=edad,
                    matricula=matricula,
                    especialidad=especialidad
                )

                if self.guardar:
                    self.maestros.guardarArchivo(self.archivo)
                print("Maestro actualizado correctamente.")
            else:
                print("Índice fuera de rango.")
        except ValueError:
            print("Entrada inválida.")

    def guardar_en_mongo_o_local(self, datos):
        client = conectar_mongo()

        if client:
            db = client["Escuela"]
            coleccion = db["Maestros"]

            try:
                if len(datos) == 1:
                    coleccion.insert_one(datos[0])
                    print("✅ Maestro guardado en MongoDB.")
                else:
                    coleccion.insert_many(datos)
                    print(f"✅ Se sincronizaron {len(datos)} maestros con MongoDB.")

                self.maestros_offline.items.clear()
                self.maestros_offline.guardarArchivo("maestros_offline.json")
                print("🗑️ Maestros offline limpiados después de sincronización.")
            except Exception as e:
                print(f"❌ Error al guardar en MongoDB: {e}")
        else:
            self.maestros_offline.guardarArchivo("maestros_offline.json")
            print("⚠️ No hay conexión. Maestro guardado localmente.")