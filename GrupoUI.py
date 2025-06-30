from grupo import Grupo
from maestro import Maestro
from alumno import Alumno
from MaestroUI import MaestroUI
from AlumnoUI import AlumnoUI
from conexion import conectar_mongo
import os
import json

class GrupoUI:
    def __init__(self, grupos=None, archivo="grupos.json"):
        self.archivo = archivo
        self.guardar = False
        
        if grupos is not None and len(grupos.items) > 0:
            self.grupos = grupos
            print("Usando clase grupo proporcionada.")
        elif archivo and os.path.exists(archivo):
            print(f"Cargando grupos desde archivo '{archivo}'.")
            self.grupos = Grupo()
            self.grupos.cargarArchivo(archivo, Grupo)
            self.guardar = True
        else:
            print("No se proporcionó archivo ni objeto con datos. Creando lista vacía.")
            self.grupos = Grupo()
        
        # Interfaces para reutilización
        self.interfaz_maestro = MaestroUI(Maestro(), "maestros.json")
        self.interfaz_alumno = AlumnoUI(Alumno(), "alumnos.json")
        
        # Lista para datos offline
        self.grupos_offline = Grupo()

    def menu(self):
        while True:
            print("\n--- Menú de Grupos ---")
            print("1. Mostrar grupos")
            print("2. Agregar grupo")
            print("3. Eliminar grupo")
            print("4. Actualizar grupo")
            print("5. Sincronizar con MongoDB")
            print("6. Volver al menú principal")

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
                self.sincronizar_mongo()
            elif opcion == "6":
                if self.guardar:
                    self.grupos.guardarArchivo(self.archivo)
                break
            else:
                print("Opción inválida.")

    def mostrar_grupos(self):
        if not self.grupos.items:
            print("No hay grupos registrados.")
            return
            
        print("\n=== Lista de Grupos ===")
        for i, grupo in enumerate(self.grupos.items):
            print(f"{i}. {grupo}")
            
        ver_detalle = input("¿Desea ver detalle de algún grupo? (s/n): ").lower()
        if ver_detalle == 's':
            try:
                indice = int(input("Índice del grupo a ver en detalle: "))
                if 0 <= indice < len(self.grupos.items):
                    self.grupos.items[indice].mostrar()
                else:
                    print("Índice fuera de rango.")
            except ValueError:
                print("Entrada inválida.")

    def agregar_grupo(self):
        nombre = input("Nombre del grupo: ")
        grado = input("Grado: ")
        seccion = input("Sección: ")
        
        # Crear grupo básico
        grupo = Grupo(nombre, grado, seccion)
        
        # Asignar maestro usando la interfaz existente
        print("\n--- Creando un nuevo maestro ---")
        self.interfaz_maestro.agregar()
        
        if len(self.interfaz_maestro.maestros.items) > 0:
            grupo.maestro = self.interfaz_maestro.maestros.items[-1]
        else:
            print("No se pudo crear el maestro.")
            return
        
        # Gestionar alumnos usando la interfaz existente
        agregar_alumnos = input("¿Deseas agregar alumnos al grupo? (s/n): ").lower()
        if agregar_alumnos == 's':
            # CORRECCIÓN: Crear interfaz temporal pero mantener la referencia al grupo
            print("\n--- Gestionando alumnos del grupo ---")
            interfaz_alumno_grupo = AlumnoUI(grupo.alumnos)  # Usar los alumnos del grupo
            interfaz_alumno_grupo.menu()
            
            # IMPORTANTE: Los alumnos ya están en grupo.alumnos después del menú
            # No necesitas hacer nada más, la referencia se mantiene
            print(f"Total de alumnos en el grupo: {len(grupo.alumnos.items)}")
        
        # Agregar grupo a la lista
        self.grupos.agregar(grupo)
        
        # Guardar en archivo si corresponde
        if self.guardar:
            self.grupos.guardarArchivo(self.archivo)
        
        # Agregar a lista offline
        self.grupos_offline.agregar(grupo)
        self.guardar_en_mongo_o_local(grupo)
        
        print(f"Grupo '{nombre}' agregado.")

    def eliminar_grupo(self):
        try:
            if not self.grupos.items:
                print("No hay grupos para eliminar.")
                return
                
            self.mostrar_grupos()
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
            if not self.grupos.items:
                print("No hay grupos para actualizar.")
                return
                
            self.mostrar_grupos()
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
                
                # Actualizar maestro usando la interfaz existente
                actualizar_maestro = input("¿Deseas actualizar al maestro? (s/n): ").lower()
                if actualizar_maestro == 's':
                    print("\n--- Actualizando maestro ---")
                    # Crear interfaz temporal con el maestro actual
                    maestros_temp = Maestro()
                    maestros_temp.agregar(grupo.maestro)
                    interfaz_maestro_temp = MaestroUI(maestros_temp)
                    interfaz_maestro_temp.menu()
                    # Actualizar el maestro del grupo
                    if len(maestros_temp.items) > 0:
                        grupo.maestro = maestros_temp.items[0]

                # Gestionar alumnos usando la interfaz existente
                gestionar_alumnos = input("¿Deseas gestionar los alumnos? (s/n): ").lower()
                if gestionar_alumnos == 's':
                    print("\n--- Gestionando alumnos ---")
                    interfaz_alumno_temp = AlumnoUI(grupo.alumnos)
                    interfaz_alumno_temp.menu()
                    # Los alumnos ya están actualizados en grupo.alumnos
                
                if self.guardar:
                    self.grupos.guardarArchivo(self.archivo)
                print("Grupo actualizado.")
            else:
                print("Índice fuera de rango.")
        except ValueError:
            print("Entrada inválida.")

    def guardar_en_mongo_o_local(self, grupo):
        try:
            client = conectar_mongo()
            if client:
                db = client["Escuela"]
                collection = db["grupos"]
                data = grupo.convertir_diccionario()
                result = collection.insert_one(data)
                print(f"Documento insertado en MongoDB con ID: {result.inserted_id}")
                # Limpiar de offline ya que se envió
                if grupo in self.grupos_offline.items:
                    self.grupos_offline.items.remove(grupo)
                self.limpiar_archivo_offline()
            else:
                # Guardar en archivo offline
                self.guardar_offline(grupo)
                print("No hay conexión. Grupo guardado localmente.")
        except Exception as e:
            print(f"Error: {e}")
            self.guardar_offline(grupo)

    def guardar_offline(self, grupo):
        try:
            archivo_offline = "grupos_sin_enviar.json"
            data = []
            if os.path.exists(archivo_offline):
                with open(archivo_offline, "r", encoding="utf-8") as f:
                    data = json.load(f)
            
            data.append(grupo.convertir_diccionario())
            
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
            
            archivo_offline = "grupos_sin_enviar.json"  # Cambiado aquí
            if not os.path.exists(archivo_offline):
                print("No hay datos offline para sincronizar.")
                return
            
            with open(archivo_offline, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            if not data:
                print("No hay datos offline para sincronizar.")
                return
            
            db = client["Escuela"]
            collection = db["grupos"]
            
            if len(data) == 1:
                collection.insert_one(data[0])
            else:
                collection.insert_many(data)
            
            print(f"Se sincronizaron {len(data)} grupos con MongoDB.")
            
            # Limpiar archivo offline
            with open(archivo_offline, "w", encoding="utf-8") as f:
                json.dump([], f)
                
        except Exception as e:
            print(f"Error al sincronizar: {e}")

    def limpiar_archivo_offline(self):
        try:
            archivo_offline = "grupos_sin_enviar.json"  # Cambiado aquí
            with open(archivo_offline, "w", encoding="utf-8") as f:
                json.dump([], f)
        except:
            pass