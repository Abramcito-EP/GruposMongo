from arreglo import Arreglo
import json

class Maestro(Arreglo):
    def __init__(self, nombre=None, apellido=None, edad=None, matricula=None, especialidad=None):
        if nombre is None and apellido is None and edad is None and matricula is None and especialidad is None:
            Arreglo.__init__(self)
            self.es_objeto = True
        else:
            self.nombre = nombre
            self.apellido = apellido
            self.edad = edad
            self.matricula = matricula
            self.especialidad = especialidad
            self.es_objeto = False

    def __str__(self):
        if self.es_objeto:
            return f"Total de maestros: {Arreglo.__str__(self)}"
        return (f"Maestro: {self.nombre} {self.apellido}, edad: {self.edad} años, especialidad: {self.especialidad}, "
                f"Matrícula: {self.matricula}")

    def convertir_diccionario(self):
        if self.es_objeto:
            return Arreglo.convertir_diccionario(self)
        return {
            "nombre": self.nombre,
            "apellido": self.apellido,
            "edad": self.edad,
            "matricula": self.matricula,
            "especialidad": self.especialidad
        }

    def mostrar(self):
        print(str(self))
        

if __name__ == "__main__":
    from MaestroUI import MaestroUI

    interfaz = MaestroUI()
    interfaz.menu()
