import pandas as pd
import numpy as np
import lightkurve as lk
from astroquery.ipac.nexsci.nasa_exoplanet_archive import NasaExoplanetArchive
from astroquery.mast import Observations
from sklearn.impute import SimpleImputer

from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, Dict, List, Optional

# ==============================================================================
# --- Herramienta 1: Listar estrellas con planetas confirmados (Resiliente) ---
# ==============================================================================
class ListHostsInput(BaseModel):
    max_results: int = Field(default=10, description="El número máximo de identificadores de estrellas a devolver.")

class ListConfirmedExoplanetHostsTool(BaseTool):
    name: str = "list_confirmed_exoplanet_hosts"
    description: str = (
        "Útil para cuando necesitas obtener una lista de identificadores (TIC IDs) de estrellas "
        "que se sabe que tienen exoplanetas confirmados. Devuelve una lista de strings."
    )
    args_schema: Type[BaseModel] = ListHostsInput

    def _run(self, max_results: int = 10) -> Dict:
        try:
            print(f"--- TOOL: Buscando hasta {max_results} estrellas con planetas confirmados... ---")
            planets_table = NasaExoplanetArchive.get_confirmed_planet_table(all_columns=True)
            planets_df = planets_table.to_pandas()
            positive_tic_ids = planets_df['tic_id'].dropna().unique().tolist()

            results = positive_tic_ids[:max_results]
            summary = f"Se encontraron {len(positive_tic_ids)} estrellas en total. Devolviendo las primeras {len(results)}."
            print(summary)
            return {"star_identifiers": results, "summary": summary}
        except Exception as e:
            # Estrategia de Resiliencia: Capturar cualquier excepción y devolver un error estructurado.
            error_message = f"La herramienta falló con el error: {e}. Esto podría deberse a un problema de la API de la NASA o a un error interno."
            print(f"  -> ERROR en {self.name}: {error_message}")
            return {"error": error_message}

# ==============================================================================
# --- Herramienta 2: Obtener la curva de luz (Resiliente) ---
# ==============================================================================
class GetLightCurveInput(BaseModel):
    star_id: str = Field(description="El identificador de la estrella. Debe incluir el prefijo, ej: 'TIC 307210830', 'KIC 757076'.")
    mission: Optional[str] = Field(default="TESS", description="La misión de la cual descargar los datos, como 'TESS', 'Kepler' o 'K2'.")

class GetStarLightCurveTool(BaseTool):
    name: str = "get_star_light_curve_to_file"
    description: str = (
        "Descarga los datos de la curva de luz para una estrella específica. "
        "IMPORTANTE: No devuelve los datos directamente. En su lugar, guarda los datos en un archivo CSV "
        "y devuelve un diccionario con la ruta a ese archivo ('file_path'). "
        "Luego debes usar la herramienta de python para leer y analizar ese archivo."
    )
    args_schema: Type[BaseModel] = GetLightCurveInput

    def _run(self, star_id: str, mission: str = "TESS") -> Dict:
        try:
            print(f"--- TOOL: Buscando y guardando curva de luz para '{star_id}' en misión '{mission}'... ---")
            search = lk.search_lightcurve(star_id, mission=mission, author="SPOC")

            if len(search) == 0:
                search = lk.search_lightcurve(star_id, mission=mission)
                if len(search) == 0:
                    raise ValueError("No se encontraron curvas de luz para este objetivo.")

            lc = search.download()
            lc_flat = lc.normalize().flatten(window_length=401)
            df = pd.DataFrame({'time': lc_flat.time.value, 'flux': lc_flat.flux.value})

            safe_star_id = star_id.replace(" ", "_").replace("-", "_")
            file_path = f"light_curve_{safe_star_id}_{mission}.csv"
            df.to_csv(file_path, index=False)

            summary = f"Éxito: Se guardaron {len(df)} puntos de datos en el archivo '{file_path}'."
            print(f"  -> {summary}")

            return {"status": "success", "summary": summary, "file_path": file_path}
        except Exception as e:
            error_message = f"Falló la descarga o procesamiento para '{star_id}': {e}"
            print(f"  -> ERROR en {self.name}: {error_message}")
            return {"status": "error", "message": error_message}

# ==============================================================================
# --- Herramienta 3: Listar estrellas por misión (Resiliente y Rápida) ---
# ==============================================================================
class ListStarsByMissionInput(BaseModel):
    mission: str = Field(description="La misión de la cual obtener los nombres de las estrellas. Opciones: 'Kepler', 'K2', 'TESS'.")
    limit: int = Field(default=10, description="El número máximo de estrellas a devolver.")

