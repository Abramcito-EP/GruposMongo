MONGO_URI = "mongodb+srv://admin:admin123@cluster0.3muovte.mongodb.net/?retryWrites=true&w=majority"

DB_NAME = "Escuela"

COLLECTIONS = {
    "alumnos": "alumnos",
    "maestros": "maestros",
    "grupos": "grupos"
}

BACKUP_FILES = {
    "alumnos": "alumnos_sin_enviar.json",
    "maestros": "maestros_sin_enviar.json",
    "grupos": "grupos_sin_enviar.json"
}

SYNC_INTERVAL = 20