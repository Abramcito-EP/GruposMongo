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

        # Opciones para el maestro
        print("\n--- Opciones para el maestro ---")
        print("1. Seleccionar un maestro existente")
        print("2. Crear un nuevo maestro")
        opcion_maestro = input("Seleccione una opción: ")
        
        maestro = None
        if opcion_maestro == "1":
            # Cargar maestros existentes
            maestros_existentes = Maestro()
            maestros_existentes.cargarArchivo("maestros.json", Maestro)
            
            if not maestros_existentes.items:
                print("No hay maestros registrados en el sistema. Debe crear uno nuevo.")
                opcion_maestro = "2"  # Cambiar a creación de maestro
            else:
                # Mostrar lista de maestros existentes
                print("\n=== Maestros existentes ===")
                for i, maestro_item in enumerate(maestros_existentes.items):
                    print(f"{i}. {maestro_item}")
                
                try:
                    idx = int(input("Índice del maestro a asignar: "))
                    if 0 <= idx < len(maestros_existentes.items):
                        maestro = maestros_existentes.items[idx]
                        print(f"Maestro {maestro.nombre} {maestro.apellido} seleccionado.")
                    else:
                        print("Índice fuera de rango. Debe crear un nuevo maestro.")
                        opcion_maestro = "2"  # Cambiar a creación de maestro
                except ValueError:
                    print("Entrada inválida. Debe crear un nuevo maestro.")
                    opcion_maestro = "2"  # Cambiar a creación de maestro
        
        if opcion_maestro == "2":
            print("\n--- Creando un nuevo maestro ---")
            self.interfaz_maestro.agregar()
            if len(self.interfaz_maestro.maestros.items) > 0:
                maestro = self.interfaz_maestro.maestros.items[-1]
            else:
                print("No se pudo crear el maestro.")
                return
        
        if maestro is None:
            print("No se seleccionó ni creó un maestro. No se puede crear el grupo.")
            return

        # Crear grupo con maestro y sin alumnos
        grupo = Grupo(nombre, grado, seccion, maestro, [])  # Pasamos lista vacía de alumnos
        
        # Asegurarse de que alumnos es un objeto Alumno vacío
        grupo.alumnos = Alumno()
        grupo.alumnos.items = []  # Inicializar explícitamente como vacío

        agregar_alumnos = input("¿Deseas agregar alumnos al grupo? (s/n): ").lower()
        if agregar_alumnos == "s":
            while True:
                print("\n--- Opciones para agregar alumnos ---")
                print("1. Seleccionar alumnos existentes")
                print("2. Crear nuevo alumno para el grupo")
                print("3. Terminar y volver")
                
                opcion = input("Seleccione una opción: ")
                
                if opcion == "1":
                    # Cargar todos los alumnos existentes
                    alumnos_existentes = Alumno()
                    alumnos_existentes.cargarArchivo("alumnos.json", Alumno)
                    
                    if not alumnos_existentes.items:
                        print("No hay alumnos registrados en el sistema.")
                        continue
                    
                    # Mostrar lista de alumnos existentes
                    print("\n=== Alumnos existentes ===")
                    for i, alumno in enumerate(alumnos_existentes.items):
                        print(f"{i}. {alumno}")
                    
                    try:
                        indices = input("Ingrese los índices de los alumnos a agregar (separados por coma): ")
                        if indices.strip():
                            indices_seleccionados = [int(idx.strip()) for idx in indices.split(",")]
                          
                            for idx in indices_seleccionados:
                                if 0 <= idx < len(alumnos_existentes.items):
                                    # Verificar que no esté ya en el grupo
                                    alumno = alumnos_existentes.items[idx]
                                    existe = False
                                    for a in grupo.alumnos.items:
                                        if a.matricula == alumno.matricula:
                                            existe = True
                                            break
                                
                                    if not existe:
                                        grupo.alumnos.agregar(alumno)
                                        print(f"Alumno {alumno.nombre} {alumno.apellido} agregado al grupo.")
                                    else:
                                        print(f"El alumno {alumno.nombre} {alumno.apellido} ya está en el grupo.")
                                else:
                                    print(f"Índice {idx} fuera de rango.")
                    except ValueError:
                        print("Entrada inválida. Debe ingresar números separados por coma.")
            
                elif opcion == "2":
                    # Crear un nuevo alumno
                    print("\n--- Creando nuevo alumno para el grupo ---")
                    nombre_alumno = input("Nombre: ")
                    apellido_alumno = input("Apellido: ")
                    try:
                        edad_alumno = int(input("Edad: "))
                    except ValueError:
                        print("Edad inválida, se usará 0")
                        edad_alumno = 0
                    matricula_alumno = input("Matrícula: ")
                    sexo_alumno = input("Sexo (M/F): ")
                    
                    # Crear el alumno y agregarlo al grupo
                    nuevo_alumno = Alumno(nombre_alumno, apellido_alumno, edad_alumno, matricula_alumno, sexo_alumno)
                    
                    # También agregar a la lista general de alumnos
                    alumnos_sistema = Alumno()
                    alumnos_sistema.cargarArchivo("alumnos.json", Alumno)
                    alumnos_sistema.agregar(nuevo_alumno)
                    alumnos_sistema.guardarArchivo("alumnos.json")
                    
                    # Agregar al grupo
                    grupo.alumnos.agregar(nuevo_alumno)
                    print(f"Alumno {nuevo_alumno.nombre} {nuevo_alumno.apellido} creado y agregado al grupo.")
            
                elif opcion == "3":
                    break
            
                else:
                    print("Opción no válida.")
        
        print(f"Total de alumnos en el grupo: {len(grupo.alumnos.items)}")

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
                    print("\n--- Opciones para actualizar maestro ---")
                    print("1. Seleccionar un maestro existente")
                    print("2. Crear un nuevo maestro")
                    opcion_maestro = input("Seleccione una opción: ")
                    
                    if opcion_maestro == "1":
                        # Cargar maestros existentes
                        maestros_existentes = Maestro()
                        maestros_existentes.cargarArchivo("maestros.json", Maestro)
                        
                        if not maestros_existentes.items:
                            print("No hay maestros registrados en el sistema. Debe crear uno nuevo.")
                            opcion_maestro = "2"  # Cambiar a creación de maestro
                        else:
                            # Mostrar lista de maestros existentes
                            print("\n=== Maestros existentes ===")
                            for i, maestro_item in enumerate(maestros_existentes.items):
                                print(f"{i}. {maestro_item}")
                        
                            try:
                                idx = int(input("Índice del maestro a asignar: "))
                                if 0 <= idx < len(maestros_existentes.items):
                                    grupo.maestro = maestros_existentes.items[idx]
                                    print(f"Maestro {grupo.maestro.nombre} {grupo.maestro.apellido} asignado al grupo.")
                                else:
                                    print("Índice fuera de rango. Se mantendrá el maestro original.")
                            except ValueError:
                                print("Entrada inválida. Se mantendrá el maestro original.")
                    
                    if opcion_maestro == "2":
                        print("\n--- Creando un nuevo maestro ---")
                        temp_maestros = Maestro()
                        temp_maestros.agregar(grupo.maestro)
                        self.interfaz_maestro.maestros = temp_maestros
                        self.interfaz_maestro.menu()
                        if len(self.interfaz_maestro.maestros.items) > 0:
                            grupo.maestro = self.interfaz_maestro.maestros.items[0]
                        else:
                            print("No se pudo crear el maestro, manteniendo el original.")

                gestionar_alumnos = input("¿Deseas gestionar los alumnos del grupo? (s/n): ").lower()
                if gestionar_alumnos == "s":
                    while True:
                        print("\n--- Gestión de alumnos del grupo ---")
                        print("1. Ver alumnos actuales del grupo")
                        print("2. Agregar alumnos existentes")
                        print("3. Crear nuevo alumno para el grupo")
                        print("4. Eliminar alumno del grupo")
                        print("5. Terminar gestión de alumnos")
                        
                        opcion = input("Seleccione una opción: ")
                        
                        if opcion == "1":
                            if not grupo.alumnos.items:
                                print("No hay alumnos en este grupo.")
                            else:
                                print("\n=== Alumnos del grupo ===")
                                for i, alumno in enumerate(grupo.alumnos.items):
                                    print(f"{i}. {alumno}")
                        
                        elif opcion == "2":
                            # Cargar todos los alumnos existentes
                            alumnos_existentes = Alumno()
                            alumnos_existentes.cargarArchivo("alumnos.json", Alumno)
                            
                            if not alumnos_existentes.items:
                                print("No hay alumnos registrados en el sistema.")
                                continue
                            
                            # Mostrar lista de alumnos existentes
                            print("\n=== Alumnos existentes ===")
                            for i, alumno in enumerate(alumnos_existentes.items):
                                print(f"{i}. {alumno}")
                            

                            try:
                                indices = input("Ingrese los índices de los alumnos a agregar (separados por coma): ")
                                if indices.strip():
                                    indices_seleccionados = [int(idx.strip()) for idx in indices.split(",")]
                                    
                                    for idx in indices_seleccionados:
                                        if 0 <= idx < len(alumnos_existentes.items):
                                            # Verificar que no esté ya en el grupo
                                            alumno = alumnos_existentes.items[idx]
                                            existe = False
                                            for a in grupo.alumnos.items:
                                                if hasattr(a, 'matricula') and hasattr(alumno, 'matricula') and a.matricula == alumno.matricula:
                                                    existe = True
                                                    break
                                            
                                            if not existe:
                                                grupo.alumnos.agregar(alumno)
                                                print(f"Alumno {alumno.nombre} {alumno.apellido} agregado al grupo.")
                                            else:
                                                print(f"El alumno {alumno.nombre} {alumno.apellido} ya está en el grupo.")
                                        else:
                                            print(f"Índice {idx} fuera de rango.")
                            except ValueError:
                                print("Entrada inválida. Debe ingresar números separados por coma.")
                        
                        elif opcion == "3":
                            # Crear un nuevo alumno
                            print("\n--- Creando nuevo alumno para el grupo ---")
                            nombre_alumno = input("Nombre: ")
                            apellido_alumno = input("Apellido: ")
                            try:
                                edad_alumno = int(input("Edad: "))
                            except ValueError:
                                print("Edad inválida, se usará 0")
                                edad_alumno = 0
                            matricula_alumno = input("Matrícula: ")
                            sexo_alumno = input("Sexo (M/F): ")
                            
                            # Crear el alumno y agregarlo al grupo
                            nuevo_alumno = Alumno(nombre_alumno, apellido_alumno, edad_alumno, matricula_alumno, sexo_alumno)
                            
                            # También agregar a la lista general de alumnos
                            alumnos_sistema = Alumno()
                            alumnos_sistema.cargarArchivo("alumnos.json", Alumno)
                            alumnos_sistema.agregar(nuevo_alumno)
                            alumnos_sistema.guardarArchivo("alumnos.json")
                            
                            # Agregar al grupo
                            grupo.alumnos.agregar(nuevo_alumno)
                            print(f"Alumno {nuevo_alumno.nombre} {nuevo_alumno.apellido} creado y agregado al grupo.")
                        
                        elif opcion == "4":
                            if not grupo.alumnos.items:
                                print("No hay alumnos en este grupo para eliminar.")
                                continue
                            
                            print("\n=== Alumnos del grupo ===")
                            for i, alumno in enumerate(grupo.alumnos.items):
                                print(f"{i}. {alumno}")
                            

                            try:
                                idx = int(input("Índice del alumno a eliminar del grupo: "))
                                if 0 <= idx < len(grupo.alumnos.items):
                                    alumno = grupo.alumnos.items[idx]
                                    grupo.alumnos.eliminar(indice=idx)
                                    print(f"Alumno {alumno.nombre} {alumno.apellido} eliminado del grupo.")
                                else:
                                    print("Índice fuera de rango.")
                            except ValueError:
                                print("Entrada inválida. Debe ingresar un número.")
                        
                        elif opcion == "5":
                            break
                        
                        else:
                            print("Opción no válida.")

                if self.guardar:
                    self.grupos.guardarArchivo(self.archivo)
                print("Grupo actualizado.")
            else:
                print("Índice fuera de rango.")
        except ValueError:
            print("Entrada inválida.")