class ListStarsByMissionTool(BaseTool):
    name: str = "list_stars_by_mission"
    description: str = (
        "Devuelve una lista de identificadores de estrellas que fueron observadas por una misión específica (Kepler, K2, TESS). "
        "Es útil cuando no buscas planetas confirmados, sino cualquier estrella de un catálogo de misión, ideal para aprendizaje auto-supervisado."
    )
    args_schema: Type[BaseModel] = ListStarsByMissionInput

    def _run(self, mission: str, limit: int = 10) -> Dict:
        try:
            lista_de_misiones = ["Kepler", "K2", "TESS"]
            if mission not in lista_de_misiones:
                return {"error": f"Misión inválida. Usa una de {lista_de_misiones}"}
            
            print(f"--- TOOL: Buscando {limit} estrellas de la misión {mission} con una consulta optimizada... ---")

            # SOLUCIÓN DEFINITIVA: Añadir filtros para hacer la consulta extremadamente rápida.
            # Esto evita que la consulta se quede colgada o tarde demasiado.
            query_params = {
                "obs_collection": mission,
                "dataproduct_type": "timeseries",
                "intentType": "science",
                # CORRECCIÓN: Cambiar 'max_records' por 'pagesize' o un parámetro similar
                "pagesize": limit 
            }
            
            # Añadir filtros específicos de la misión para acotar la búsqueda
            if mission == "TESS":
                query_params["sequence_number"] = 1 # Busca solo en el Sector 1 de TESS.
            elif mission == "Kepler":
                query_params["quarter"] = 1 # Busca solo en el primer trimestre de Kepler.

            obs_table = Observations.query_criteria(**query_params)

            if len(obs_table) == 0:
                 return {"error": f"La consulta optimizada no devolvió observaciones para la misión {mission}."}

            df = obs_table.to_pandas()
            estrellas = df["target_name"].unique().tolist()[:limit]
            
            if not estrellas:
                return {"error": "La consulta devolvió datos, pero no se pudieron extraer identificadores de estrellas."}

            summary = f"Se encontraron y devolvieron {len(estrellas)} identificadores de estrellas únicos para la misión {mission}."
            print(summary)
            return {"star_identifiers": estrellas, "summary": summary}
        except Exception as e:
            # El error 'TIMEOUT' era un AttributeError. Esta cláusula lo capturará.
            error_message = f"La consulta a MAST falló con el error: {e}. Esto puede ser un bug en la librería o un problema con el servicio externo."
            print(f"  -> ERROR en {self.name}: {error_message}")
            return {"error": error_message}

# ==============================================================================
# --- Herramienta 4: Obtener dataset para Machine Learning (Resiliente) ---
# ==============================================================================
class GetLabeledDatasetInput(BaseModel):
    mission: str = Field(description="La misión para la cual construir el dataset. Opciones: 'Kepler', 'K2', 'TESS'.")

class GetLabeledExoplanetDatasetTool(BaseTool):
    name: str = "get_labeled_exoplanet_dataset"
    description: str = (
        "Descarga datos tabulares de exoplanetas candidatos de una misión (Kepler, K2, TESS) desde el NASA Exoplanet Archive. "
        "Procesa los datos, los separa en características (features) y etiquetas (labels) listos para Machine Learning, "
        "los guarda en archivos CSV y devuelve las rutas a dichos archivos."
    )
    args_schema: Type[BaseModel] = GetLabeledDatasetInput

    def _cargar_datos_nasa(self, nombre_tabla: str) -> pd.DataFrame:
        base_url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+*+from+"
        formatos = "&format=csv"
        url = base_url + nombre_tabla + formatos
        df = pd.read_csv(url, low_memory=False)
        print(f"  -> Tabla '{nombre_tabla}' cargada con {df.shape[0]} filas y {df.shape[1]} columnas.")
        return df

    def _construir_dataset_para_ml(self, df, label_col):
        if label_col not in df.columns:
            raise ValueError(f"La columna de etiquetas '{label_col}' no está en el DataFrame.")
        y_raw = df[label_col].astype(str).str.lower()
        y = y_raw.map(lambda s: "confirmed" if "conf" in s else ("candidate" if "cand" in s else ("false_positive" if "fp" in s or "false" in s else "unknown")))
        mask = y != "unknown"
        df, y = df[mask].copy(), y[mask]
        feature_cols = [c for c in df.columns if any(k in c.lower() for k in ["period", "dur", "depth", "rad", "mass", "a", "st_"])]
        X = df[feature_cols].apply(pd.to_numeric, errors="coerce")
        X = X.loc[:, X.isna().mean() < 0.5]
        imputer = SimpleImputer(strategy="median")
        return pd.DataFrame(imputer.fit_transform(X), columns=X.columns, index=X.index), y

    def _run(self, mission: str) -> Dict:
        try:
            print(f"--- TOOL: Creando dataset de ML para la misión {mission}... ---")
            tablas = {"Kepler": ("cumulative", "koi_disposition"), "TESS": ("toi", "tfopwg_disp"), "K2": ("k2pandc", "disposition")}
            if mission not in tablas:
                return {"error": f"Misión inválida. Usa una de {list(tablas.keys())}"}
            
            tabla, etiqueta = tablas[mission]
            df = self._cargar_datos_nasa(tabla)
            X, y = self._construir_dataset_para_ml(df, label_col=etiqueta)
            
            features_path = f"{mission}_ml_features.csv"
            labels_path = f"{mission}_ml_labels.csv"
            X.to_csv(features_path)
            y.to_csv(labels_path)
            
            summary = f"Dataset para {mission} creado. Características: {X.shape[0]} filas, {X.shape[1]} columnas. Etiquetas: {len(y)}."
            print(f"  -> {summary}")
            return {"status": "success", "summary": summary, "features_file_path": features_path, "labels_file_path": labels_path}
        except Exception as e:
            error_message = f"No se pudo construir el dataset para {mission}: {e}"
            print(f"  -> ERROR en {self.name}: {error_message}")
            return {"error": error_message}