from pymongo import MongoClient, errors

def conectar_mongo():
    try:
        uri = "mongodb+srv://admin:admin123@cluster0.3muovte.mongodb.net/?retryWrites=true&w=majority"
        client = MongoClient(uri, serverSelectionTimeoutMS=3000)
        client.admin.command('ping')
        return client
    except errors.PyMongoError:
        return None