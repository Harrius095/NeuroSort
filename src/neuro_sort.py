import os
import shutil
import csv

BASE_FOLDER = "imagenes_base"
PERSONAJES_FOLDER = "personajes"
LOG_FOLDER = "logs"
LOG_FILE = os.path.join(LOG_FOLDER, "movimientos.csv")

def crear_estructura():
    os.makedirs(BASE_FOLDER, exist_ok=True)
    os.makedirs(PERSONAJES_FOLDER, exist_ok=True)
    os.makedirs(LOG_FOLDER, exist_ok=True)
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["archivo", "personaje"])

def crear_carpeta_personaje(nombre_personaje):
    ruta = os.path.join(PERSONAJES_FOLDER, nombre_personaje)
    if not os.path.exists(ruta):
        os.makedirs(ruta)
        print(f"✅ Carpeta '{nombre_personaje}' creada.")
    else:
        print(f"⚠️ La carpeta '{nombre_personaje}' ya existe.")

def listar_carpetas():
    carpetas = os.listdir(PERSONAJES_FOLDER)
    if carpetas:
        print("📁 Carpetas de personajes:")
        for c in carpetas:
            print(f"- {c}")
    else:
        print("❌ No hay carpetas creadas.")

def listar_imagenes_base():
    imagenes = os.listdir(BASE_FOLDER)
    if not imagenes:
        print("📂 No hay imágenes en la carpeta base.")
    return imagenes

def mover_imagen():
    imagenes = listar_imagenes_base()
    if not imagenes:
        return
    print("\n📷 Imágenes disponibles:")
    for idx, img in enumerate(imagenes):
        print(f"{idx+1}. {img}")
    try:
        eleccion = int(input("Selecciona el número de la imagen a mover: ")) - 1
        if eleccion < 0 or eleccion >= len(imagenes):
            print("❌ Selección inválida.")
            return
        archivo = imagenes[eleccion]
        personaje = input("Ingresa el nombre del personaje (carpeta destino): ").strip()
        carpeta_destino = os.path.join(PERSONAJES_FOLDER, personaje)
        if not os.path.exists(carpeta_destino):
            print("⚠️ Carpeta no encontrada. ¿Deseas crearla? (s/n)")
            if input().lower() == 's':
                crear_carpeta_personaje(personaje)
            else:
                return
        origen = os.path.join(BASE_FOLDER, archivo)
        destino = os.path.join(carpeta_destino, archivo)
        shutil.move(origen, destino)
        registrar_movimiento(archivo, personaje)
        print(f"✅ Imagen '{archivo}' movida a '{personaje}'")
    except ValueError:
        print("❌ Entrada inválida.")

def registrar_movimiento(archivo, personaje):
    with open(LOG_FILE, mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([archivo, personaje])

def mostrar_menu():
    print("\n==== Menú NeuroSort ====")
    print("1. Crear carpeta de personaje")
    print("2. Listar carpetas de personajes")
    print("3. Mover imagen a carpeta")
    print("4. Salir")

def main():
    crear_estructura()
    while True:
        mostrar_menu()
        opcion = input("Elige una opción: ")
        if opcion == "1":
            nombre = input("Nombre del personaje: ").strip()
            crear_carpeta_personaje(nombre)
        elif opcion == "2":
            listar_carpetas()
        elif opcion == "3":
            mover_imagen()
        elif opcion == "4":
            print("👋 Cerrando NeuroSort...")
            break
        else:
            print("❌ Opción inválida.")

if __name__ == "__main__":
    main()
