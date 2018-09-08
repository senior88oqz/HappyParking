import geopandas as gpd
from shapely.geometry import Point
from shapely.geometry import LinearRing
from math import radians, cos, sin, asin, sqrt
from bay_sensor import data2geojson

# @params: lon: longitude
# @params: lat: latitude
# @params: parks: geojson

def availableParks(inputGeojson):
    circle = Point(144.969696,-37.809298)
    parks_data = gpd.read_file(inputGeojson)
    avi_parks = []
    for geom in parks_data['geometry']:
        if(geom.geom_type != 'Polygon'):
            polygons = list(geom)
            for geom_seg in polygons:
                p = findNearestPoint(geom_seg,circle)
                dis = haversine(circle.x,circle.y,p[0],p[1])

        else:
            findNearestPoint(geom,circle)
            dis = haversine(circle.x,circle.y,p[0],p[1])
        if (dis < 500):
            avi_parks.append(geom)
    outputgeojson = parks_data.loc[parks_data['geometry'].isin(avi_parks)]
    outputgeojson = outputgeojson.loc[outputgeojson['occupied'] == false]
    outputgeojson = data2geojson(outputgeojson)
    return outputgeojson

def findNearestPoint(geom,circle):
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
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    # Radius of earth in kilometers is 6371
    m = 6371 * c * 1000
    return m
#
# def data2geojson(gdf):
#     geoJson = {'type': 'FeatureCollection', 'features': []}
#     with open('park_config.json') as json_doc:
#         style = json.load(json_doc)
#     for i in range(len(gdf)):
#         visual = style[gdf['status'][i]]
#         res = {'p_tag': gdf['restriction']['p_tag'][i],
#                'duration': gdf['restriction']['duration'][i],
#                'is_charged': gdf['restriction']['is_charged'][i],
#                'timestart': gdf['restriction']['timestart'][i],
#                'timeend': gdf['restriction']['timeend'][i],
#         }
#         temp = {"bay_id": gdf['bay_id'][i],
#                 "occupied": gdf["occupied"][i],
#                 "only_for_disabled": gdf['only_for_disabled'][i],
#                 'restriction':res
#         }
#         properties = dict(temp, **visual)
#         feature = {'type': 'Feature',
#                'properties': properties,
#                'geometry': gdf['geometry'][i]
#                }
#         geoJson['features'].append(feature)
#     with open('bay_sensor.geojson','w', encoding='utf-8') as f:
#         output = json.dump(geoJson, f)
#         return output

    #def availableRestriction(gdf, P):
    # for restriction matching

    # test
    # aParks = availableParks(144.971755,-37.802740,'On-street Parking Bays.geojson')
    # data2geojson(aParks)