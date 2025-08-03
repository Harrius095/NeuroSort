import os
import clip
import torch
import pickle
from PIL import Image
from sklearn.neighbors import KNeighborsClassifier
from datetime import datetime

# === RUTAS SEGURAS ===
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CARPETA_PERSONAJES = os.path.join(BASE_DIR, "data", "personajes")
MODELO_PATH = os.path.join(BASE_DIR, "models", "modelo_knn.pkl")
BACKUP_FOLDER = os.path.join(BASE_DIR, "models", "backups")

# === DISPOSITIVO ===
DISPOSITIVO = "cuda" if torch.cuda.is_available() else "cpu"

# === CARGAR MODELO CLIP ===
modelo, preprocess = clip.load("ViT-B/32", device=DISPOSITIVO)

def obtener_embeddings_y_etiquetas():
    embeddings, etiquetas, nombres = [], [], []

    if not os.path.isdir(CARPETA_PERSONAJES):
        print(f"La carpeta '{CARPETA_PERSONAJES}' no existe.")
        return [], [], []

    for personaje in sorted(os.listdir(CARPETA_PERSONAJES)):
        ruta_personaje = os.path.join(CARPETA_PERSONAJES, personaje)
        if not os.path.isdir(ruta_personaje):
            continue

        for archivo in os.listdir(ruta_personaje):
            ruta_imagen = os.path.join(ruta_personaje, archivo)
            try:
                imagen = Image.open(ruta_imagen).convert("RGB")
                tensor = preprocess(imagen).unsqueeze(0).to(DISPOSITIVO)

                with torch.no_grad():
                    emb = modelo.encode_image(tensor)
                    emb = emb / emb.norm(dim=-1, keepdim=True)
                    embeddings.append(emb.cpu().numpy()[0])
                    etiquetas.append(personaje)
                    nombres.append(archivo)
            except Exception as e:
                print(f"Error al procesar '{archivo}': {e}")
    
    return embeddings, etiquetas, nombres

def entrenar_y_guardar_modelo():
    print("Obteniendo datos de entrenamiento...")
    X, y, _ = obtener_embeddings_y_etiquetas()

    if not X:
        print("No se encontraron imágenes válidas para entrenar.")
        return

    print(f"Entrenando modelo con {len(X)} imágenes de {len(set(y))} personajes...")
    n_vecinos = min(3, len(X))
    knn = KNeighborsClassifier(n_neighbors=n_vecinos)
    knn.fit(X, y)

    os.makedirs(os.path.dirname(MODELO_PATH), exist_ok=True)
    os.makedirs(BACKUP_FOLDER, exist_ok=True)

    # Guardar versión principal
    with open(MODELO_PATH, "wb") as f:
        pickle.dump(knn, f)
    print(f"Modelo guardado en: {MODELO_PATH}")

    # Guardar copia con fecha y hora
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(BACKUP_FOLDER, f"modelo_knn_{timestamp}.pkl")
    with open(backup_path, "wb") as f:
        pickle.dump(knn, f)
    print(f"Copia de respaldo creada: {backup_path}")

if __name__ == "__main__":
    entrenar_y_guardar_modelo()
