import streamlit as st
import pandas as pd
import plotly.graph_objects as go

COLUMNA_AGRUPADORA = "columna_agrupadora_xxxjhtrs"

GRAF_LINEAS = "Líneas"
GRAF_BARRAS_EJE = "Barras"
GRAF_BARRAS_GRUPO = "Barras (X = grupos)"
GRAF_TORTA = "Torta"

SI = "Sí"
NO = "No"

def etiqueta_fondo(fondo, divisor):
    return fondo if divisor == 1 else f"{fondo} (÷ {divisor})"

def fechas_unicas_ordenadas(df, es_fecha):
    if es_fecha:
        return (
            df["eje_x"]
            .sort_values()
            .dt.strftime("%Y-%m-%d")
            .unique()
        )
    else:
        return df["eje_x"].astype(str).unique()

def columnas_son_fechas(columnas):
    try:
        pd.to_datetime(columnas)
        return True
    except:
        return False

def get_correct_dict(es_fecha, fechas_unicas):
    if es_fecha:
        return dict(
            type="date",
            tickvals=fechas_unicas,
            ticktext=[pd.to_datetime(f).strftime("%d-%m") for f in fechas_unicas]
        )
    else:
        return dict(
                type="category",
            )

st.title("Creador de graficos")

archivo = st.file_uploader("Cargá el archivo Excel", type=["xlsx", "xls"])

def crear_grafico_linea(df_plot, fondos_config, mostrar_valores, titulo, titulo_x, titulo_y, es_fecha, **kwargs):
    fig = go.Figure()
    

    for fondo in df_plot[COLUMNA_AGRUPADORA].unique():
        datos = df_plot[df_plot[COLUMNA_AGRUPADORA] == fondo]

        label = etiqueta_fondo(fondo, fondos_config[fondo]["divisor"])


        fig.add_trace(
            go.Scatter(
                x=datos["eje_x"],
                y=datos["valor"],
                mode="lines+markers+text" if mostrar_valores==SI else "lines+markers",
                name=label,
                text=datos["valor"].round(2) if mostrar_valores==SI else None,
                textposition="top center"
            )
        )

    fechas_unicas = fechas_unicas_ordenadas(df_plot, es_fecha)

    fig.update_layout(
        title=titulo,
        template="simple_white",
        xaxis_title=titulo_x,
        yaxis_title=titulo_y,
        xaxis=get_correct_dict(es_fecha, fechas_unicas)
    )

    return fig

