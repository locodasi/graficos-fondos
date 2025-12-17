import streamlit as st
import pandas as pd

from config import *
from utils import columnas_son_fechas
from graficos import *
from data import normalizar_df, obtener_columnas_x, preparar_df_plot
from filters import filtros_columnas, filtros_fondos


GRAFICOS = {
    GRAF_LINEAS: crear_grafico_linea,
    GRAF_BARRAS_GRUPO: crear_grafico_barra_por_grupo,
    GRAF_BARRAS_EJE: crear_grafico_barra_por_eje,
    GRAF_TORTA: crear_grafico_torta
}

st.title("Creador de gráficos")

archivo = st.file_uploader("Cargá el archivo Excel", type=["xlsx", "xls"])

if archivo is not None:
    df = pd.read_excel(archivo)
    df = normalizar_df(df)

    columnas_x = obtener_columnas_x(df)
    es_fecha = columnas_son_fechas(columnas_x)

    with st.container(border=True):

        st.markdown("## Tipo de gráfico")
        
        tipo_grafico = st.radio(
            "Tipo de gráfico",
            list(GRAFICOS.keys())
        )

        st.markdown("## Configuración")
        titulo = st.text_input("Título del gráfico", "Evolución de fondos")
        titulo_x = st.text_input("Título eje X", "Fecha")
        titulo_y = st.text_input("Título eje Y", "Valor")

        mostrar_valores = st.radio(
            "Mostrar valores",
            [NO, SI]
        )

        st.markdown("## Filtros")
        columnas_seleccionadas = filtros_columnas(columnas_x, es_fecha)

        st.markdown("## Grupos y divisores")
        fondos_config = filtros_fondos(df)

        with st.form("form_graficar", border=False):
            boton = st.form_submit_button("Crear gráfico")

    if boton:
        if not columnas_seleccionadas:
            st.warning("No seleccionaste columnas")
            st.stop()

        df_plot = preparar_df_plot(
            df,
            columnas_seleccionadas,
            fondos_config,
            es_fecha
        )

        if df_plot is None:
            st.warning("No seleccionaste ningún fondo")
            st.stop()

        fig = GRAFICOS[tipo_grafico](
            df_plot=df_plot,
            fondos_config=fondos_config,
            mostrar_valores=mostrar_valores,
            titulo=titulo,
            titulo_x=titulo_x,
            titulo_y=titulo_y,
            es_fecha=es_fecha
        )

        if fig is not None:
            st.plotly_chart(fig, use_container_width=True)
