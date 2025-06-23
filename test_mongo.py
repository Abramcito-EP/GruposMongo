from pymongo import MongoClient
import sys

# URL de conexión
mongo_uri = "mongodb+srv://admin:123456@cluster0.3muovte.mongodb.net/?retryWrites=true&w=majority"

try:
    # Intentar conexión
    print("Conectando a MongoDB...")
    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
    
    # Verificar la conexión
    client.admin.command('ping')
    
    # Listar bases de datos disponibles
    print("\nBases de datos disponibles:")
    for db in client.list_database_names():
        print(f" - {db}")
    
    # Conectar a la base de datos específica
    db = client["Escuela"]
    
    # Listar colecciones en la base de datos
    print("\nColecciones en la base de datos Escuela:")
    for collection in db.list_collection_names():
        print(f" - {collection}")
    
    print("\n✅ Conexión exitosa!")
    
except Exception as e:
    print(f"\n❌ Error de conexión: {e}")
    print("\nConsejo: Verifica las credenciales y asegúrate de que tu IP tenga acceso.")
    sys.exit(1)