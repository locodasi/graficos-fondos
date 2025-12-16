import streamlit as st
import pandas as pd
import plotly.graph_objects as go


st.title("Evolución de fondos (diferencia vs base)")

archivo = st.file_uploader("Cargá el archivo Excel", type=["xlsx", "xls"])

def crear_grafico_linea(df_plot, fondos_config):
    fig = go.Figure()
    

    for fondo in df_plot["fondos"].unique():
        datos = df_plot[df_plot["fondos"] == fondo]
        divisor = fondos_config[fondo]["divisor"]

        if divisor == 1:
            label = fondo
        else:
            label = f"{fondo} (÷ {divisor})"

        fig.add_trace(
            go.Scatter(
                x=datos["fecha"],
                y=datos["valor"],
                mode="lines+markers",
                name=label
            )
        )

    fechas_unicas = df_plot["fecha"].sort_values().dt.strftime("%Y-%m-%d").unique()

    fig.update_layout(
        title="Evolución de fondos",
        template="simple_white",
        xaxis_title="Fecha",
        yaxis_title="Diferencia vs base (ajustada)",
        xaxis=dict(
            type="date",
            tickvals=fechas_unicas,
            ticktext=[pd.to_datetime(f).strftime("%d-%m") for f in fechas_unicas]
        )
    )

    return fig

def crear_grafico_barra(df_plot, fondos_config):
    fig = go.Figure()

    # Fechas únicas ordenadas
    fechas = sorted(df_plot["fecha"].unique())

    # Fondos (eje X) con divisor en el nombre si corresponde
    fondos_labels = []
    for fondo in df_plot["fondos"].unique():
        divisor = fondos_config[fondo]["divisor"]
        if divisor == 1:
            fondos_labels.append(fondo)
        else:
            fondos_labels.append(f"{fondo} (÷ {divisor})")

    # Crear una traza POR FECHA
    for fecha in fechas:
        datos_fecha = df_plot[df_plot["fecha"] == fecha]

        fig.add_trace(
            go.Bar(
                x=fondos_labels,               # 👈 eje X = fondos
                y=datos_fecha["valor"],        # valores
                name=pd.to_datetime(fecha).strftime("%d-%m")  # color = fecha
            )
        )

    fig.update_layout(
        title="Comparación de fondos por fecha",
        template="simple_white",
        xaxis_title="Fondos",
        yaxis_title="Diferencia vs base (ajustada)",
        barmode="group"   # 👈 barras lado a lado
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

    columnas_fijas = ["fondos"]
    columnas_fechas = [c for c in df.columns if c not in columnas_fijas]

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
        
        # 👇 RADIO BUTTON
        tipo_grafico = st.radio(
            "Tipo de gráfico",
            ["Líneas", "Barras"]
        )

        st.markdown("### Fondos y divisores")

        fondos_config = {}

        for fondo in df["fondos"].unique():
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
            id_vars="fondos",
            value_vars=fechas_filtradas,
            var_name="fecha",
            value_name="valor"
        )

        df_largo["fecha"] = pd.to_datetime(df_largo["fecha"])

        # Aplicar filtros y divisores
        filas = []

        for fondo, cfg in fondos_config.items():
            if cfg["incluir"]:
                temp = df_largo[df_largo["fondos"] == fondo].copy()
                temp["valor"] = temp["valor"] / cfg["divisor"]
                filas.append(temp)

        if filas:
            df_plot = pd.concat(filas)

            # 👇 ACA SE ELIGE QUÉ FUNCIÓN USAR
            if tipo_grafico == "Líneas":
                fig = crear_grafico_linea(df_plot, fondos_config)
            else:
                fig = crear_grafico_barra(df_plot, fondos_config)
                
            st.session_state["fig"] = fig
            st.plotly_chart(fig, use_container_width=True)

        else:
            st.warning("No seleccionaste ningún fondo.")