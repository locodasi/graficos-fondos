import streamlit as st
import plotly.graph_objects as go
import pandas as pd

from utils import etiqueta_fondo, fechas_unicas_ordenadas, get_correct_dict
from config import COLUMNA_AGRUPADORA, SI

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
