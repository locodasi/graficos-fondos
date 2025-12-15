# 📊 App de Gráficos de Fondos (Streamlit)

Esta aplicación permite cargar un Excel, aplicar divisores por fondo y generar gráficos interactivos (líneas o barras) usando **Streamlit + Plotly**, sin necesidad de instalar Python en la computadora de destino.

---

## 📁 Estructura de carpetas esperada

La carpeta principal (por ejemplo `graficos/`) debe quedar así:

```

graficos/
│
├─ codigo.py
├─ run_app.bat
├─ python/
│ ├─ python.exe
│ ├─ python311.zip
│ ├─ python311._pth
│ └─ (otros archivos del Python embebido)

```


---

## 🐍 Descargar Python embebido (solo una vez)

1. Descargar **Python embebido para Windows** (zip):
   👉 https://www.python.org/downloads/windows/

   Elegir por ejemplo:
   **Python 3.11 – Embedded ZIP (64-bit)**
2. Crear la carpeta python

3. Descomprimir **todo el zip** dentro de la carpeta.


---

## ✏️ Configurar Python embebido

### 1️⃣ Editar `python311._pth` (o la version qu etengas)

Abrir el archivo `python311._pth` y dejarlo así:

```txt
python311.zip
.
Lib\site-packages

import site
```

### Muy importante:

Eliminar el # delante de import site

Asegurarse de que exista la línea .

# 📦 Instalar pip

Descargar get-pip.py:
👉 https://bootstrap.pypa.io/get-pip.py

Guardar get-pip.py dentro de la carpeta graficos/

Desde la carpeta graficos, ejecutar en la terminal:

python\python.exe get-pip.py

# 📦 Instalar librerías necesarias

Desde la carpeta graficos, ejecutar:

python\python.exe -m pip install streamlit pandas plotly openpyxl

# Uso

Para usar haz doble click en run_app
