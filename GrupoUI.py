from grupo import Grupo
from maestro import Maestro
from alumno import Alumno
from MaestroUI import MaestroUI
from AlumnoUI import AlumnoUI
import json
import os

class GrupoUI:
    def __init__(self, grupos=None, archivo="grupos.json"):
        self.archivo = archivo
        self.guardar = True if archivo else False

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
        # Datos básicos del grupo
        nombre = input("Nombre del grupo: ")
        grado = input("Grado: ")
        seccion = input("Sección: ")
        
        # Crear grupo vacío (sin maestro ni alumnos todavía)
        grupo = Grupo(nombre, grado, seccion, None, [])
        grupo.alumnos = Alumno()
        grupo.alumnos.es_objeto = True
        grupo.alumnos.items = []
        
        # Asignar maestro usando la interfaz de maestros
        print("\n--- Asignación de maestro ---")
        print("1. Seleccionar maestro existente")
        print("2. Crear nuevo maestro")
        opcion_maestro = input("Seleccione una opción: ")
        
        if opcion_maestro == "1":
            # Cargar maestros existentes
            maestros_sistema = Maestro()
            maestros_sistema.cargarArchivo("maestros.json", Maestro)
            
            if not maestros_sistema.items:
                print("No hay maestros registrados. Debe crear uno nuevo.")
                opcion_maestro = "2"
            else:
                # Mostrar lista para selección
                print("\n=== Maestros disponibles ===")
                for i, m in enumerate(maestros_sistema.items):
                    print(f"{i}. {m}")
                    
                try:
                    idx = int(input("Seleccione el índice del maestro: "))
                    if 0 <= idx < len(maestros_sistema.items):
                        grupo.maestro = maestros_sistema.items[idx]
                        print(f"Maestro {grupo.maestro.nombre} {grupo.maestro.apellido} asignado al grupo.")
                    else:
                        print("Índice inválido. Se creará un nuevo maestro.")
                        opcion_maestro = "2"
                except ValueError:
                    print("Entrada inválida. Se creará un nuevo maestro.")
                    opcion_maestro = "2"
        
        if opcion_maestro == "2":
            # Usar la interfaz de maestros para crear uno nuevo
            print("\n--- Creando nuevo maestro para el grupo ---")
            maestro_ui = MaestroUI(Maestro(), "maestros.json")
            
            # Guardar el modo actual
            modo_guardar_original = maestro_ui.guardar
            maestro_ui.guardar = True  # Forzar guardar
            
            # Agregar maestro con la interfaz existente
            maestro_ui.agregar()
            
            # Restaurar modo original
            maestro_ui.guardar = modo_guardar_original
            
            # Cargar maestros para obtener el recién creado
            maestros_temp = Maestro()
            maestros_temp.cargarArchivo("maestros.json", Maestro)
            if maestros_temp.items:
                grupo.maestro = maestros_temp.items[-1]  # El último es el recién creado
                print(f"Maestro {grupo.maestro.nombre} {grupo.maestro.apellido} creado y asignado al grupo.")
            else:
                print("Error al crear maestro. El grupo se creará sin maestro asignado.")
        
        # Agregar alumnos al grupo
        gestionar_alumnos = input("\n¿Desea agregar alumnos al grupo? (s/n): ").lower()
        if gestionar_alumnos == 's':
            self.gestionar_alumnos_grupo(grupo)
        
        # Guardar el grupo
        self.grupos.agregar(grupo)
        if self.guardar:
            self.grupos.guardarArchivo(self.archivo)
        print(f"Grupo '{nombre}' creado exitosamente.")

    def gestionar_alumnos_grupo(self, grupo):
        """Gestiona los alumnos de un grupo utilizando la interfaz de alumnos existente"""
        while True:
            print("\n--- Gestión de Alumnos del Grupo ---")
            print("1. Ver alumnos actuales del grupo")
            print("2. Agregar alumnos existentes")
            print("3. Crear nuevo alumno")
            print("4. Eliminar alumno del grupo")
            print("5. Volver al menú anterior")
            
            opcion = input("Seleccione una opción: ")
            
            if opcion == "1":
                # Ver alumnos del grupo
                if not grupo.alumnos.items:
                    print("No hay alumnos en este grupo.")
                else:
                    print("\n=== Alumnos del Grupo ===")
                    for i, alumno in enumerate(grupo.alumnos.items):
                        print(f"{i}. {alumno}")
            
            elif opcion == "2":
                # Agregar alumnos existentes al grupo
                alumnos_sistema = Alumno()
                alumnos_sistema.cargarArchivo("alumnos.json", Alumno)
                
                if not alumnos_sistema.items:
                    print("No hay alumnos registrados en el sistema.")
                    continue
                
                # Mostrar alumnos disponibles
                print("\n=== Alumnos Disponibles ===")
                for i, alumno in enumerate(alumnos_sistema.items):
                    print(f"{i}. {alumno}")
                
                try:
                    indices = input("Ingrese índices de alumnos a agregar (separados por coma): ")
                    if indices.strip():
                        for idx in [int(i.strip()) for i in indices.split(",")]:
                            if 0 <= idx < len(alumnos_sistema.items):
                                alumno = alumnos_sistema.items[idx]
                                # Verificar si ya está en el grupo
                                ya_existe = False
                                for a in grupo.alumnos.items:
                                    if a.matricula == alumno.matricula:
                                        ya_existe = True
                                        break
                                
                                if not ya_existe:
                                    grupo.alumnos.items.append(alumno)
                                    print(f"Alumno {alumno.nombre} agregado al grupo.")
                                else:
                                    print(f"Alumno {alumno.nombre} ya está en el grupo.")
                            else:
                                print(f"Índice {idx} fuera de rango.")
                    
                    if self.guardar:
                        self.grupos.guardarArchivo(self.archivo)
                except ValueError:
                    print("Formato inválido. Use números separados por comas.")
            
            elif opcion == "3":
                # Crear nuevo alumno usando la interfaz existente
                print("\n--- Creando nuevo alumno para el grupo ---")
                alumno_ui = AlumnoUI(Alumno(), "alumnos.json")
                
                # Guardar modo original
                modo_guardar_original = alumno_ui.guardar
                alumno_ui.guardar = True  # Forzar guardar
                
                # Usar el método existente para crear alumno
                alumno_ui.agregar_alumno()
                
                # Restaurar modo
                alumno_ui.guardar = modo_guardar_original
                
                # Obtener el alumno recién creado
                alumnos_temp = Alumno()
                alumnos_temp.cargarArchivo("alumnos.json", Alumno)
                if alumnos_temp.items:
                    nuevo_alumno = alumnos_temp.items[-1]  # El último es el recién creado
                    grupo.alumnos.items.append(nuevo_alumno)
                    print(f"Alumno {nuevo_alumno.nombre} creado y agregado al grupo.")
                
                if self.guardar:
                    self.grupos.guardarArchivo(self.archivo)
            
            elif opcion == "4":
                # Eliminar alumno del grupo
                if not grupo.alumnos.items:
                    print("No hay alumnos en este grupo.")
                    continue
                
                print("\n=== Alumnos del Grupo ===")
                for i, alumno in enumerate(grupo.alumnos.items):
                    print(f"{i}. {alumno}")
                
                try:
                    idx = int(input("Índice del alumno a eliminar: "))
                    if 0 <= idx < len(grupo.alumnos.items):
                        alumno = grupo.alumnos.items[idx]
                        grupo.alumnos.items.pop(idx)
                        print(f"Alumno {alumno.nombre} eliminado del grupo.")
                        
                        if self.guardar:
                            self.grupos.guardarArchivo(self.archivo)
                    else:
                        print("Índice fuera de rango.")
                except ValueError:
                    print("Entrada inválida.")
            
            elif opcion == "5":
                # Volver al menú anterior
                return
            
            else:
                print("Opción no válida.")

    def eliminar_grupo(self):
        if not self.grupos.items:
            print("No hay grupos para eliminar.")
            return
            
        # Mostrar grupos
        print("\n=== Grupos disponibles ===")
        for i, grupo in enumerate(self.grupos.items):
            print(f"{i}. {grupo}")
            
        try:
            indice = int(input("Índice del grupo a eliminar: "))
            if 0 <= indice < len(self.grupos.items):
                grupo = self.grupos.items[indice]
                confirmacion = input(f"¿Está seguro de eliminar el grupo '{grupo.nombre}'? (s/n): ").lower()
                
                if confirmacion == 's':
                    self.grupos.eliminar(indice=indice)
                    print("Grupo eliminado correctamente.")
                    
                    if self.guardar:
                        self.grupos.guardarArchivo(self.archivo)
            else:
                print("Índice fuera de rango.")
        except ValueError:
            print("Entrada inválida.")

    def actualizar_grupo(self):
        if not self.grupos.items:
            print("No hay grupos para actualizar.")
            return
            
        # Mostrar grupos
        print("\n=== Grupos disponibles ===")
        for i, grupo in enumerate(self.grupos.items):
            print(f"{i}. {grupo}")
            
        try:
            indice = int(input("Índice del grupo a actualizar: "))
            if 0 <= indice < len(self.grupos.items):
                grupo = self.grupos.items[indice]
                
                print("\n--- Actualización de Grupo ---")
                print("Deje en blanco los campos que no desea modificar.")
                
                nombre = input(f"Nombre ({grupo.nombre}): ") or grupo.nombre
                grado = input(f"Grado ({grupo.grado}): ") or grupo.grado
                seccion = input(f"Sección ({grupo.seccion}): ") or grupo.seccion
                
                grupo.nombre = nombre
                grupo.grado = grado
                grupo.seccion = seccion
                
                # Preguntar si desea actualizar el maestro
                actualizar_maestro = input("¿Desea actualizar el maestro? (s/n): ").lower()
                if actualizar_maestro == 's':
                    print("\n--- Opciones para el maestro ---")
                    print("1. Seleccionar otro maestro")
                    print("2. Editar maestro actual")
                    opcion_maestro = input("Seleccione una opción: ")
                    
                    if opcion_maestro == "1":
                        # Usar el mismo código de selección de maestro de agregar_grupo
                        maestros_sistema = Maestro()
                        maestros_sistema.cargarArchivo("maestros.json", Maestro)
                        
                        if not maestros_sistema.items:
                            print("No hay maestros registrados.")
                        else:
                            print("\n=== Maestros disponibles ===")
                            for i, m in enumerate(maestros_sistema.items):
                                print(f"{i}. {m}")
                                
                            try:
                                idx = int(input("Seleccione el índice del maestro: "))
                                if 0 <= idx < len(maestros_sistema.items):
                                    grupo.maestro = maestros_sistema.items[idx]
                                    print(f"Maestro {grupo.maestro.nombre} asignado al grupo.")
                                else:
                                    print("Índice inválido.")
                            except ValueError:
                                print("Entrada inválida.")
                    
                    elif opcion_maestro == "2" and hasattr(grupo, 'maestro') and grupo.maestro:
                        # Editar el maestro actual usando la interfaz de maestros
                        print("\n--- Editando maestro actual ---")
                        maestros_temp = Maestro()
                        maestros_temp.agregar(grupo.maestro)
                        
                        maestro_ui = MaestroUI(maestros_temp, "maestros.json")
                        modo_guardar_original = maestro_ui.guardar
                        maestro_ui.guardar = True
                        
                        # Editar directamente el primer (y único) maestro en la lista
                        indice_maestro = 0
                        maestro_ui.actualizar_maestro(indice_maestro)
                        
                        # Restaurar modo
                        maestro_ui.guardar = modo_guardar_original
                
                # Preguntar si desea gestionar alumnos
                gestionar_alumnos = input("¿Desea gestionar los alumnos del grupo? (s/n): ").lower()
                if gestionar_alumnos == 's':
                    self.gestionar_alumnos_grupo(grupo)
                
                if self.guardar:
                    self.grupos.guardarArchivo(self.archivo)
                print("Grupo actualizado correctamente.")
            else:
                print("Índice fuera de rango.")
        except ValueError:
            print("Entrada inválida.")