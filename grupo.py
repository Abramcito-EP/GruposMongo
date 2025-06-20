from alumno import Alumno
from maestro import Maestro
from arreglo import Arreglo

class Grupo(Arreglo):
    def __init__(self, nombre=None, grado=None, seccion=None, maestro=None, alumnos=None):
        super().__init__()
        self.collection_name = "grupos"  # Definir el nombre de la colección
        
        if nombre is None:
            self.es_objeto = True
            return

        self.nombre = nombre
        self.grado = grado
        self.seccion = seccion

        if isinstance(maestro, dict):
            self.maestro = Maestro(**maestro)
        else:
            self.maestro = maestro

        self.alumnos = Alumno()
        if alumnos:
            if isinstance(alumnos, list):
                for alumno in alumnos:
                    if isinstance(alumno, dict):
                        self.alumnos.agregar(Alumno(**alumno))
                    else:
                        self.alumnos.agregar(alumno)
            else:
                self.alumnos = alumnos

        self.es_objeto = False

    def asignarMaestro(self, maestro):
        self.maestro = maestro
        return f"El maestro {maestro.nombre} {maestro.apellido} ha sido asignado al grupo {self.nombre}."

    def convertir_diccionario(self):
        if self.es_objeto:
            return super().convertir_diccionario()
        
        # Convertir alumnos a lista de diccionarios
        alumnos_dict = []
        if hasattr(self.alumnos, 'items'):
            for alumno in self.alumnos.items:
                if hasattr(alumno, 'convertir_diccionario'):
                    alumnos_dict.append(alumno.convertir_diccionario())
        
        # Convertir maestro a diccionario
        maestro_dict = {}
        if hasattr(self.maestro, 'convertir_diccionario'):
            maestro_dict = self.maestro.convertir_diccionario()
        
        return {
            "nombre": self.nombre,
            "grado": self.grado,
            "seccion": self.seccion,
            "maestro": maestro_dict,
            "alumnos": alumnos_dict
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


if __name__ == "__main__":
    from GrupoUI import GrupoUI

    grupos = Grupo()
    maestro = Maestro("Pedro", "Gómez", 42, "M001", "Historia")
    alumno = Alumno("Lucía", "Martínez", 13, "A001", "F")
    grupo_individual = Grupo("Grupo C", "1ro", "A", maestro, [alumno])
    grupos.agregar(grupo_individual)

    interfaz = GrupoUI(grupos)
    interfaz.menu()