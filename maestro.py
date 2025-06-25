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
        
    def __iter__(self):
        if self.es_objeto:
            return iter(self.items)
        else:
            # Si no es un contenedor, devolver un iterador que solo incluye este objeto
            return iter([self])
    
    # Verificar si un maestro ya existe por matrícula (localmente y en MongoDB)
    def existe_maestro(self, matricula):
        # Verificar localmente
        if self.es_objeto:
            for maestro in self.items:
                if getattr(maestro, 'matricula', None) == matricula:
                    return True
        
        # Verificar en MongoDB (si hay conexión)
        if self.collection_name and self.mongo_manager.is_connected:
            # Buscar documento con la misma matrícula en MongoDB
            maestro_encontrado = self.mongo_manager.find_document(self.collection_name, {"matricula": matricula})
            if maestro_encontrado:
                return True
        
        return False
    
    # Sobrescribir el método agregar para evitar duplicados
    def agregar(self, *items):
        for item in items:
            # Verificar si el elemento ya existe (por matrícula)
            if not self.existe_maestro(item.matricula):
                super().agregar(item)
            else:
                print(f"No se agregó maestro con matrícula {item.matricula} porque ya existe.")

if __name__ == "__main__":
    from MaestroUI import MaestroUI

    # Crear una instancia de Maestro que cargará automáticamente del JSON
    maestros = Maestro()
    interfaz = MaestroUI(maestros, 'maestros.json')
    interfaz.menu()
