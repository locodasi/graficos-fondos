import streamlit as st
import pandas as pd

from config import *
from utils import *
from graficos import *


GRAFICOS = {
    GRAF_LINEAS: crear_grafico_linea,
    GRAF_BARRAS_GRUPO: crear_grafico_barra_por_grupo,
    GRAF_BARRAS_EJE: crear_grafico_barra_por_eje,
    GRAF_TORTA: crear_grafico_torta
}

st.title("Creador de graficos")

archivo = st.file_uploader("Cargá el archivo Excel", type=["xlsx", "xls"])

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