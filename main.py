from AlumnoUI import AlumnoUI
from MaestroUI import MaestroUI
from GrupoUI import GrupoUI
from alumno import Alumno
from maestro import Maestro
from grupo import Grupo
from mongo_manager import MongoManager

def main():
    # Inicializar el administrador de MongoDB (esto inicia la sincronización automática)
    mongo_manager = MongoManager()
    
    # Mostrar estado de conexión
    if mongo_manager.is_connected:
        print("Conectado a MongoDB. Los datos se guardarán en la nube.")
    else:
        print("Trabajando en modo offline. Los datos se guardarán localmente.")
    
    while True:
        print("\n=== SISTEMA DE GESTIÓN ESCOLAR ===")
        print("1. Gestionar Alumnos")
        print("2. Gestionar Maestros")
        print("3. Gestionar Grupos")
        print("4. Sincronizar datos con MongoDB manualmente")
        print("5. Ver estado de conexión")
        print("6. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            # Cargar alumnos
            alumnos = Alumno()
            interfaz = AlumnoUI(alumnos, "alumnos.json")
            interfaz.menu()
        elif opcion == "2":
            # Cargar maestros
            maestros = Maestro()
            interfaz = MaestroUI(maestros, "maestros.json")
            interfaz.menu()
        elif opcion == "3":
            # Cargar grupos
            grupos = Grupo()
            interfaz = GrupoUI(grupos, "grupos.json")
            interfaz.menu()
        elif opcion == "4":
            # Sincronizar datos manualmente
            print("Sincronizando datos con MongoDB...")
            if mongo_manager.sync_all_pending_data():
                print("Sincronización manual completada.")
            else:
                print("No se pudieron sincronizar todos los datos.")
        elif opcion == "5":
            # Ver estado de conexión
            if mongo_manager.is_connected:
                print("Conectado a MongoDB. Los datos se guardan directamente en la nube.")
            else:
                print("Trabajando en modo offline. Los datos se guardan localmente.")
                print("Se intentará sincronizar automáticamente cada 20 segundos.")
                
            # Mostrar datos pendientes
            for collection_name, backup_file in mongo_manager.BACKUP_FILES.items():
                try:
                    with open(backup_file, 'r') as f:
                        data = json.load(f)
                    print(f"Datos pendientes en {collection_name}: {len(data)}")
                except:
                    print(f"No hay datos pendientes en {collection_name}")
        elif opcion == "6":
            print("Gracias por usar el sistema. ¡Hasta pronto!")
            
            # Detener hilo de sincronización antes de salir
            mongo_manager.stop_sync_thread()
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()