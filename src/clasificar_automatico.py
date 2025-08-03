import os
import shutil
import torch
import clip
import pickle
import csv
from PIL import Image
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox, ttk

# === RUTAS ABSOLUTAS SEGURAS ===
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CARPETA_BASE = os.path.join(BASE_DIR, "data", "imagenes_base")
CARPETA_PERSONAJES = os.path.join(BASE_DIR, "data", "personajes")
LOG_FILE = os.path.join(BASE_DIR, "data", "logs", "movimientos.csv")
MODELO_PATH = os.path.join(BASE_DIR, "models", "modelo_knn.pkl")

# === Interfaz oculta para diálogos ===
root = tk.Tk()
root.withdraw()

# === Cargar modelo CLIP ===
modelo_clip, preprocess = clip.load("ViT-B/32", device="cuda" if torch.cuda.is_available() else "cpu")

# === Cargar modelo KNN entrenado ===
with open(MODELO_PATH, "rb") as f:
    modelo_knn = pickle.load(f)

def mostrar_imagen(ruta):
    img = Image.open(ruta).convert("RGB")
    plt.imshow(img)
    plt.axis('off')
    plt.title("Vista previa")
    plt.show()

def predecir_personaje(ruta_imagen):
    imagen = preprocess(Image.open(ruta_imagen)).unsqueeze(0).to("cuda" if torch.cuda.is_available() else "cpu")
    with torch.no_grad():
        embedding = modelo_clip.encode_image(imagen)
        embedding = embedding / embedding.norm(dim=-1, keepdim=True)
        vector = embedding.cpu().numpy()[0]

    vecinos = modelo_knn.kneighbors([vector], return_distance=False)[0]
    prediccion = modelo_knn.predict([vector])[0]
    vecinos_vectors = modelo_knn._fit_X[vecinos]
    similitudes = cosine_similarity([vector], vecinos_vectors)[0]
    confianza = max(similitudes)

    return prediccion, confianza

def registrar_movimiento(nombre_archivo, personaje):
    with open(LOG_FILE, mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([nombre_archivo, personaje])

def seleccionar_personaje_manual(carpetas):
    ventana = tk.Toplevel()
    ventana.title("Selecciona carpeta de personaje")
    ventana.geometry("300x120")
    ventana.resizable(False, False)

    tk.Label(ventana, text="Selecciona el personaje:", font=("Arial", 11)).pack(pady=5)
    seleccion = tk.StringVar()
    combobox = ttk.Combobox(ventana, values=carpetas, textvariable=seleccion, state="readonly")
    combobox.pack(pady=5)
    combobox.set(carpetas[0])

    resultado = {"seleccion": None}

    def confirmar():
        resultado["seleccion"] = seleccion.get()
        ventana.destroy()

    def cancelar():
        ventana.destroy()

    boton_frame = tk.Frame(ventana)
    boton_frame.pack(pady=5)

    tk.Button(boton_frame, text="Mover", width=10, command=confirmar).pack(side="left", padx=5)
    tk.Button(boton_frame, text="Cancelar", width=10, command=cancelar).pack(side="right", padx=5)

    ventana.grab_set()
    root.wait_window(ventana)
    return resultado["seleccion"]

def clasificar_imagenes(threshold=0.85):
    imagenes = os.listdir(CARPETA_BASE)
    if not imagenes:
        messagebox.showinfo("Clasificación", "📂 No hay imágenes nuevas para clasificar.")
        return

    for imagen in imagenes:
        ruta = os.path.join(CARPETA_BASE, imagen)
        try:
            prediccion, confianza = predecir_personaje(ruta)
            mostrar_imagen(ruta)

            if confianza >= threshold:
                destino = os.path.join(CARPETA_PERSONAJES, prediccion, imagen)
                shutil.move(ruta, destino)
                registrar_movimiento(imagen, prediccion)
                messagebox.showinfo("✅ Clasificación automática",
                                    f"Imagen '{imagen}' movida a '{prediccion}' con confianza {confianza:.2f}")
            else:
                respuesta = messagebox.askyesno(
                    "🤔 Clasificación con baja confianza",
                    f"Predicción: {prediccion}\nConfianza: {confianza:.2f}\n\n¿Deseas mover la imagen a '{prediccion}'?"
                )
                if respuesta:
                    destino = os.path.join(CARPETA_PERSONAJES, prediccion, imagen)
                    shutil.move(ruta, destino)
                    registrar_movimiento(imagen, prediccion)
                    messagebox.showinfo("✅ Imagen movida", f"Imagen movida a '{prediccion}'")
                else:
                    carpetas = os.listdir(CARPETA_PERSONAJES)
                    seleccion = seleccionar_personaje_manual(carpetas)
                    if seleccion:
                        destino = os.path.join(CARPETA_PERSONAJES, seleccion, imagen)
                        shutil.move(ruta, destino)
                        registrar_movimiento(imagen, seleccion)
                        messagebox.showinfo("✅ Imagen movida", f"Imagen movida manualmente a '{seleccion}'")
                    else:
                        messagebox.showwarning("⚠️ Imagen no movida", "No se seleccionó ningún personaje.")
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error con la imagen '{imagen}':\n{e}")

if __name__ == "__main__":
    clasificar_imagenes()
