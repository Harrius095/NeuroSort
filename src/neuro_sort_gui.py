import os
import shutil
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from PIL import Image, ImageTk
import subprocess
import csv
import datetime




# === RUTAS ABSOLUTAS SEGURAS ===
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CARPETA_BASE = os.path.join(BASE_DIR, "data", "imagenes_base")
CARPETA_PERSONAJES = os.path.join(BASE_DIR, "data", "personajes")
LOGS_FOLDER = os.path.join(BASE_DIR, "data", "logs")
LOG_FILE = os.path.join(LOGS_FOLDER, "movimientos.csv")
MODELO_PATH = os.path.join(BASE_DIR, "models", "modelo_knn.pkl")

# === FUNCIONES ===
def crear_carpeta_personaje():
    nombre = simpledialog.askstring("Nuevo personaje", "Ingresa el nombre del personaje:")
    if not nombre:
        return
    ruta = os.path.join(CARPETA_PERSONAJES, nombre)
    if not os.path.exists(ruta):
        os.makedirs(ruta)
        messagebox.showinfo("Éxito", f"Carpeta '{nombre}' creada.")
    else:
        messagebox.showwarning("Ya existe", f"La carpeta '{nombre}' ya existe.")

def listar_carpetas():
    carpetas = os.listdir(CARPETA_PERSONAJES)
    if not carpetas:
        messagebox.showinfo("Carpetas", "No hay carpetas de personajes aún.")
    else:
        lista = "\n".join(carpetas)
        messagebox.showinfo("Carpetas existentes", lista)





        

def mover_imagen_manual():
    archivos = filedialog.askopenfilenames(
        initialdir=CARPETA_BASE,
        title="Selecciona imágenes",
        filetypes=[("Imágenes", "*.png *.jpg *.jpeg")]
    )

    if not archivos:
        return

    # Obtener lista de carpetas disponibles
    carpetas = os.listdir(CARPETA_PERSONAJES)
    if not carpetas:
        messagebox.showwarning("Sin carpetas", "Primero crea al menos una carpeta de personaje.")
        return

    # Selección única de carpeta
    ventana = tk.Toplevel()
    ventana.title("Seleccionar carpeta de destino")
    ventana.geometry("300x120")

    tk.Label(ventana, text="Selecciona carpeta de destino:").pack(pady=5)
    carpeta_var = tk.StringVar(ventana)
    carpeta_var.set(carpetas[0])  # valor inicial

    menu = tk.OptionMenu(ventana, carpeta_var, *carpetas)
    menu.pack(pady=5)

    def confirmar():
        carpeta_destino = carpeta_var.get()
        destino = os.path.join(CARPETA_PERSONAJES, carpeta_destino)
        if not os.path.exists(destino):
            os.makedirs(destino)

        for archivo in archivos:
            nombre_archivo = os.path.basename(archivo)
            ruta_destino = os.path.join(destino, nombre_archivo)
            shutil.move(archivo, ruta_destino)
            print(f"✅ Imagen movida a '{carpeta_destino}': {nombre_archivo}")

            # Guardar log
            with open(LOG_FILE, "a", encoding="utf-8") as log:
                log.write(f"{nombre_archivo},{carpeta_destino}\n")

        ventana.destroy()
        messagebox.showinfo("Éxito", f"{len(archivos)} imágenes movidas a '{carpeta_destino}'")

    tk.Button(ventana, text="Mover imágenes", command=confirmar).pack(pady=5)













def entrenar_modelo():
    ruta_script = os.path.join(BASE_DIR, "src", "entrenar_modelo.py")
    try:
        resultado = subprocess.run(
            f'python "{ruta_script}"',
            shell=True,
            capture_output=True,
            text=True
        )

        if resultado.returncode == 0:
            messagebox.showinfo("✅ Entrenamiento exitoso", "El modelo fue entrenado y guardado correctamente.")
        else:
            error_salida = resultado.stderr.strip() or resultado.stdout.strip()
            messagebox.showerror("❌ Error al entrenar", f"Ocurrió un problema:\n\n{error_salida}")

    except Exception as e:
        messagebox.showerror("❌ Error crítico", f"No se pudo ejecutar el script:\n{e}")

def clasificar_automatico():
    ruta_script = os.path.join(BASE_DIR, "src", "clasificar_automatico.py")
    try:
        resultado = subprocess.run(
            f'python "{ruta_script}"',
            shell=True,
            capture_output=True,
            text=True
        )

        if resultado.returncode == 0:
            messagebox.showinfo("✅ Clasificación completa", "Clasificación automática terminada.")
        else:
            error_salida = resultado.stderr.strip() or resultado.stdout.strip()
            messagebox.showerror("❌ Error al clasificar", f"Ocurrió un problema:\n\n{error_salida}")

    except Exception as e:
        messagebox.showerror("❌ Error crítico", f"No se pudo ejecutar el script:\n{e}")


        

def salir():
    root.destroy()

# === INTERFAZ GRÁFICA ===
root = tk.Tk()
root.title("🧠 NeuroSort")
root.geometry("300x350")
root.resizable(False, False)

tk.Label(root, text="NeuroSort", font=("Helvetica", 18)).pack(pady=10)

tk.Button(root, text="📁 Crear carpeta de personaje", command=crear_carpeta_personaje).pack(pady=5)
tk.Button(root, text="📂 Ver carpetas existentes", command=listar_carpetas).pack(pady=5)
tk.Button(root, text="🖼️ Mover imagen manualmente", command=mover_imagen_manual).pack(pady=5)
tk.Button(root, text="⚙️ Entrenar modelo", command=entrenar_modelo).pack(pady=5)
tk.Button(root, text="🤖 Clasificación automática", command=clasificar_automatico).pack(pady=5)
tk.Button(root, text="❌ Salir", command=salir).pack(pady=20)

root.mainloop()
