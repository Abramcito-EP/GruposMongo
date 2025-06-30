from maestro import Maestro
from conexion import conectar_mongo
import os
import json

class MaestroUI:
    def __init__(self, maestros=None, archivo='maestros.json'):
        self.archivo = archivo
        self.guardar = False
        
        if maestros is not None and len(maestros.items) > 0:
            self.maestros = maestros
            print("Usando clase maestro proporcionada.")
        elif archivo and os.path.exists(archivo):
            print(f"Cargando maestros desde archivo '{archivo}'.")
            self.maestros = Maestro()
            self.maestros.cargarArchivo(archivo, Maestro)
            self.guardar = True
        else:
            print("No se proporcionó archivo ni objeto con datos. Creando lista vacía.")
            self.maestros = Maestro()
        
        # Lista para datos offline
        self.maestros_offline = Maestro()

    def menu(self):
        while True:
            print("\n--- Menú de Maestros ---")
            print("1. Mostrar maestros")
            print("2. Agregar maestro")
            print("3. Eliminar maestro")
            print("4. Actualizar maestro")
            print("5. Sincronizar con MongoDB")
            print("6. Volver al menú principal")

            opcion = input("Seleccione una opción: ")
            if opcion == "1":
                self.mostrar_maestros()
            elif opcion == "2":
                self.agregar()
            elif opcion == "3":
                self.eliminar()
            elif opcion == "4":
                self.actualizar()
            elif opcion == "5":
                self.sincronizar_mongo()
            elif opcion == "6":
                if self.guardar:
                    self.maestros.guardarArchivo(self.archivo)
                break
            else:
                print("Opción inválida.")

    def mostrar_maestros(self):
        if not self.maestros.items:
            print("No hay maestros registrados.")
            return
            
        print("\n=== Lista de Maestros ===")
        for i, maestro in enumerate(self.maestros.items):
            print(f"{i}. {maestro}")

    def agregar(self):
        nombre = input("Nombre: ")
        apellido = input("Apellido: ")
        try:
            edad = int(input("Edad: "))
        except ValueError:
            print("Edad inválida, se usará 0")
            edad = 0
        matricula = input("Matrícula: ")
        especialidad = input("Especialidad: ")
        
        maestro = Maestro(nombre, apellido, edad, matricula, especialidad)
        
        # Agregar a lista principal
        self.maestros.agregar(maestro)
        
        # Guardar en archivo si corresponde
        if self.guardar:
            self.maestros.guardarArchivo(self.archivo)
        
        # Agregar a lista offline
        self.maestros_offline.agregar(maestro)
        self.guardar_en_mongo_o_local(maestro)
        
        print("Maestro agregado.")

    def eliminar(self):
        try:
            if not self.maestros.items:
                print("No hay maestros para eliminar.")
                return
                
            self.mostrar_maestros()
            indice = int(input("Índice del maestro a eliminar: "))
            if self.maestros.eliminar(indice=indice):
                if self.guardar:
                    self.maestros.guardarArchivo(self.archivo)
                print("Maestro eliminado.")
            else:
                print("No se pudo eliminar el maestro.")
        except ValueError:
            print("Índice inválido.")

    def actualizar(self):
        try:
            if not self.maestros.items:
                print("No hay maestros para actualizar.")
                return
                
            self.mostrar_maestros()
            indice = int(input("Índice del maestro a actualizar: "))
            if 0 <= indice < len(self.maestros.items):
                maestro = self.maestros.items[indice]
                print("Deja en blanco si no deseas cambiar un campo.")
                
                nombre = input(f"Nombre ({maestro.nombre}): ") or maestro.nombre
                apellido = input(f"Apellido ({maestro.apellido}): ") or maestro.apellido
                edad_str = input(f"Edad ({maestro.edad}): ")
                edad = int(edad_str) if edad_str else maestro.edad
                matricula = input(f"Matrícula ({maestro.matricula}): ") or maestro.matricula
                especialidad = input(f"Especialidad ({maestro.especialidad}): ") or maestro.especialidad
                
                maestro.nombre = nombre
                maestro.apellido = apellido
                maestro.edad = edad
                maestro.matricula = matricula
                maestro.especialidad = especialidad
                
                if self.guardar:
                    self.maestros.guardarArchivo(self.archivo)
                print("Maestro actualizado.")
            else:
                print("Índice fuera de rango.")
        except ValueError:
            print("Entrada inválida.")

    def guardar_en_mongo_o_local(self, maestro):
        try:
            client = conectar_mongo()
            if client:
                db = client["Escuela"]
                collection = db["maestros"]
                data = maestro.convertir_diccionario()
                result = collection.insert_one(data)
                print(f"Maestro enviado a MongoDB con ID: {result.inserted_id}")
                # Limpiar de offline ya que se envió
                if maestro in self.maestros_offline.items:
                    self.maestros_offline.items.remove(maestro)
                self.limpiar_archivo_offline()
            else:
                # Guardar en archivo offline
                self.guardar_offline(maestro)
                print("No hay conexión. Maestro guardado localmente.")
        except Exception as e:
            print(f"Error: {e}")
            self.guardar_offline(maestro)

    def guardar_offline(self, maestro):
        try:
            archivo_offline = "maestros_sin_enviar.json"  # Cambiado aquí
            data = []
            if os.path.exists(archivo_offline):
                with open(archivo_offline, "r", encoding="utf-8") as f:
                    data = json.load(f)
            
            data.append(maestro.convertir_diccionario())
            
            with open(archivo_offline, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
                
        except Exception as e:
            print(f"Error al guardar offline: {e}")

    def sincronizar_mongo(self):
        try:
            client = conectar_mongo()
            if not client:
                print("No hay conexión a MongoDB.")
                return
            
            archivo_offline = "maestros_sin_enviar.json"  # Cambiado aquí
            if not os.path.exists(archivo_offline):
                print("No hay datos offline para sincronizar.")
                return
            
            with open(archivo_offline, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            if not data:
                print("No hay datos offline para sincronizar.")
                return
            
            db = client["Escuela"]
            collection = db["maestros"]
            
            if len(data) == 1:
                collection.insert_one(data[0])
            else:
                collection.insert_many(data)
            
            print(f"Se sincronizaron {len(data)} maestros con MongoDB.")
            
            # Limpiar archivo offline
            with open(archivo_offline, "w", encoding="utf-8") as f:
                json.dump([], f)
                
        except Exception as e:
            print(f"Error al sincronizar: {e}")

    def limpiar_archivo_offline(self):
        try:
            archivo_offline = "maestros_sin_enviar.json"  # Cambiado aquí
            with open(archivo_offline, "w", encoding="utf-8") as f:
                json.dump([], f)
        except:
            pass