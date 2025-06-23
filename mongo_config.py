# Configuración para MongoDB

# URL de conexión a MongoDB Atlas
MONGO_URI = "mongodb+srv://admin:admin123@cluster0.3muovte.mongodb.net/?retryWrites=true&w=majority"

# Nombre de la base de datos
DB_NAME = "Escuela"

# Colecciones
COLLECTIONS = {
    "alumnos": "alumnos",
    "maestros": "maestros",
    "grupos": "grupos"
}

# Archivos de respaldo para datos sin enviar
BACKUP_FILES = {
    "alumnos": "alumnos_sin_enviar.json",
    "maestros": "maestros_sin_enviar.json",
    "grupos": "grupos_sin_enviar.json"
}

# Intervalo de sincronización en segundos
SYNC_INTERVAL = 20