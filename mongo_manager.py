import os
import json
import time
import threading
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
import requests
from mongo_config import MONGO_URI, DB_NAME, COLLECTIONS, BACKUP_FILES, SYNC_INTERVAL

class MongoManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoManager, cls).__new__(cls)
            cls._instance.initialize()
        return cls._instance
    
    def initialize(self):
        """Inicializa la conexión a MongoDB y configura la sincronización automática."""
        self.client = None
        self.db = None
        self.is_connected = False
        self.sync_thread = None
        self.stop_sync = False
        
        # Crear archivos de respaldo si no existen
        for collection_name, file_path in BACKUP_FILES.items():
            if not os.path.exists(file_path):
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump([], f)
        
        # Intentar conexión inicial
        self.connect()
        
        # Iniciar hilo de sincronización
        self.start_sync_thread()
    
    def connect(self):
        """Intenta establecer conexión con MongoDB."""
        try:
            # Comprobar conexión a internet
            if not self._check_internet_connection():
                print("No hay conexión a internet. Modo offline activado.")
                self.is_connected = False
                return False
            
            # Intentar conexión a MongoDB
            print("Intentando conectar a MongoDB...")
            self.client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
            # Verificar conexión
            self.client.admin.command('ping')
            self.db = self.client[DB_NAME]
            self.is_connected = True
            print("Conexión a MongoDB establecida correctamente.")
            return True
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            print(f"Error de conexión a MongoDB: {e}")
            self.is_connected = False
            return False
        except Exception as e:
            print(f"Error inesperado al conectar a MongoDB: {e}")
            print("Trabajando en modo offline.")
            self.is_connected = False
            return False
    
    def _check_internet_connection(self):
        """Verifica si hay conexión a internet."""
        try:
            requests.get("http://www.google.com", timeout=3)
            return True
        except:
            return False
    
    def start_sync_thread(self):
        """Inicia un hilo para sincronización automática."""
        if self.sync_thread is None or not self.sync_thread.is_alive():
            self.stop_sync = False
            self.sync_thread = threading.Thread(target=self._sync_process, daemon=True)
            self.sync_thread.start()
            print(f"Sincronización automática iniciada (cada {SYNC_INTERVAL} segundos).")
    
    def stop_sync_thread(self):
        """Detiene el hilo de sincronización."""
        if self.sync_thread and self.sync_thread.is_alive():
            self.stop_sync = True
            self.sync_thread.join(timeout=1)
            print("Sincronización automática detenida.")
    
    def _sync_process(self):
        """Proceso de sincronización automática."""
        while not self.stop_sync:
            # Intentar sincronizar datos pendientes
            self.sync_all_pending_data()
            
            # Esperar el intervalo definido
            for _ in range(SYNC_INTERVAL):
                if self.stop_sync:
                    break
                time.sleep(1)
    
    def sync_all_pending_data(self):
        """Sincroniza todos los datos pendientes."""
        if not self.is_connected:
            if not self.connect():
                print("Sin conexión. Los datos se guardarán localmente.")
                return False
        
        success = True
        for collection_name in COLLECTIONS.keys():
            if not self._sync_collection_data(collection_name):
                success = False
        
        return success
    
    def _sync_collection_data(self, collection_name):
        """Sincroniza los datos pendientes de una colección específica."""
        backup_file = BACKUP_FILES[collection_name]
        if not os.path.exists(backup_file):
            return True  # No hay archivo de respaldo
        
        try:
            # Leer datos pendientes
            with open(backup_file, 'r', encoding='utf-8') as f:
                pending_data = json.load(f)
            
            if not pending_data:
                return True  # No hay datos pendientes
            
            # Obtener colección
            collection = self.db[COLLECTIONS[collection_name]]
            
            # Insertar datos pendientes
            if len(pending_data) == 1:
                # Usar insertOne para un solo documento
                collection.insert_one(pending_data[0])
                print(f"Se envió 1 documento a la colección {collection_name}")
            else:
                # Usar insertMany para múltiples documentos
                collection.insert_many(pending_data)
                print(f"Se enviaron {len(pending_data)} documentos a la colección {collection_name}")
            
            # Limpiar archivo de respaldo
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump([], f)
            
            print(f"Datos de {collection_name} sincronizados correctamente.")
            return True
        except Exception as e:
            print(f"Error al sincronizar {collection_name}: {e}")
            return False
    
    def insert_document(self, collection_name, document):
        """Inserta un documento en MongoDB o lo guarda en el archivo de respaldo."""
        # Remover el campo es_objeto si existe
        if 'es_objeto' in document:
            document = {k: v for k, v in document.items() if k != 'es_objeto'}
        
        if self.is_connected:
            try:
                collection = self.db[COLLECTIONS[collection_name]]
                result = collection.insert_one(document)
                print(f"Documento insertado en MongoDB con ID: {result.inserted_id}")
                return True
            except Exception as e:
                print(f"Error al insertar en MongoDB: {e}")
                # Guardar en archivo de respaldo
                self._save_to_backup(collection_name, document)
                return False
        else:
            # Guardar en archivo de respaldo
            self._save_to_backup(collection_name, document)
            return False
    
    def _save_to_backup(self, collection_name, document):
        """Guarda un documento en el archivo de respaldo correspondiente."""
        backup_file = BACKUP_FILES[collection_name]
        try:
            # Leer datos existentes
            if os.path.exists(backup_file):
                with open(backup_file, 'r', encoding='utf-8') as f:
                    try:
                        pending_data = json.load(f)
                    except json.JSONDecodeError:
                        pending_data = []
            else:
                pending_data = []
            
            # Agregar nuevo documento
            pending_data.append(document)
            
            # Guardar archivo actualizado
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(pending_data, f, indent=4, ensure_ascii=False)
            
            print(f"Documento guardado en archivo de respaldo {backup_file}")
            return True
        except Exception as e:
            print(f"Error al guardar en archivo de respaldo: {e}")
            return False
    
    def find_documents(self, collection_name, query=None):
        """Busca documentos en MongoDB o en los archivos locales."""
        if self.is_connected:
            try:
                collection = self.db[COLLECTIONS[collection_name]]
                if query is None:
                    cursor = collection.find({})
                else:
                    cursor = collection.find(query)
                return list(cursor)
            except Exception as e:
                print(f"Error al buscar en MongoDB: {e}")
                # Buscar en archivos locales
                return self._find_in_local_files(collection_name, query)
        else:
            # Buscar en archivos locales
            return self._find_in_local_files(collection_name, query)
    
    def _find_in_local_files(self, collection_name, query=None):
        """Busca documentos en los archivos locales."""
        # Primero buscar en archivos regulares
        regular_file = f"{collection_name}.json"
        documents = []
        
        if os.path.exists(regular_file):
            try:
                with open(regular_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                documents.extend(data)
            except:
                pass
        
        # Luego buscar en archivos de respaldo
        backup_file = BACKUP_FILES[collection_name]
        if os.path.exists(backup_file):
            try:
                with open(backup_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                documents.extend(data)
            except:
                pass
        
        # Filtrar por query si es necesario
        if query is not None:
            filtered_docs = []
            for doc in documents:
                match = True
                for key, value in query.items():
                    if key not in doc or doc[key] != value:
                        match = False
                        break
                if match:
                    filtered_docs.append(doc)
            return filtered_docs
        
        return documents
    
    def update_document(self, collection_name, query, update_data):
        """Actualiza un documento en MongoDB o lo marca para actualización posterior."""
        if self.is_connected:
            try:
                collection = self.db[COLLECTIONS[collection_name]]
                result = collection.update_one(query, {"$set": update_data})
                print(f"Documento actualizado en MongoDB. Coincidencias: {result.matched_count}")
                return True
            except Exception as e:
                print(f"Error al actualizar en MongoDB: {e}")
                # Implementar lógica de actualización en archivo local
                return False
        else:
            # Implementar lógica de actualización en archivo local
            return False
    
    def delete_document(self, collection_name, query):
        """Elimina un documento de MongoDB o lo marca para eliminación posterior."""
        if self.is_connected:
            try:
                collection = self.db[COLLECTIONS[collection_name]]
                result = collection.delete_one(query)
                print(f"Documento eliminado de MongoDB. Eliminaciones: {result.deleted_count}")
                return True
            except Exception as e:
                print(f"Error al eliminar de MongoDB: {e}")
                # Implementar lógica de eliminación en archivo local
                return False
        else:
            # Implementar lógica de eliminación en archivo local
            return False