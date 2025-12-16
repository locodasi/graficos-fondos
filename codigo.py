import streamlit as st
import pandas as pd
import plotly.graph_objects as go

COLUMNA_AGRUPADORA = "columna_agrupadora_xxxjhtrs"
st.title("Creador de graficos")

archivo = st.file_uploader("Cargá el archivo Excel", type=["xlsx", "xls"])

def crear_grafico_linea(df_plot, fondos_config, mostrar_valores, titulo, titulo_x, titulo_y):
    fig = go.Figure()
    

    for fondo in df_plot[COLUMNA_AGRUPADORA].unique():
        datos = df_plot[df_plot[COLUMNA_AGRUPADORA] == fondo]
        divisor = fondos_config[fondo]["divisor"]

        if divisor == 1:
            label = fondo
        else:
            label = f"{fondo} (÷ {divisor})"

        fig.add_trace(
            go.Scatter(
                x=datos["fecha"],
                y=datos["valor"],
                mode="lines+markers+text" if mostrar_valores=="Sí" else "lines+markers",
                name=label,
                text=datos["valor"].round(2) if mostrar_valores=="Sí" else None,
                textposition="top center"
            )
        )

    fechas_unicas = df_plot["fecha"].sort_values().dt.strftime("%Y-%m-%d").unique()

    fig.update_layout(
        title=titulo,
        template="simple_white",
        xaxis_title=titulo_x,
        yaxis_title=titulo_y,
        xaxis=dict(
            type="date",
            tickvals=fechas_unicas,
            ticktext=[pd.to_datetime(f).strftime("%d-%m") for f in fechas_unicas]
        )
    )

    return fig

def crear_grafico_barra_por_grupo(df_plot, fondos_config, mostrar_valores, titulo, titulo_x, titulo_y):
    fig = go.Figure()

    # Fechas únicas ordenadas
    fechas = sorted(df_plot["fecha"].unique())

    # Fondos (eje X) con divisor en el nombre si corresponde
    fondos_labels = []
    for fondo in df_plot[COLUMNA_AGRUPADORA].unique():
        divisor = fondos_config[fondo]["divisor"]
        if divisor == 1:
            fondos_labels.append(fondo)
        else:
            fondos_labels.append(f"{fondo} (÷ {divisor})")

    # Crear una traza POR FECHA
    for fecha in fechas:
        datos_fecha = df_plot[df_plot["fecha"] == fecha]
        y_vals = datos_fecha["valor"]
        fig.add_trace(
            go.Bar(
                x=fondos_labels,
                y=y_vals,
                name=pd.to_datetime(fecha).strftime("%d-%m"),
                text=y_vals.round(2) if mostrar_valores=="Sí" else None,
                textposition="auto"
            )
        )

    fig.update_layout(
        title=titulo,
        template="simple_white",
        xaxis_title=titulo_x,
        yaxis_title=titulo_y,
        barmode="group"
    )

    return fig

def crear_grafico_barra_por_eje(
    df_plot, fondos_config, mostrar_valores, titulo, titulo_x, titulo_y
):
    fig = go.Figure()

    fechas_unicas = df_plot["fecha"].sort_values().dt.strftime("%Y-%m-%d").unique()

    for fondo in df_plot[COLUMNA_AGRUPADORA].unique():
        datos_fondo = df_plot[df_plot[COLUMNA_AGRUPADORA] == fondo]

        divisor = fondos_config[fondo]["divisor"]
        label = fondo if divisor == 1 else f"{fondo} (÷ {divisor})"

        y_vals = datos_fondo.sort_values("fecha")["valor"]

        fig.add_trace(
            go.Bar(
                x=fechas_unicas,
                y=y_vals,
                name=label,
                text=y_vals.round(2) if mostrar_valores == "Sí" else None,
                textposition="auto"
            )
        )

    fig.update_layout(
        title=titulo,
        template="simple_white",
        xaxis_title=titulo_x,
        yaxis_title=titulo_y,
        barmode="group",
        xaxis=dict(
            type="date",
            tickvals=fechas_unicas,
            ticktext=[pd.to_datetime(f).strftime("%d-%m") for f in fechas_unicas]
        )
    )

    return fig

