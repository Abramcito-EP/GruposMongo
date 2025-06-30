from arreglo import Arreglo

class Maestro(Arreglo):
    def __init__(self, nombre=None, apellido=None, edad=None, matricula=None, especialidad=None):
        super().__init__()
        
        if nombre is None and apellido is None and edad is None and matricula is None and especialidad is None:
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
            return f"Total de maestros: {super().__str__()}"
        return (f"Maestro: {self.nombre} {self.apellido}, edad: {self.edad} años, especialidad: {self.especialidad}, "
                f"Matrícula: {self.matricula}")

    def convertir_diccionario(self):
        if self.es_objeto:
            resultado = []
            for maestro in self.items:
                if hasattr(maestro, 'convertir_diccionario'):
                    resultado.append(maestro.convertir_diccionario())
            return resultado
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
    maestros = Maestro()
    interfaz = MaestroUI(maestros, 'maestros.json')
    interfaz.menu()
