from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import geopandas as gpd
import requests, zipfile, io
import os
import json

from airflow.providers.amazon.aws.hooks.s3 import S3Hook

DATA_DIR = "/tmp/data"
SHAPEFILE_URL = "https://eric.clst.org/assets/wiki/uploads/Stuff/gz_2010_us_050_00_20m.zip"

def find_shapefile(base_dir: str) -> str:
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".shp") and not file.startswith("._"):
                return os.path.join(root, file)
    raise FileNotFoundError("No valid .shp file found in extracted folder.")

def download_shapefile():
    os.makedirs(DATA_DIR, exist_ok=True)
    r = requests.get(SHAPEFILE_URL)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall(DATA_DIR)

def convert_to_geoparquet():
    shapefile_path = find_shapefile("/tmp/data")
    gdf = gpd.read_file(shapefile_path)
    output_path = os.path.join(DATA_DIR, "us_states.parquet")
    gdf.to_parquet(output_path)

    # Write a metadata summary
    metadata = {
        "parquet_path": output_path,
        "geometry_column": gdf.geometry.name,
        "crs": str(gdf.crs),
        "num_rows": len(gdf),
    }
    with open(os.path.join(DATA_DIR, "metadata.json"), "w") as f:
        json.dump(metadata, f, indent=2)
    with open(os.path.join("metadata.json"), "w") as f:
        json.dump(metadata, f, indent=2)
    
       
    # Load the file to S3
    s3_hook = S3Hook(aws_conn_id="aws_conn")
    s3_hook.load_file(
        filename=output_path,
        key="geoparquet/us_state.parquet",
        bucket_name="geospatial-data-platform",
        replace=True
    )

with DAG(
    dag_id="shapefile_to_geoparquet",
    start_date=datetime(2024, 1, 1),
    schedule="@once",
    catchup=False,
    tags=["geospatial", "starter"],
) as dag:

    t1 = PythonOperator(
        task_id="download_shapefile",
        python_callable=download_shapefile,
    )

    t2 = PythonOperator(
        task_id="convert_to_geoparquet",
        python_callable=convert_to_geoparquet,
    )

    t1 >> t2