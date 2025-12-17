import pandas as pd

def etiqueta_fondo(fondo, divisor):
    return fondo if divisor == 1 else f"{fondo} (÷ {divisor})"

def columnas_son_fechas(columnas):
    try:
        pd.to_datetime(columnas)
        return True
    except:
        return False

def fechas_unicas_ordenadas(df, es_fecha):
    if es_fecha:
        return (
            df["eje_x"]
            .sort_values()
            .dt.strftime("%Y-%m-%d")
            .unique()
        )
    return df["eje_x"].astype(str).unique()

def get_correct_dict(es_fecha, eje_x_vals):
    if es_fecha:
        return dict(
            type="date",
            tickvals=eje_x_vals,
            ticktext=[pd.to_datetime(f).strftime("%d-%m") for f in eje_x_vals]
        )
    return dict(type="category")
