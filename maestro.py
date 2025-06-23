from arreglo import Arreglo
import json

class Maestro(Arreglo):
    def __init__(self, nombre=None, apellido=None, edad=None, matricula=None, especialidad=None):
        super().__init__()
        self.collection_name = "maestros"  # Definir el nombre de la colección
        self.archivo_json = "maestros.json"  # Archivo JSON por defecto
        
        if nombre is None and apellido is None and edad is None and matricula is None and especialidad is None:
            self.es_objeto = True
            # Cargar automáticamente del archivo JSON si existe
            if self.archivo_json:
                self.cargarArchivo(self.archivo_json, Maestro)
        else:
            self.nombre = nombre
            self.apellido = apellido
            self.edad = edad
            self.matricula = matricula
            self.especialidad = especialidad
            self.es_objeto = False

    def __str__(self):
        if self.es_objeto:
            return f"Total de maestros: {super().__str__()}"
        return (f"Maestro: {self.nombre} {self.apellido}, edad: {self.edad} años, especialidad: {self.especialidad}, "
                f"Matrícula: {self.matricula}")

    def convertir_diccionario(self):
        if self.es_objeto:
            return super().convertir_diccionario()
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

    # Crear una instancia de Maestro que cargará automáticamente del JSON
    maestros = Maestro()
    interfaz = MaestroUI(maestros, 'maestros.json')
    interfaz.menu()
