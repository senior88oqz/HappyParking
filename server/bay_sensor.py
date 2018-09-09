import pandas as pd
from sodapy import Socrata
import json

# On-street Parking Bays
park_bays = "wuf8-susg"
# On-street Parking Bay Sensors
park_bay_sensor = "dtpv-d4pf"
# On-street Car Park Bay Restrictions
park_bay_restrictions = "rzb8-bz3y"


def getData(dataName):
    client = Socrata("data.melbourne.vic.gov.au", None)
    results = client.get(dataName, limit=100000)
    return results


# convert dataframe to geoJson
def data2geojson(df):
    geoJson = {'type': 'FeatureCollection', 'features': []}
    with open('./static/park_config.json') as json_doc:
        style = json.load(json_doc)

    for i in range(len(df)):
        visual = style[df['status'][i]]
        temp = {"bay_id": df['bay_id'][i],
                "st_marker_id": df["st_marker_id"][i],
                "status": df['status'][i],
                "descriptions": df["descriptions"][i]}
        properties = dict(temp, **visual)
        feature = {'type': 'Feature',
                   'properties': properties,
                   'geometry': df['the_geom'][i]
                   }
        geoJson['features'].append(feature)
    # write data to json files
    with open('bay_sensor.geojson','w', encoding='utf-8') as f:
        json.dump(geoJson,f)
        output = json.dumps(geoJson)
    return output


# convert all park bays
"""

def data2geojson1(df):
    geoJson = {'type': 'FeatureCollection', 'features': []}
    with open('park_config.json') as json_doc:
        style = json.load(json_doc)
    for i in range(len(df)):
        visual = style['Unavailable']
        temp = {"bay_id": df['bay_id'][i],
                "descriptions": df["descriptions"][i]}
        properties = dict(temp, **visual)
        feature = {'type': 'Feature',
                   'properties': properties,
                   'geometry': df['the_geom'][i]
                   }
        geoJson['features'].append(feature)
    # write data to json files
    with open('all_park.geojson', 'w', encoding='utf-8') as f:
        output = json.dump(geoJson, f)
        return output

"""


def getRealTimeData(bays_data, latitude=None, longtitude=None, is_disabled=None):
    res_json = open('./static/restriction.json', 'r')
    restrition = json.load(res_json)

    # bays_data = getData(park_bays)
    bay_sensor_data = getData(park_bay_sensor)

    results_bays = pd.DataFrame.from_records(bays_data)
    results_bays_sensor = pd.DataFrame.from_records(bay_sensor_data)

    # remove non-useful columns
    thin_bays_sensor = results_bays_sensor.drop(["location"], axis=1)

    # add new column for geometry and descriptions
    thin_bays_sensor["the_geom"] = ""
    thin_bays_sensor["descriptions"] = ""

    # Hashmap for parking bays
    bays = dict()
    for i in range(len(results_bays)):
        bays[results_bays["bay_id"][i]] = results_bays["the_geom"][i]

    # add geom info to sensor database
    for j in range(len(thin_bays_sensor)):
        bay_id = thin_bays_sensor["bay_id"][j]
        if bay_id in bays.keys():
            thin_bays_sensor["the_geom"][j] = bays[bay_id]
        if bay_id in restrition.keys():
            thin_bays_sensor["descriptions"][j] = restrition[bay_id]

    outputJson = data2geojson(thin_bays_sensor)
    return outputJson
