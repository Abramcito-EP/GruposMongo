from alumno import Alumno
from maestro import Maestro
from arreglo import Arreglo

class Grupo(Arreglo):
    def __init__(self, nombre=None, grado=None, seccion=None, maestro=None, alumnos=None):
        super().__init__()
        self.collection_name = "grupos" 
        self.archivo_json = "grupos.json"  
        
        if nombre is None:
            self.es_objeto = True
            if self.archivo_json:
                self.cargarArchivo(self.archivo_json, Grupo)
            return

        self.nombre = nombre
        self.grado = grado
        self.seccion = seccion

        if isinstance(maestro, dict):
            self.maestro = Maestro(**maestro)
        else:
            self.maestro = maestro

        # Inicializar alumnos
        self.alumnos = Alumno()
        self.alumnos.es_objeto = True
        self.alumnos.items = [] 
        
        # Cargar alumnos si se proporcionan
        if alumnos:
            if isinstance(alumnos, list):
                for alumno in alumnos:
                    if isinstance(alumno, dict):
                        self.alumnos.items.append(Alumno(**alumno))
                    else:
                        self.alumnos.items.append(alumno)
            elif hasattr(alumnos, 'items'):
                for alumno in alumnos.items:
                    self.alumnos.items.append(alumno)

        self.es_objeto = False

    def asignarMaestro(self, maestro):
        self.maestro = maestro
        if self.archivo_json:
            self.guardarArchivo(self.archivo_json)
        return f"El maestro {maestro.nombre} {maestro.apellido} ha sido asignado al grupo {self.nombre}."

    def convertir_diccionario(self):
        if self.es_objeto:
            return super().convertir_diccionario()
        
        # Para el grupo, incluimos TODOS los datos de los alumnos
        alumnos_completos = []
        if hasattr(self.alumnos, 'items'):
            for alumno in self.alumnos.items:
                if hasattr(alumno, 'convertir_diccionario'):
                    # Guardar el diccionario completo del alumno
                    alumno_dict = alumno.convertir_diccionario()
                    # Eliminar campos que no queremos incluir
                    if '_id' in alumno_dict:
                        del alumno_dict['_id']
                    if 'es_objeto' in alumno_dict:
                        del alumno_dict['es_objeto']
                    alumnos_completos.append(alumno_dict)
        
        # Asegurar que el maestro tiene datos completos
        maestro_dict = {}
        if hasattr(self.maestro, 'convertir_diccionario'):
            maestro_dict = self.maestro.convertir_diccionario()
        
        return {
            "nombre": self.nombre,
            "grado": self.grado,
            "seccion": self.seccion,
            "maestro": maestro_dict,
            "alumnos": alumnos_completos  # Guardar datos completos de alumnos
        }

    def __str__(self):
        if self.es_objeto:
            return f"Total de grupos: {super().__str__()}"
        
        alumnos_count = len(self.alumnos.items) if hasattr(self.alumnos, 'items') else 0
        maestro_info = f"{self.maestro.nombre} {self.maestro.apellido}" if hasattr(self.maestro, 'nombre') else "Sin asignar"
        
        return (f"Grupo: {self.nombre}, Grado: {self.grado}, Sección: {self.seccion}, "
                f"Maestro: {maestro_info}, Alumnos: {alumnos_count}")

    def mostrar(self):
        print(str(self))
        if not self.es_objeto:
            print("\nInformación del maestro:")
            if hasattr(self.maestro, 'mostrar'):
                self.maestro.mostrar()
            else:
                print("Sin maestro asignado")
            
            print("\nLista de alumnos:")
            if hasattr(self.alumnos, 'items') and self.alumnos.items:
                for alumno in self.alumnos.items:
                    if hasattr(alumno, 'mostrar'):
                        alumno.mostrar()
            else:
                print("No hay alumnos en este grupo")

    def cargarDatos(self, datos, clase_objeto):
        self.items = []

        if isinstance(datos, list):
            for item in datos:
                try:
                    # Procesar al maestro si existe
                    maestro = None
                    if "maestro" in item and isinstance(item["maestro"], dict):
                        maestro_data = item["maestro"]
                        maestro_data = {k: v for k, v in maestro_data.items() 
                                      if k != "_id" and k != "es_objeto"}
                        maestro = Maestro(**maestro_data)
                    
                    # Crear el grupo
                    grupo_data = {k: v for k, v in item.items() 
                                 if k != "alumnos" and k != "maestro" and k != "_id" and k != "es_objeto"}
                    grupo = Grupo(**grupo_data)
                    
                    # Asignar maestro
                    if maestro:
                        grupo.maestro = maestro
                    
                    # Procesar alumnos con sus datos completos
                    grupo.alumnos = Alumno()
                    grupo.alumnos.es_objeto = True
                    grupo.alumnos.items = []
                    
                    if "alumnos" in item and isinstance(item["alumnos"], list):
                        for alumno_data in item["alumnos"]:
                            if isinstance(alumno_data, dict):
                                # Filtrar campos no deseados
                                alumno_data = {k: v for k, v in alumno_data.items() 
                                             if k != "_id" and k != "es_objeto"}
                                # Crear objeto Alumno con los datos completos
                                alumno = Alumno(**alumno_data)
                                grupo.alumnos.items.append(alumno)
                    
                    self.items.append(grupo)
                except Exception as e:
                    print(f"Error al cargar grupo: {e}")
        else:
            super().cargarDatos(datos, clase_objeto)

    def agregar_alumno(self, alumno):
        """Agrega un alumno al grupo sin duplicarlo en MongoDB"""
        if not hasattr(self, 'alumnos') or not isinstance(self.alumnos, Alumno):
            self.alumnos = Alumno()
            self.alumnos.es_objeto = True
            self.alumnos.items = []
        
        # Usar el método existe_alumno de la clase Alumno si está disponible
        if hasattr(self.alumnos, 'existe_alumno') and hasattr(alumno, 'matricula'):
            if self.alumnos.existe_alumno(alumno.matricula):
                print(f"El alumno con matrícula {alumno.matricula} ya está en el grupo.")
                return False
        else:
            # Verificación manual si el método no está disponible
            for a in self.alumnos.items:
                if hasattr(a, 'matricula') and hasattr(alumno, 'matricula') and a.matricula == alumno.matricula:
                    print(f"El alumno con matrícula {alumno.matricula} ya está en el grupo.")
                    return False
        
        # Agregar directamente a la lista de items sin intentar guardar en MongoDB
        self.alumnos.items.append(alumno)
        
        # Guardar el grupo actualizado
        if self.archivo_json:
            self.guardarArchivo(self.archivo_json)
        
        return True

if __name__ == "__main__":
    from GrupoUI import GrupoUI

 
    grupos = Grupo()
    interfaz = GrupoUI(grupos, 'grupos.json')
    interfaz.menu()