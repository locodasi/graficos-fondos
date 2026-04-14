import pandas as pd
from config import COLUMNA_AGRUPADORA


def normalizar_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.lower()
    )

    primera_columna = df.columns[0]
    df = df.rename(columns={primera_columna: COLUMNA_AGRUPADORA})

    # Cortar en la primera fila donde el nombre del fondo sea NaN
    primer_nan = df[COLUMNA_AGRUPADORA].isna().idxmax()
    if df[COLUMNA_AGRUPADORA].isna().any():
        df = df.iloc[:primer_nan]
        
    return df


def obtener_columnas_x(df):
    columnas_x = [c for c in df.columns if c != COLUMNA_AGRUPADORA]
    return columnas_x


def preparar_df_plot(df, columnas_seleccionadas, fondos_config, es_fecha):
    df_largo = df.melt(
        id_vars=COLUMNA_AGRUPADORA,
        value_vars=columnas_seleccionadas,
        var_name="eje_x",
        value_name="valor"
    )

    if es_fecha:
        df_largo["eje_x"] = pd.to_datetime(df_largo["eje_x"])

    filas = []
    for fondo, cfg in fondos_config.items():
        if cfg["incluir"]:
            temp = df_largo[df_largo[COLUMNA_AGRUPADORA] == fondo].copy()
            temp["valor"] = temp["valor"] / cfg["divisor"]
            filas.append(temp)

    if not filas:
        return None

    return pd.concat(filas)
