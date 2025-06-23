from arreglo import Arreglo

class Alumno(Arreglo):
    def __init__(self, nombre=None, apellido=None, edad=None, matricula=None, sexo=None):
        super().__init__()
        self.collection_name = "alumnos"  # Definir el nombre de la colección
        self.archivo_json = "alumnos.json"  # Archivo JSON por defecto
        
        if nombre is None and apellido is None and edad is None and matricula is None and sexo is None:
            self.es_objeto = True
            # Cargar automáticamente del archivo JSON si existe, 
            # pero solo si este es el objeto principal, no un contenedor
            if self.archivo_json and not hasattr(self, '_skip_load'):
                self.cargarArchivo(self.archivo_json, Alumno)
        else:
            self.nombre = nombre
            self.apellido = apellido
            self.edad = edad
            self.matricula = matricula
            self.sexo = sexo
            self.es_objeto = False

    def __str__(self):
        if self.es_objeto:
            return f"Total de alumnos: {super().__str__()}"
        return (f"Alumno: {self.nombre} {self.apellido}, {self.edad} años, sexo: {self.sexo}, "
                f"Matrícula: {self.matricula}")

    def convertir_diccionario(self):
        if self.es_objeto:
            return super().convertir_diccionario()
        return {
            "nombre": self.nombre,
            "apellido": self.apellido,
            "edad": self.edad,
            "matricula": self.matricula,
            "sexo": self.sexo
        }

    def mostrar(self):
        print(str(self))

if __name__ == "__main__":
    from AlumnoUI import AlumnoUI

    # Crear una instancia de Alumno que cargará automáticamente del JSON
    alumnos = Alumno()
    interfaz = AlumnoUI(alumnos, 'alumnos.json')
    interfaz.menu()
