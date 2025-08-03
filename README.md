# 🧠 NeuroSort

**NeuroSort** es una herramienta interactiva para clasificar imágenes de personajes usando inteligencia artificial. Aprovecha el poder de **CLIP** y un clasificador **KNN**, junto con una interfaz gráfica amigable creada con **Tkinter**, para hacer la organización de imágenes tan precisa como eficiente.

---

## 🚀 Características

- ✅ Clasificación automática de imágenes usando IA (CLIP + KNN)
- ✅ Vista previa de imágenes antes de moverlas
- ✅ Confirmación de clasificación con opción de corrección
- ✅ Clasificación manual optimizada con selección múltiple
- ✅ Creación rápida de carpetas de personajes
- ✅ Registro completo de movimientos en archivo CSV
- ✅ Entrenamiento automático del modelo con respaldo
- ✅ Interfaz gráfica amigable con botones claros

---

## 🖼️ Ejemplo visual

| Clasificación automática con vista previa | Clasificación manual en lote |
|------------------------------------------|-------------------------------|
| ![auto](./docs/preview_auto.png)         | ![manual](./docs/preview_manual.png) |

> Puedes personalizar tus imágenes de demostración en la carpeta `docs/`.

---

## 🧩 Estructura del proyecto

```
NeuroSort/
│
├── data/
│   ├── imagenes_base/           # Imágenes sin clasificar
│   ├── personajes/              # Carpetas por personaje
│   └── logs/
│       └── movimientos.csv      # Historial de movimientos
│
├── models/
│   ├── modelo_knn.pkl           # Modelo entrenado actual
│   └── backups/                 # Backups automáticos
│
├── src/
│   ├── neuro_sort_gui.py        # Interfaz principal
│   ├── entrenar_modelo.py       # Script de entrenamiento
│   └── clasificar_automatico.py # Script de clasificación automática
```

---

## ⚙️ Requisitos

- Python 3.9+
- Recomendado: entorno virtual

### 📦 Dependencias

Instálalas con pip:

```bash
pip install -r requirements.txt
```

Contenido sugerido para `requirements.txt`:

```
torch
ftfy
regex
tqdm
Pillow
scikit-learn
matplotlib
openai-clip
```

---

## 🧪 Cómo usar

### 1. Ejecutar la interfaz

```bash
python src/neuro_sort_gui.py
```

### 2. Funcionalidades disponibles

| Botón                      | Acción                                                                 |
|---------------------------|------------------------------------------------------------------------|
| Crear carpeta de personaje | Crea una carpeta nueva bajo `data/personajes`                         |
| Ver carpetas existentes    | Muestra todas las carpetas de personajes actuales                     |
| Mover imagen manualmente   | Selecciona múltiples imágenes y muévelas rápidamente a una carpeta     |
| Entrenar modelo            | Genera embeddings y entrena el clasificador (usa las carpetas actuales) |
| Clasificación automática   | Predice a qué carpeta mover cada imagen y pregunta si confirmas        |

---

## 📝 Registro

Todos los movimientos (manuales o automáticos) quedan registrados en:

```
data/logs/movimientos.csv
```

Incluye:
- Nombre del archivo
- Acción realizada (auto o manual)
- Etiqueta destino
- Confianza (si aplica)

---

## 🧠 IA y funcionamiento

- Utiliza el modelo **CLIP** para convertir imágenes en embeddings numéricos.
- Luego, se entrena un **KNeighborsClassifier** con las imágenes ya clasificadas.
- Las imágenes nuevas se comparan contra este modelo para predecir su carpeta correcta.

---

## 🛠️ Próximas mejoras (sugerencias)

- ✔️ Eliminación/edición de imágenes desde la GUI
- 📊 Visualizador de estadísticas de clasificación
- 🔄 Botón "Deshacer última acción"
- 📁 Soporte para clasificación por etiquetas secundarias (ropa, emociones, etc.)

---

## 🤝 Autor

Creado por **[Tu Nombre Aquí]**.  
¿Te interesa usar esto para organizar datasets, proyectos de animación o videojuegos? ¡Puedes contribuir!

---

## 📄 Licencia

Este proyecto está bajo la licencia [MIT](LICENSE).