def crear_grafico_barra_por_grupo(
    df_plot, fondos_config, mostrar_valores,
    titulo, titulo_x, titulo_y, es_fecha, **kwargs
):
    fig = go.Figure()

    eje_x_vals = df_plot["eje_x"].unique()

    # Fondos (eje X)
    fondos_labels = [
        etiqueta_fondo(f, fondos_config[f]["divisor"])
        for f in df_plot[COLUMNA_AGRUPADORA].unique()
    ]

    for x_val in eje_x_vals:
        datos = df_plot[df_plot["eje_x"] == x_val]
        y_vals = datos["valor"]

        nombre = (
            pd.to_datetime(x_val).strftime("%d-%m")
            if es_fecha else str(x_val)
        )

        fig.add_trace(
            go.Bar(
                x=fondos_labels,
                y=y_vals,
                name=nombre,
                text=y_vals.round(2) if mostrar_valores == SI else None,
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
    df_plot, fondos_config, mostrar_valores,
    titulo, titulo_x, titulo_y, es_fecha, **kwargs
):
    fig = go.Figure()

    eje_x_vals = fechas_unicas_ordenadas(df_plot, es_fecha)

    for fondo in df_plot[COLUMNA_AGRUPADORA].unique():
        datos = df_plot[df_plot[COLUMNA_AGRUPADORA] == fondo]

        label = etiqueta_fondo(fondo, fondos_config[fondo]["divisor"])

        fig.add_trace(
            go.Bar(
                x=eje_x_vals,
                y=datos["valor"],
                name=label,
                text=datos["valor"].round(2) if mostrar_valores == SI else None,
                textposition="auto"
            )
        )

    fig.update_layout(
        title=titulo,
        template="simple_white",
        xaxis_title=titulo_x,
        yaxis_title=titulo_y,
        barmode="group",
        xaxis=get_correct_dict(es_fecha, eje_x_vals)
    )

    return fig

def crear_grafico_torta(df_plot, titulo, mostrar_valores, es_fecha, **kwargs):

    fondos_config = kwargs.get("fondos_config", {})

    grupos = df_plot[COLUMNA_AGRUPADORA].unique()
    eje_x_vals = df_plot["eje_x"].unique()

    textinfo = "percent+label" + ("+value" if mostrar_valores == SI else "")

    # --- 1 grupo, varias columnas ---
    if len(grupos) == 1 and len(eje_x_vals) > 1:
        datos = df_plot.sort_values("eje_x")

        labels = (
            datos["eje_x"].dt.strftime("%d-%m")
            if es_fecha else datos["eje_x"].astype(str)
        )

        fig = go.Figure(
            data=[go.Pie(
                labels=labels,
                values=datos["valor"],
                textinfo=textinfo
            )]
        )

        fondo = grupos[0]
        fig.update_layout(
            title=f"{titulo} – {etiqueta_fondo(fondo, fondos_config[fondo]['divisor'])}",
            template="simple_white"
        )
        return fig

    # --- 1 columna, varios grupos ---
    elif len(eje_x_vals) == 1 and len(grupos) > 1:
        labels = [
            etiqueta_fondo(f, fondos_config[f]["divisor"])
            for f in df_plot[COLUMNA_AGRUPADORA]
        ]

        titulo_x_val = (
            pd.to_datetime(eje_x_vals[0]).strftime("%d-%m")
            if es_fecha else str(eje_x_vals[0])
        )

        fig = go.Figure(
            data=[go.Pie(
                labels=labels,
                values=df_plot["valor"],
                textinfo=textinfo
            )]
        )

        fig.update_layout(
            title=f"{titulo} – {titulo_x_val}",
            template="simple_white"
        )
        return fig

    else:
        st.warning(
            "⚠️ El gráfico de torta requiere:\n"
            "- una sola columna y varios grupos\n"
            "- o un solo grupo y varias columnas"
        )
        return None

GRAFICOS = {
    GRAF_LINEAS: crear_grafico_linea,
    GRAF_BARRAS_GRUPO: crear_grafico_barra_por_grupo,
    GRAF_BARRAS_EJE: crear_grafico_barra_por_eje,
    GRAF_TORTA: crear_grafico_torta
}

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
    
    columnas_x = [c for c in df.columns if c != COLUMNA_AGRUPADORA]
    es_fecha = columnas_son_fechas(columnas_x)

    # Formulario
    with st.form("form_filtros"):
        
        st.markdown("## Tipo de grafico")
        
        # 👇 RADIO BUTTON
        tipo_grafico = st.radio(
            "Tipo de gráfico",
            [
                GRAF_LINEAS,
                GRAF_BARRAS_EJE,
                GRAF_BARRAS_GRUPO,
                GRAF_TORTA
            ]
        )
        
        st.markdown("## Configuracion")
        
        st.markdown("### Titulos")
        
        # Títulos personalizados
        titulo_grafico = st.text_input("Título del gráfico", value="Evolución de fondos")
        titulo_x = st.text_input("Título eje X", value="Fecha")
        titulo_y = st.text_input("Título eje Y", value="Valor")
        
        # Mostrar valores
        mostrar_valores = st.radio(
            "Mostrar valores en el gráfico?",
            [NO, SI]
        )
        
        st.markdown("## Filtros")


        if es_fecha:
            fechas = pd.to_datetime(columnas_x)

            fecha_inicio, fecha_fin = st.date_input(
                "Seleccioná el rango de fechas",
                value=(fechas.min(), fechas.max())
            )
        else:
            col_a, col_b = st.columns(2)

            with col_a:
                idx_inicio = st.number_input(
                    "Desde columna Nº",
                    min_value=1,
                    max_value=len(columnas_x),
                    value=1,
                    step=1
                )

            with col_b:
                idx_fin = st.number_input(
                    "Hasta columna Nº",
                    min_value=1,
                    max_value=len(columnas_x),
                    value=len(columnas_x),
                    step=1
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
        if es_fecha:
            columnas_seleccionadas = [
                c for c in columnas_x
                if fecha_inicio <= pd.to_datetime(c).date() <= fecha_fin
            ]
        else:
            
            if idx_fin < idx_inicio:
                st.error("⚠️ El número final no puede ser menor que el inicial")
                st.stop()
            columnas_seleccionadas = columnas_x[idx_inicio-1 : idx_fin]
        
        if not columnas_seleccionadas:
            st.warning("No hay columnas dentro del rango seleccionado")
            st.stop()

        df_largo = df.melt(
            id_vars=COLUMNA_AGRUPADORA,
            value_vars=columnas_seleccionadas,
            var_name="eje_x",
            value_name="valor"
        )

        if es_fecha:
            df_largo["eje_x"] = pd.to_datetime(df_largo["eje_x"])

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
            fig = GRAFICOS[tipo_grafico](
                df_plot=df_plot,
                fondos_config=fondos_config,
                mostrar_valores=mostrar_valores,
                titulo=titulo_grafico,
                titulo_x=titulo_x,
                titulo_y=titulo_y,
                es_fecha=es_fecha
            )
                
            if fig is not None:
                st.plotly_chart(fig, use_container_width=True)

        else:
            st.warning("No seleccionaste ningún fondo.")