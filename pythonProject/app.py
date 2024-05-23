from flask import Flask, render_template
import geopandas as gpd
from neo4j import GraphDatabase
from shapely.geometry import Point

app = Flask(__name__)

@app.route('/')
def index():
    # Neo4j sorgusu
    Host_url = "bolt://localhost:7687"
    kullaniciAd = "neo4j"
    sifre = "neo4j.muhammed"
    query = """
    MATCH (city:City)
    RETURN city.name AS name, city.latitude AS latitude, city.longitude AS longitude,
           city.okurYazarOrani AS literacyRate, city.gocOrani AS migrationRate,
           city.yasliOrani AS elderlyRate, city.evlilikOrani AS marriageRate,
           city.gencOrani AS youthRate
    """
    driver = GraphDatabase.driver(Host_url, auth=(kullaniciAd, sifre))
    with driver.session() as session:
        result = session.run(query)
        city_data = [{
            'name': record['name'],
            'latitude': record['latitude'],
            'longitude': record['longitude'],
            'literacyRate': record['literacyRate'],
            'migrationRate': record['migrationRate'],
            'elderlyRate': record['elderlyRate'],
            'marriageRate': record['marriageRate'],
            'youthRate': record['youthRate']
        } for record in result]

    # Şehir verilerini geometriye dönüştürdüm
    geometry = [Point(float(record['longitude']), float(record['latitude'])) for record in city_data]
    city_gdf = gpd.GeoDataFrame(city_data, geometry=geometry, columns=['name', 'latitude', 'longitude', 'literacyRate', 'migrationRate', 'elderlyRate', 'marriageRate', 'youthRate'])

    # GeoJSON olarak dönüştürdüm
    city_geojson = city_gdf.to_json()


    print(city_geojson)

    return render_template('index.html', city_geojson=city_geojson)

if __name__ == '__main__':
    app.run(debug=True)
