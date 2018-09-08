import pandas as pd
from sodapy import Socrata

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


bays_data = getData(park_bays)
bay_sensor_data = getData(park_bay_sensor)
bay_restrictions_data = getData(park_bay_restrictions)

results_bays = pd.DataFrame.from_records(bays_data)
results_bays_sensor = pd.DataFrame.from_records(bay_sensor_data)
results_bay_restrictions = pd.DataFrame.from_records(bay_restrictions_data)

# remove non-useful columns
thin_bays_sensor = results_bays_sensor.drop(["lat", "location", "lon"], axis=1)
# add new column for geometry
thin_bays_sensor["the_geom"] = ""

# Hashmap for parking bays
bays = dict()
for i in range(len(results_bays)):
    bays[results_bays["bay_id"][i]] = results_bays["the_geom"][i]

# add geom info to sensor database
for j in range(len(thin_bays_sensor)):
    bay_id = thin_bays_sensor["bay_id"][j]
    if bay_id in bays.keys():
        thin_bays_sensor["the_geom"][j] = bays[bay_id]

# print(thin_bays_sensor)
