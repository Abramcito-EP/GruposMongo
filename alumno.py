from arreglo import Arreglo

class Alumno(Arreglo):
    def __init__(self, nombre=None, apellido=None, edad=None, matricula=None, sexo=None):
        super().__init__()
        
        if nombre is None and apellido is None and edad is None and matricula is None and sexo is None:
            self.es_objeto = True
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
            resultado = []
            for alumno in self.items:
                if hasattr(alumno, 'convertir_diccionario'):
                    resultado.append(alumno.convertir_diccionario())
                else:
                    alumno_dict = {k: v for k, v in vars(alumno).items() 
                                 if not k.startswith('_') and k not in ['es_objeto', 'items']}
                    resultado.append(alumno_dict)
            return resultado
        else:
            return {
                "nombre": self.nombre,
                "apellido": self.apellido,
                "edad": self.edad,
                "matricula": self.matricula,
                "sexo": self.sexo
            }

    def mostrar(self):
        print(str(self))

    def existe_alumno(self, matricula):
        if self.es_objeto:
            for alumno in self.items:
                if getattr(alumno, 'matricula', None) == matricula:
                    return True
        return False

if __name__ == "__main__":
    from AlumnoUI import AlumnoUI
    alumnos = Alumno()
    interfaz = AlumnoUI(alumnos, 'alumnos.json')
    interfaz.menu()
