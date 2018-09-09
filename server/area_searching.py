import geopandas as gpd
import pandas as pd
import geojson
import json
from sodapy import Socrata
from shapely.geometry import Point
from shapely.geometry import LinearRing
from math import radians, cos, sin, asin, sqrt

# On-street Parking Bays
park_bays = "wuf8-susg"
# On-street Parking Bay Sensors
park_bay_sensor = "dtpv-d4pf"
# On-street Car Park Bay Restrictions
park_bay_restrictions = "rzb8-bz3y"
bays_data = None


# @params: lon: longitude
# @params: lat: latitude
# @params: parks: geojson

def availableParks():
    inputGeojson = 'bay_sensor.geojson'
    circle = Point(144.968492, -37.797397)
    # json.loads(data)
    # parks_data = gpd.GeoDataFrame(json.loads(inputGeojson))
    # parks_data = parks_data.set_geometry('geometry')
    parks_data = gpd.read_file(inputGeojson)
    avi_parks = []
    for geom in parks_data['geometry']:
        if (geom.geom_type != 'Polygon'):
            polygons = list(geom)
            for geom_seg in polygons:
                p = findNearestPoint(geom_seg, circle)
                dis = haversine(circle.x, circle.y, p[0], p[1])

        else:
            findNearestPoint(geom, circle)
            dis = haversine(circle.x, circle.y, p[0], p[1])
        if (dis < 500):
            avi_parks.append(geom)
    if (len(avi_parks) != 0):
        outputgeojson = parks_data.loc[parks_data['geometry'].isin(avi_parks)]
        outputgeojson = outputgeojson.loc[outputgeojson['status'] == 'Unoccupied']
        outputgeojson = data2geojson(outputgeojson)
        return outputgeojson
    else:
        return 0


def findNearestPoint(geom, circle):
    pol_ext = LinearRing(geom.exterior.coords)
    d = pol_ext.project(circle)
    p = pol_ext.interpolate(d)
    closest_point_coords = list(p.coords)[0]
    return closest_point_coords


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    # Radius of earth in kilometers is 6371
    m = 6371 * c * 1000
    return m


def data2geojson(df):
    geoJson = {'type': 'FeatureCollection', 'features': []}
    with open('park_config.json') as json_doc:
       style = json.load(json_doc)
    for i in range(1, len(df)):

        visual = style[df['status'][i]]
        temp = {"bay_id": df['bay_id'].values[i],
                "st_marker_id": df["st_marker_id"].values[i],
                "status": df['status'].values[i]}
        properties = dict((temp), **visual)
        feature = {'type': 'Feature',
                   'properties': properties,
                   'geometry': df['geometry'].values[i]
                   }
        geoJson['features'].append(feature)
    with open('bay_sensor.geojson', 'w', encoding='utf-8') as f:
        output = geojson.dumps(geoJson)
    return output