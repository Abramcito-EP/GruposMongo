import json
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
            return "[]"
        return f"Elementos: {len(self.items)}"

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
                    if hasattr(valor, "__str__"):
                        print(f"{atributo}: {valor}")
                    else:
                        print(f"{atributo}: {valor}")
    
    def guardarArchivo(self, archivo):
        try:
            with open(archivo, "w", encoding="utf-8") as f:
                json.dump(self.convertir_diccionario(), f, indent=4, ensure_ascii=False)
            print(f"Datos guardados en {archivo}")
        except Exception as e:
            print(f"Error al guardar en archivo: {e}")

    def cargarArchivo(self, archivo, clase_objeto):
        try:
            with open(archivo, "r", encoding="utf-8") as f:
                datos = json.load(f)
            self.cargarDatos(datos, clase_objeto)
        except FileNotFoundError:
            print(f"Error: El archivo {archivo} no existe")
        except TypeError as e:
            print(f"Error: La clase {clase_objeto.__name__} no es compatible con los datos del archivo: {e}")
        except Exception as e:
            print(f"Error al cargar desde archivo: {e}")

    def cargarDatos(self, datos, clase_objeto):
        self.items = []

        if isinstance(datos, list):
            for item in datos:
                item = {k: v for k, v in item.items() if k != "es_objeto"}
                objeto = clase_objeto(**item)
                self.items.append(objeto)
            print("Datos cargados correctamente desde lista")
        else:
            datos = {k: v for k, v in datos.items() if k != "es_objeto"}
            objeto = clase_objeto(**datos)
            self.items.append(objeto)
            print("Dato cargado correctamente desde un solo objeto")

