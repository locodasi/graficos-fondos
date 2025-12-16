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

# Explicacion

## Tabla

Para el uso de la aplicacion, la tabla a graficar debe tener la siguiente estructura:
- La primera columna debe ser la columna agrupadora
- El resto de columnas seran los valores del eje X
- Los valores a graficar deben ser numeros
- Las columnas debe ser fechas (Por ahora)

### Ejemplo de tabla

```
Fondos	                              3/11/2025	   1/12/2025	   9/12/2025	   15/12/2025
Galicia Fima Premium	                  $ 71,784208	   $ 73,103270	   $ 73,377878	   $ 73,580017
Santander Super Fondos Acciones	      $ 490,683043	$ 477,045967	$ 484,584417	$ 475,638150
Santander Super Mix VI	               $ 128,751969	$ 132,736153	$ 133,865660	$ 134,689030
Credicoop 1810  Ahorro	               $ 199,191294	$ 202,866500	$ 203,671400	$ 204,265600
Credicoop 1810 Renta Variable	         $ 236,401288	$ 229,481350	$ 230,333600	$ 225,003520
```

### Ejemplos

En ejemplos.txt podran ver diversos casos de uso de cada una de los tipos de graficos que se pueden hacer

## Explicacion

Solo carga un excel con una tabla en el formato establecido, completa los pasos y crea un grafico.
En el grafico podras hacer cosas como zoom, pasar el mouse para ver mas informacion o descargar el grafico como una imagen.

### Grafico

En la primera seccion podras seleccionar que tipo de grafico queres, las opciones son:

- Grafico de lineas
- Grafico de barras
- Grafico de barras (X=Grupo) (En este caso el eje X serian los grupos y las barras las columnas)
- Grafico de torta (Solo funciona si seleccionar varios grupos y una fecha o varias fechas y un solo grupo)

### Configuracion

Aca podras configurar ciertas cosas del grafico, como por ejemplo si queres que se vean los datos o no, como tambien los titulos del grafico y del eje.

### Filtros

Podras filtrar los datos para solo mostrar los datos de las fechas especificas, como de solo los grupos seleccionados.
Ademas en el caso de que los valores sean muy dispares, lo que no permitiria que el grafico muestre claramente las diferencias de valores, podras a cada grupo dividir sus valores para asi tener una menor disparidad y mejorar el grafico, no te preocupes que en el titulo del grupo aparecera por cuanto lo dividiste, si es que lo dividiste.

### Crear garfico

Solo dale click a Crear gráfico y ya esta.



