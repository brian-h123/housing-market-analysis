import json

from pathlib import Path

def load_geojson():
    geojson_path = Path(__file__).resolve().parents[2] / "data" / "twTown1982.geo.json"

    if not geojson_path.exists():
        raise FileNotFoundError(f"GeoJson not found at {geojson_path}")

    with open(geojson_path, encoding='utf-8') as f:
        return json.load(f)