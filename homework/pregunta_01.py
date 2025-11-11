"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""


def pregunta_01():
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"

    """
    import pandas as pd


    def load_data(input_file):
        """Lea el archivo usando pandas y devuelva un DataFrame"""
        df = pd.read_csv(input_file, sep=";", index_col=0)
        return df
    

    def limpiar_columna_textual(df, column, apply_strip=True):
        """
        Limpia columnas textuales con normalización mínima:
        lower, reemplazo de guiones/guiones bajos, strip opcional.
        Sin fuzzy matching ni n-gramas.
        """
        df = df.copy()
        df[column] = df[column].str.lower().str.replace("-", " ", regex=False).str.replace("_", " ", regex=False)
        if apply_strip:
            df[column] = df[column].str.strip()
        return df


    def limpiar_columna_numerica(df, column):
        """
        Limpia columnas numéricas con conversión simple
        """
        df = df.copy()

        if column == "comuna_ciudadano":
            df[column] = df[column].astype(int)
        elif column == "monto_del_credito":
            # Eliminar símbolos de moneda, comas y espacios
            df[column] = df[column].astype(str).str.replace('$', '', regex=False)
            df[column] = df[column].str.replace(',', '', regex=False)
            df[column] = df[column].str.replace(' ', '', regex=False)
            df[column] = pd.to_numeric(df[column]).astype(int)

        return df
    

    def limpiar_columna_fecha(df, column):
        """
        Reformatea fechas de forma mínima: solo reordena YYYY/MM/DD si el primer
        segmento tiene 4 dígitos. Deja el resto intacto como string.
        """
        df = df.copy()
        df[column] = df[column].apply(
            lambda f: f"{f.split('/')[2]}/{f.split('/')[1]}/{f.split('/')[0]}" 
            if len(f.split('/')[0]) == 4 else f
        )
        return df


    def save_data(df, output_file):
        """Guarda el DataFrame en un archivo"""
        from pathlib import Path
        df = df.copy()
        filepath = Path(output_file)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(output_file, sep=";", index=False)


    input_file = "files/input/solicitudes_de_credito.csv"
    output_file = "files/output/solicitudes_de_credito.csv"

    raw = load_data(input_file)
    df = raw.copy()
    
    # Eliminar NaN primero
    df = df.dropna()
    
    # Limpiar columnas de texto
    columnas = df.columns.to_list()
    for columna in columnas:
        if df[columna].dtype == "object" and columna != "barrio":
            df = limpiar_columna_textual(df, columna, apply_strip=True)
    
    # Limpieza numérica
    df = limpiar_columna_numerica(df, "comuna_ciudadano")
    df = limpiar_columna_numerica(df, "monto_del_credito")
    
    # Limpieza columna Barrio
    df = limpiar_columna_textual(df, "barrio", apply_strip=False)
    
    # Fecha
    df = limpiar_columna_fecha(df, "fecha_de_beneficio")
    
    # Eliminar duplicados al final
    df = df.drop_duplicates()

    
    save_data(df, output_file)