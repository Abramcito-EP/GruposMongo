import json
import os

class Arreglo:
    def __init__(self):
        self.items = []
        self.es_objeto = True
    
    def agregar(self, *items):
        for item in items:
            self.items.append(item)
    
    def eliminar(self, item=None, indice=None):
        try:
            if indice is not None:
                del self.items[indice]
            else:
                self.items.remove(item)
            return True
        except (IndexError, ValueError):
            return False
    
    def actualizar(self, objeto, **nuevos_valores):
        for elem in self.items:
            if elem == objeto:
                for attr, val in nuevos_valores.items():
                    setattr(elem, attr, val)
                return True
        return False
    
    def __str__(self):
        if not self.items:
            return "0"
        return str(len(self.items))

    def convertir_diccionario(self):
        def limpiar(dic):
            return {k: v for k, v in dic.items() if k != "_id"}
        
        if self.es_objeto:
            return [limpiar(vars(item)) for item in self.items]
        else:
            return limpiar(vars(self))

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
                if not atributo.startswith("__") and atributo != "es_objeto" and atributo != "items":
                    print(f"{atributo}: {valor}")
    
    def guardarArchivo(self, archivo):
        try:
            with open(archivo, "w", encoding="utf-8") as f:
                # CORREGIR: Usar siempre convertir_diccionario() para serializar
                json.dump(self.convertir_diccionario(), f, indent=4, ensure_ascii=False)
            print(f"Datos guardados en {archivo}")
            return True
        except Exception as e:
            print(f"Error al guardar en archivo: {e}")
            return False

    def cargarArchivo(self, archivo, clase_objeto):
        try:
            if os.path.exists(archivo):
                with open(archivo, "r", encoding="utf-8") as f:
                    datos = json.load(f)
                self.cargarDatos(datos, clase_objeto)
                print(f"Datos cargados desde archivo local {archivo}")
                return True
            else:
                print(f"No se encontró el archivo {archivo}")
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
                    # CORREGIR: Filtrar TODOS los campos internos, incluyendo 'items'
                    item_filtrado = {k: v for k, v in item.items() 
                                   if k not in ["_id", "es_objeto", "items"]}
                    objeto = clase_objeto(**item_filtrado)
                    self.items.append(objeto)
                except Exception as e:
                    print(f"Error al cargar item: {e}")
            print(f"Datos cargados correctamente: {len(self.items)} elementos")
        else:
            try:
                # CORREGIR: También filtrar aquí
                datos_filtrados = {k: v for k, v in datos.items() 
                                 if k not in ["_id", "es_objeto", "items"]}
                objeto = clase_objeto(**datos_filtrados)
                self.items.append(objeto)
                print("Dato cargado correctamente desde un solo objeto")
            except Exception as e:
                print(f"Error al cargar objeto único: {e}")

