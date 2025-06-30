from pymongo import MongoClient
import sys

mongo_uri = "mongodb+srv://admin:admin123@cluster0.3muovte.mongodb.net/?retryWrites=true&w=majority"

try:
    print("Conectando a MongoDB...")
    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
    
    client.admin.command('ping')
    
    print("\nBases de datos disponibles:")
    for db in client.list_database_names():
        print(f" - {db}")
    
    db = client["Escuela"]
    
    print("\nColecciones en la base de datos Escuela:")
    for collection in db.list_collection_names():
        print(f" - {collection}")
    
    print("\n✅ Conexión exitosa!")
    
except Exception as e:
    print(f"\n❌ Error de conexión: {e}")
    print("\nConsejo: Verifica las credenciales y asegúrate de que tu IP tenga acceso.")
    sys.exit(1)