if archivo is not None:
    # Leer excel
    df = pd.read_excel(archivo)

    # Normalizar columnas
    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.lower()
    )

    # Detectar la primera columna del Excel
    primera_columna = df.columns[0]

    # Renombrar la primera columna con la constante
    df = df.rename(columns={primera_columna: COLUMNA_AGRUPADORA})
    
    columnas_fechas = [c for c in df.columns if c not in COLUMNA_AGRUPADORA]

    # Convertir fechas
    fechas = pd.to_datetime(columnas_fechas)

    # Formulario
    with st.form("form_filtros"):
        st.subheader("Filtros")

        # Rango de fechas
        fecha_inicio, fecha_fin = st.date_input(
            "Seleccioná el rango de fechas",
            value=(fechas.min(), fechas.max())
        )
        
        # Títulos personalizados
        titulo_grafico = st.text_input("Título del gráfico", value="Evolución de fondos")
        titulo_x = st.text_input("Título eje X", value="Fecha")
        titulo_y = st.text_input("Título eje Y", value="Valor")
        
        # Mostrar valores
        mostrar_valores = st.radio(
            "Mostrar valores en el gráfico?",
            ["No", "Sí"]
        )
        
        # 👇 RADIO BUTTON
        tipo_grafico = st.radio(
            "Tipo de gráfico",
            [
                "Líneas",
                "Barras (X = grupos)",
                "Barras"
            ]
        )

        st.markdown("### Grupos y divisores")

        fondos_config = {}

        for fondo in df[COLUMNA_AGRUPADORA].unique():
            col1, col2, col3 = st.columns([2, 2, 2])

            with col1:
                incluir = st.checkbox(f"Incluir {fondo}", value=True)

            with col2:
                divisor = st.number_input(
                    f"Divisor {fondo}",
                    min_value=0.0001,
                    value=1.0,
                    step=0.1,
                    key=f"div_{fondo}"
                )

            fondos_config[fondo] = {
                "incluir": incluir,
                "divisor": divisor
            }

        boton = st.form_submit_button("Crear gráfico")

    # Crear gráfico
    if boton:
        fechas_filtradas = [
            c for c in columnas_fechas
            if fecha_inicio <= pd.to_datetime(c).date() <= fecha_fin
        ]

        df_largo = df.melt(
            id_vars=COLUMNA_AGRUPADORA,
            value_vars=fechas_filtradas,
            var_name="fecha",
            value_name="valor"
        )

        df_largo["fecha"] = pd.to_datetime(df_largo["fecha"])

        # Aplicar filtros y divisores
        filas = []

        for fondo, cfg in fondos_config.items():
            if cfg["incluir"]:
                temp = df_largo[df_largo[COLUMNA_AGRUPADORA] == fondo].copy()
                temp["valor"] = temp["valor"] / cfg["divisor"]
                filas.append(temp)

        if filas:
            df_plot = pd.concat(filas)

            # 👇 ACA SE ELIGE QUÉ FUNCIÓN USAR
            if tipo_grafico == "Líneas":
                fig = crear_grafico_linea(
                    df_plot, fondos_config, mostrar_valores,
                    titulo_grafico, titulo_x, titulo_y
                )

            elif tipo_grafico == "Barras (X = grupos)":
                fig = crear_grafico_barra_por_grupo(
                    df_plot, fondos_config, mostrar_valores,
                    titulo_grafico, titulo_x, titulo_y
                )

            else:  # Barras
                fig = crear_grafico_barra_por_eje(
                    df_plot, fondos_config, mostrar_valores,
                    titulo_grafico, titulo_x, titulo_y
                )
                
            st.session_state["fig"] = fig
            st.plotly_chart(fig, use_container_width=True)

        else:
            st.warning("No seleccionaste ningún fondo.")