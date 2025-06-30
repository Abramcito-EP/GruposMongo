from alumno import Alumno
from conexion import conectar_mongo
import os
import json

class AlumnoUI:
    def __init__(self, alumnos=None, archivo='alumnos.json'):
        self.archivo = archivo
        self.guardar = False
        
        if alumnos is not None and hasattr(alumnos, 'items'):
            # CORRECCIÓN: Si se pasa un objeto Alumno (contenedor), usarlo directamente
            self.alumnos = alumnos
            print("Usando clase alumno proporcionada.")
            # No cargar desde archivo si ya tienes un objeto
        elif archivo and os.path.exists(archivo):
            print(f"Cargando alumnos desde archivo '{archivo}'.")
            self.alumnos = Alumno()
            self.alumnos.cargarArchivo(archivo, Alumno)
            self.guardar = True
        else:
            print("No se proporcionó archivo ni objeto con datos. Creando lista vacía.")
            self.alumnos = Alumno()
        
        # Lista para datos offline
        self.alumnos_offline = Alumno()

    def menu(self):
        while True:
            print("\n--- Menú de Alumnos ---")
            print("1. Mostrar alumnos")
            print("2. Agregar alumno")
            print("3. Eliminar alumno")
            print("4. Actualizar alumno")
            print("5. Sincronizar con MongoDB")
            print("6. Volver al menú principal")

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
                self.sincronizar_mongo()
            elif opcion == "6":
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
        try:
            edad = int(input("Edad: "))
        except ValueError:
            print("Edad inválida, se usará 0")
            edad = 0
        matricula = input("Matrícula: ")
        sexo = input("Sexo (M/F): ")
        
        alumno = Alumno(nombre, apellido, edad, matricula, sexo)
        
        # CORRECCIÓN: Agregar a la lista de alumnos (que puede ser del grupo)
        self.alumnos.agregar(alumno)
        
        # Guardar en archivo SOLO si estamos manejando el archivo principal
        if self.guardar:
            self.alumnos.guardarArchivo(self.archivo)
        
        # Agregar a lista offline para MongoDB
        self.alumnos_offline.agregar(alumno)
        self.guardar_en_mongo_o_local(alumno)
        
        print("Alumno agregado.")

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

    def guardar_en_mongo_o_local(self, alumno):
        try:
            client = conectar_mongo()
            if client:
                db = client["Escuela"]
                collection = db["alumnos"]
                data = alumno.convertir_diccionario()
                result = collection.insert_one(data)
                print(f"Documento insertado en MongoDB con ID: {result.inserted_id}")
                # Limpiar de offline ya que se envió
                if alumno in self.alumnos_offline.items:
                    self.alumnos_offline.items.remove(alumno)
                self.limpiar_archivo_offline()
            else:
                # Guardar en archivo offline
                self.guardar_offline(alumno)
                print("No hay conexión. Alumno guardado localmente.")
        except Exception as e:
            print(f"Error: {e}")
            self.guardar_offline(alumno)

    def guardar_offline(self, alumno):
        try:
            archivo_offline = "alumnos_sin_enviar.json"
            data = []
            if os.path.exists(archivo_offline):
                with open(archivo_offline, "r", encoding="utf-8") as f:
                    data = json.load(f)
            
            data.append(alumno.convertir_diccionario())
            
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
            
            archivo_offline = "alumnos_sin_enviar.json"  # Cambiado aquí
            if not os.path.exists(archivo_offline):
                print("No hay datos offline para sincronizar.")
                return
            
            with open(archivo_offline, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            if not data:
                print("No hay datos offline para sincronizar.")
                return
            
            db = client["Escuela"]
            collection = db["alumnos"]
            
            if len(data) == 1:
                collection.insert_one(data[0])
            else:
                collection.insert_many(data)
            
            print(f"Se sincronizaron {len(data)} alumnos con MongoDB.")
            
            # Limpiar archivo offline
            with open(archivo_offline, "w", encoding="utf-8") as f:
                json.dump([], f)
                
        except Exception as e:
            print(f"Error al sincronizar: {e}")

    def limpiar_archivo_offline(self):
        try:
            archivo_offline = "alumnos_sin_enviar.json"  # Cambiado aquí
            with open(archivo_offline, "w", encoding="utf-8") as f:
                json.dump([], f)
        except:
            pass