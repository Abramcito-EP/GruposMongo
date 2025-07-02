from alumno import Alumno
from maestro import Maestro
from arreglo import Arreglo
import json

class Grupo(Arreglo):
    def __init__(self, nombre=None, grado=None, seccion=None, maestro=None, alumnos=None):
        if nombre is None:
            super().__init__()
            self.es_objeto = True
            return

        self.nombre = nombre
        self.grado = grado
        self.seccion = seccion

        if isinstance(maestro, dict):
            maestro = {k: v for k, v in maestro.items() if k in ["nombre", "apellido", "edad", "matricula", "especialidad"]}
            self.maestro = Maestro(**maestro)
        else:
            self.maestro = maestro if isinstance(maestro, Maestro) else None

        self.alumnos = Alumno()
        if alumnos:
            for alumno_data in alumnos:
                if isinstance(alumno_data, dict):
                    alumno_data = {k: v for k, v in alumno_data.items() if k in ["nombre", "apellido", "edad", "matricula", "sexo"]}
                    self.alumnos.agregar(Alumno(**alumno_data))
                elif isinstance(alumno_data, Alumno):
                    self.alumnos.agregar(alumno_data)

        self.es_objeto = False

    def asignarMaestro(self, maestro):
        self.maestro = maestro
        return f"El maestro {maestro.nombre} {maestro.apellido} ha sido asignado al grupo {self.nombre}."

    def convertir_diccionario(self):
        if self.es_objeto:
            return [item.convertir_diccionario() for item in self.items]

        return {
            "nombre": self.nombre,
            "grado": self.grado,
            "seccion": self.seccion,
            "maestro": self.maestro.convertir_diccionario() if self.maestro else None,
            "alumnos": self.alumnos.convertir_diccionario()
        }

    def __str__(self):
        if self.es_objeto:
            return f"Total de grupos: {len(self.items)}"
        maestro_nombre = f"{self.maestro.nombre} {self.maestro.apellido}" if self.maestro else "Sin asignar"
        return f"Grupo: {self.nombre}, Grado: {self.grado}, Sección: {self.seccion}, Maestro: {maestro_nombre}, Alumnos: {len(self.alumnos.items)}"

    def mostrar(self):
        print(self)
        print("Alumnos:")
        self.alumnos.mostrar()




if __name__ == "__main__":
    from GrupoUI import GrupoUI

    grupos = Grupo()
    maestro = Maestro("Pedro", "Gómez", 42, "M001", "Historia")
    alumno = Alumno("Lucía", "Martínez", 13, "A001", "F")
    grupo_individual = Grupo("Grupo C", "1ro", "A", maestro, [alumno])
    grupos.agregar(grupo_individual)

    interfaz = GrupoUI(grupos)
    interfaz.menu()