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
                # Usar flag para evitar sincronización automática con MongoDB durante la carga inicial
                self._loading_from_file = True
                self.cargarArchivo(self.archivo_json, Alumno)
                self._loading_from_file = False
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
        
    def __iter__(self):
        if self.es_objeto:
            # Usar el atributo 'items' que es el nombre correcto según la clase Arreglo
            return iter(self.items)
        else:
            # Si no es un contenedor, devolver un iterador que solo incluye este objeto
            return iter([self])

    # Verificar si un alumno ya existe por matrícula
    def existe_alumno(self, matricula):
        if self.es_objeto:
            for alumno in self.items:
                if getattr(alumno, 'matricula', None) == matricula:
                    return True
        return False
    
    # Sobrescribir el método agregar para evitar duplicados
    def agregar(self, *items):
        for item in items:
            # Verificar si el elemento ya existe (por matrícula)
            if not self.existe_alumno(item.matricula):
                super().agregar(item)
            else:
                print(f"No se agregó alumno con matrícula {item.matricula} porque ya existe.")
    
    # Sobrescribir el método cargarArchivo para manejar sincronización
    def cargarArchivo(self, archivo, clase_objeto):
        from os import path
        
        # Primero cargamos normalmente
        super().cargarArchivo(archivo, clase_objeto)
        
        # Verificar si existe el archivo de pendientes
        pendientes_path = "alumnos_sin_enviar.json"
        if path.exists(pendientes_path):
            try:
                # Cargar los alumnos pendientes
                import json
                with open(pendientes_path, 'r', encoding='utf-8') as f:
                    pendientes = json.load(f)
                
                if pendientes and isinstance(pendientes, list) and len(pendientes) > 0:
                    print(f"Encontrados {len(pendientes)} alumnos pendientes de sincronizar")
                    
                    # Verificar conexión a MongoDB
                    if self.mongo_manager.is_connected:
                        print("Sincronizando alumnos pendientes con MongoDB...")
                        
                        # Obtener todos los documentos existentes para comparar
                        docs_existentes = self.mongo_manager.find_documents(self.collection_name)
                        matriculas_existentes = set()
                        if docs_existentes:
                            matriculas_existentes = {doc.get('matricula') for doc in docs_existentes if 'matricula' in doc}
                        
                        # Insertar solo los no duplicados
                        for alumno_data in pendientes:
                            if 'matricula' in alumno_data and alumno_data['matricula'] not in matriculas_existentes:
                                self.mongo_manager.insert_document(self.collection_name, alumno_data)
                                matriculas_existentes.add(alumno_data['matricula'])  # Añadir a existentes
                            else:
                                print(f"Saltando alumno con matrícula {alumno_data.get('matricula')} porque ya existe en MongoDB")
                        
                        # Limpiar archivo de pendientes después de sincronizar
                        with open(pendientes_path, 'w', encoding='utf-8') as f:
                            json.dump([], f)
                        print("Sincronización completada. Archivo de pendientes limpiado.")
                    else:
                        print("No hay conexión a MongoDB. Los alumnos pendientes se sincronizarán más tarde.")
            except Exception as e:
                print(f"Error al procesar alumnos pendientes: {e}")
        
        return True

if __name__ == "__main__":
    from AlumnoUI import AlumnoUI

    # Crear una instancia de Alumno que cargará automáticamente del JSON
    alumnos = Alumno()
    interfaz = AlumnoUI(alumnos, 'alumnos.json')
    interfaz.menu()
    interfaz.menu()
