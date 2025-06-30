from alumno import Alumno
from maestro import Maestro
from arreglo import Arreglo

class Grupo(Arreglo):
    def __init__(self, nombre=None, grado=None, seccion=None, maestro=None, alumnos=None):
        super().__init__()
        
        if nombre is None and grado is None and seccion is None:
            self.es_objeto = True
        else:
            self.nombre = nombre
            self.grado = grado
            self.seccion = seccion
            
            # Manejar maestro
            if isinstance(maestro, dict):
                maestro = {k: v for k, v in maestro.items() if k in ["nombre", "apellido", "edad", "matricula", "especialidad"]}
                self.maestro = Maestro(**maestro)
            else:
                self.maestro = maestro
            
            # Inicializar alumnos como contenedor
            self.alumnos = Alumno()
            
            # Agregar alumnos si se proporcionan
            if alumnos:
                if isinstance(alumnos, list):
                    for alumno_data in alumnos:
                        if isinstance(alumno_data, dict):
                            # Filtrar solo campos válidos de alumno
                            alumno_data = {k: v for k, v in alumno_data.items() if k in ["nombre", "apellido", "edad", "matricula", "sexo"]}
                            self.alumnos.agregar(Alumno(**alumno_data))
                        else:
                            self.alumnos.agregar(alumno_data)
                elif hasattr(alumnos, 'items'):
                    for alumno in alumnos.items:
                        self.alumnos.agregar(alumno)
            
            self.es_objeto = False

    def asignarMaestro(self, maestro):
        self.maestro = maestro
        return f"El maestro {maestro.nombre} {maestro.apellido} ha sido asignado al grupo {self.nombre}."

    def convertir_diccionario(self):
        if self.es_objeto:
            # CORREGIR: Para contenedores, devolver lista de grupos procesados
            resultado = []
            for grupo in self.items:
                if hasattr(grupo, 'convertir_diccionario'):
                    grupo_dict = grupo.convertir_diccionario()
                    resultado.append(grupo_dict)
            return resultado
        else:
            # CORREGIR: Asegurar que maestro y alumnos se conviertan correctamente
            maestro_dict = None
            if self.maestro and hasattr(self.maestro, 'convertir_diccionario'):
                maestro_dict = self.maestro.convertir_diccionario()
            
            alumnos_list = []
            if hasattr(self.alumnos, 'items'):
                for alumno in self.alumnos.items:
                    if hasattr(alumno, 'convertir_diccionario'):
                        alumno_dict = alumno.convertir_diccionario()
                        alumnos_list.append(alumno_dict)
            
            return {
                "nombre": self.nombre,
                "grado": self.grado,
                "seccion": self.seccion,
                "maestro": maestro_dict,
                "alumnos": alumnos_list
            }

    def __str__(self):
        if self.es_objeto:
            return f"Total de grupos: {super().__str__()}"
        
        alumnos_count = len(self.alumnos.items) if hasattr(self.alumnos, 'items') else 0
        maestro_info = f"{self.maestro.nombre} {self.maestro.apellido}" if self.maestro else "Sin asignar"
        
        return (f"Grupo: {self.nombre}, Grado: {self.grado}, Sección: {self.seccion}, "
                f"Maestro: {maestro_info}, Alumnos: {alumnos_count}")

    def mostrar(self):
        print(str(self))
        if not self.es_objeto:
            print("\nInformación del maestro:")
            if self.maestro:
                self.maestro.mostrar()
            else:
                print("Sin maestro asignado")
            
            print("\nLista de alumnos:")
            if hasattr(self.alumnos, 'items') and self.alumnos.items:
                for i, alumno in enumerate(self.alumnos.items):
                    print(f"  {i+1}. {alumno}")
            else:
                print("No hay alumnos en este grupo")

    def cargarDatos(self, datos, clase_objeto):
        self.items = []
        
        if isinstance(datos, list):
            for item in datos:
                try:
                    # Filtrar campos no deseados
                    grupo_data = {k: v for k, v in item.items() 
                                 if k not in ["_id", "es_objeto", "maestro", "alumnos"]}
                    
                    # Extraer datos del maestro
                    maestro_data = item.get("maestro")
                    
                    # Extraer datos de alumnos
                    alumnos_data = item.get("alumnos", [])
                    
                    # Crear grupo
                    grupo = Grupo(nombre=grupo_data.get("nombre"),
                                 grado=grupo_data.get("grado"),
                                 seccion=grupo_data.get("seccion"),
                                 maestro=maestro_data,
                                 alumnos=alumnos_data)
                    
                    self.items.append(grupo)
                except Exception as e:
                    print(f"Error al cargar grupo: {e}")
        else:
            super().cargarDatos(datos, clase_objeto)

if __name__ == "__main__":
    from GrupoUI import GrupoUI
    grupos = Grupo()
    interfaz = GrupoUI(grupos, 'grupos.json')
    interfaz.menu()