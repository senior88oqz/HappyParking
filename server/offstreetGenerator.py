import pandas as pd
from sodapy import Socrata
import json

dataName = "9xmh-yeh2"
client = Socrata("data.melbourne.vic.gov.au", None)
results = client.get(dataName)

#list


features = []
for data in results:
	try:
		temp = {
		"type" : "Feature",
		"properties":
	        {
	        	    "base_property_id": data["base_property_id"],
				    "block_id": data["block_id"],
				    "census_year": data["census_year"],
				    "clue_small_area": data["clue_small_area"],
				    "parking_spaces": data["parking_spaces"],
				    "parking_type": data["parking_type"],
				    "property_id": data["property_id"],
				    "street_name": data["street_name"]
	        },
	    "geometry":
	      	{
	            "type": "Point",
	            "coordinates": data["x_coordinate"]["coordinates"]
	        }
		}
	except Exception as e:

	features.append(temp)

georeuslt = {
	"type": "FeatureCollection",
	"features": features
}



with open('./static/offstreet_parking.geojson','w', encoding='utf-8') as f:
	json.dump(georeuslt, f)
