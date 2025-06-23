import json
import os
from mongo_manager import MongoManager

class Arreglo:
    def __init__(self):
        self.items = []
        self.es_objeto = True
        self.mongo_manager = MongoManager()
        self.collection_name = None  # Debe ser definido por las subclases
        self.archivo_json = None  # Archivo JSON asociado
    
    def agregar(self, *items):
        for item in items:
            self.items.append(item)
            
            # Si tenemos el nombre de la colección, intentar guardar en MongoDB
            if self.collection_name and hasattr(item, 'convertir_diccionario'):
                data = item.convertir_diccionario()
                self.mongo_manager.insert_document(self.collection_name, data)
        
        # Guardar automáticamente en JSON si tenemos un archivo asociado
        if self.archivo_json:
            self.guardarArchivo(self.archivo_json)
    
    def eliminar(self, item=None, indice=None):
        try:
            if indice is not None:
                del self.items[indice]
            else:
                self.items.remove(item)
                
            # Guardar automáticamente en JSON si tenemos un archivo asociado
            if self.archivo_json:
                self.guardarArchivo(self.archivo_json)
                
            return True
        except (IndexError, ValueError):
            return False
    
    def actualizar(self, objeto, **nuevos_valores):
        for elem in self.items:
            if elem == objeto:
                for attr, val in nuevos_valores.items():
                    setattr(elem, attr, val)
                
                # Guardar automáticamente en JSON si tenemos un archivo asociado
                if self.archivo_json:
                    self.guardarArchivo(self.archivo_json)
                    
                return True
        return False
    
    def __str__(self):
        if not self.items:
            return "[]"
        return f"Elementos: {len(self.items)}"

    def convertir_diccionario(self):
        if self.es_objeto:
            return [item.convertir_diccionario() for item in self.items if hasattr(item, 'convertir_diccionario')]
        else:
            return {k: v for k, v in vars(self).items() if k != 'mongo_manager' and k != 'archivo_json'}

    def mostrar(self):
        if self.items:
            print(f"Elementos: {len(self.items)}")
            for item in self.items:
                if hasattr(item, 'mostrar'):
                    item.mostrar()
                else:
                    print(item)
        else:
            for atributo, valor in vars(self).items():
                if not atributo.startswith("__") and atributo != "es_objeto" and atributo != "items" and atributo != "mongo_manager" and atributo != "archivo_json":
                    print(f"{atributo}: {valor}")
    
    def guardarArchivo(self, archivo):
        try:
            # Guardar en un archivo temporal primero para evitar corrupción
            archivo_temp = f"{archivo}.tmp"
            with open(archivo_temp, "w", encoding="utf-8") as f:
                json.dump(self.convertir_diccionario(), f, indent=4, ensure_ascii=False)
            
            # Si la escritura fue exitosa, reemplazar el archivo original
            if os.path.exists(archivo_temp):
                if os.path.exists(archivo):
                    os.remove(archivo)
                os.rename(archivo_temp, archivo)
            
            # Actualizar el nombre del archivo asociado
            self.archivo_json = archivo
            
            print(f"Datos guardados en {archivo}")
            
            # Intentar sincronizar con MongoDB como respaldo
            if self.collection_name:
                self.mongo_manager.sync_all_pending_data()
                
            return True
        except Exception as e:
            print(f"Error al guardar en archivo: {e}")
            if os.path.exists(f"{archivo}.tmp"):
                os.remove(f"{archivo}.tmp")
            return False

    def cargarArchivo(self, archivo, clase_objeto):
        try:
            # Guardar referencia al archivo
            self.archivo_json = archivo
            
            # Primero intentar cargar desde archivo local (prioridad)
            if os.path.exists(archivo):
                with open(archivo, "r", encoding="utf-8") as f:
                    datos = json.load(f)
                self.cargarDatos(datos, clase_objeto)
                print(f"Datos cargados desde archivo local {archivo}")
                
                # Como respaldo, intentar sincronizar con MongoDB si hay conexión
                if self.collection_name and self.mongo_manager.is_connected:
                    self.mongo_manager.sync_all_pending_data()
                
                return True
            else:
                # Si no hay archivo local, intentar cargar desde MongoDB
                if self.collection_name and self.mongo_manager.is_connected:
                    documentos = self.mongo_manager.find_documents(self.collection_name)
                    if documentos:
                        self.cargarDatos(documentos, clase_objeto)
                        print(f"Datos cargados desde MongoDB para {self.collection_name}")
                        # Guardar inmediatamente en archivo local
                        self.guardarArchivo(archivo)
                        return True
                
                print(f"No se encontró el archivo {archivo} y no hay datos en MongoDB")
                # Crear archivo vacío
                with open(archivo, "w", encoding="utf-8") as f:
                    json.dump([], f)
                print(f"Se creó un archivo vacío: {archivo}")
                return False
        except FileNotFoundError:
            print(f"Error: El archivo {archivo} no existe")
            # Crear archivo vacío
            with open(archivo, "w", encoding="utf-8") as f:
                json.dump([], f)
            print(f"Se creó un archivo vacío: {archivo}")
            return False
        except Exception as e:
            print(f"Error al cargar datos: {e}")
            return False

    def cargarDatos(self, datos, clase_objeto):
        self.items = []

        if isinstance(datos, list):
            for item in datos:
                try:
                    # Eliminar campos que no correspondan al modelo
                    item_filtrado = {k: v for k, v in item.items() if k != "_id" and k != "es_objeto"}
                    objeto = clase_objeto(**item_filtrado)
                    self.items.append(objeto)
                except Exception as e:
                    print(f"Error al cargar item: {e}")
            print(f"Datos cargados correctamente: {len(self.items)} elementos")
        else:
            try:
                # Eliminar campos que no correspondan al modelo
                datos_filtrados = {k: v for k, v in datos.items() if k != "_id" and k != "es_objeto"}
                objeto = clase_objeto(**datos_filtrados)
                self.items.append(objeto)
                print("Dato cargado correctamente desde un solo objeto")
            except Exception as e:
                print(f"Error al cargar objeto único: {e}")

