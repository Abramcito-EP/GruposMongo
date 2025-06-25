from arreglo import Arreglo
import json

class Maestro(Arreglo):
    def __init__(self, nombre=None, apellido=None, edad=None, matricula=None, especialidad=None):
        super().__init__()
        self.collection_name = "maestros"  
        self.archivo_json = "maestros.json"  
        
        if nombre is None and apellido is None and edad is None and matricula is None and especialidad is None:
            self.es_objeto = True
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
        
    def __iter__(self):
        if self.es_objeto:
            return iter(self.items)
        else:
            return iter([self])
    
    def existe_maestro(self, matricula):
        if self.es_objeto:
            for maestro in self.items:
                if getattr(maestro, 'matricula', None) == matricula:
                    return True
        
        if self.collection_name and self.mongo_manager.is_connected:
            maestro_encontrado = self.mongo_manager.find_document(self.collection_name, {"matricula": matricula})
            if maestro_encontrado:
                return True
        
        return False
    

    def agregar(self, *items):
        for item in items:
            if not self.existe_maestro(item.matricula):
                super().agregar(item)
            else:
                print(f"No se agregó maestro con matrícula {item.matricula} porque ya existe.")

if __name__ == "__main__":
    from MaestroUI import MaestroUI

    maestros = Maestro()
    interfaz = MaestroUI(maestros, 'maestros.json')
    interfaz.menu()
