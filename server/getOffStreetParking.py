#!/usr/bin/env python

import pandas as pd
from sodapy import Socrata
import json
import urllib.request
import pygeoj
urllib.request.urlretrieve ("https://data.melbourne.vic.gov.au/resource/dtpv-d4pf.geojson", "parkSensor.json")



def getData(code, limit):
    client = Socrata("data.melbourne.vic.gov.au", None)
    results = client.get(code, limit=limit)
    results_df = pd.DataFrame.from_records(results)
    return results_df

if __name__ == '__main__':
    urllib.request.urlretrieve("https://data.melbourne.vic.gov.au/resource/9xmh-yeh2.geojson", "offStreet.geojson")
    # offStreetData = pygeoj.load("offStreet.geojson")
    # offStreetData = getData(code="9xmh-yeh2", limit=100000)
    # offStreetData = offStreetData.drop(["clue_small_area", "property_id", "x_coordinate","x_coordinate_2","y_coordinate"], axis=1)

    # with open("off-street.geojson", "w") as write_file:
    #     json.dump(offStreetData, write_file)
    with open("offStreet.geojson") as file:
        offStreetData = json.load(file)

    keys_filter = ['x_coordinate_state','base_property_id','block_id','y_coordinate','x_coordinate_city',
                   'property_id','x_coordinate_zip','x_coordinate_address','x_coordinate_2']
    numberOfEntry = len(offStreetData['features'])
    for i in range(numberOfEntry):
        for key in keys_filter:
            try:
                del offStreetData['features'][i]['properties'][key]
            except KeyError:
                pass
    with open("offStreet.geojson",'w') as file:
        offStreetData = json.dump(offStreetData, file)