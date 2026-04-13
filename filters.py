import streamlit as st
import pandas as pd
from config import COLUMNA_AGRUPADORA


def filtros_columnas(columnas_x, es_fecha):
    if es_fecha:
        fechas = pd.to_datetime(columnas_x)

        rango = st.date_input(
            "Seleccioná el rango de fechas",
            value=(fechas.min(), fechas.max())
        )

        if not (isinstance(rango, tuple) and len(rango) == 2):
            st.info("Seleccioná fecha de inicio y fin")
            return []

        ini, fin = rango

        columnas_en_rango = [
            c for c in columnas_x
            if ini <= pd.to_datetime(c).date() <= fin
        ]

        opciones = {
            pd.to_datetime(c).strftime("%d-%m-%Y"): c
            for c in columnas_en_rango
        }

    else:
        col_a, col_b = st.columns(2)

        with col_a:
            idx_ini = st.number_input(
                "Desde columna Nº",
                min_value=1,
                max_value=len(columnas_x),
                value=1
            )

        with col_b:
            idx_fin = st.number_input(
                "Hasta columna Nº",
                min_value=1,
                max_value=len(columnas_x),
                value=len(columnas_x)
            )

        columnas_en_rango = columnas_x[idx_ini-1:idx_fin]
        opciones = {c: c for c in columnas_en_rango}

    labels = st.multiselect(
        "Seleccioná las columnas a graficar",
        options=list(opciones.keys()),
        default=list(opciones.keys())
    )

    # 🔑 mantener orden original
    return [
        c for c in columnas_en_rango
        if c in [opciones[l] for l in labels]
    ]


def filtros_fondos(df):
    fondos_config = {}

    for fondo in df[COLUMNA_AGRUPADORA].unique():
        col1, col2 = st.columns(2)

        with col1:
            incluir = st.checkbox(f"Incluir {fondo}", value=True)

        with col2:
            divisor = st.number_input(
                f"Divisor {fondo}",
                min_value=1,
                value=1,
                step=1,
                key=f"div_{fondo}"
            )

        fondos_config[fondo] = {
            "incluir": incluir,
            "divisor": divisor
        }

    return fondos_config
