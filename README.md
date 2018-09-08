# HappyParking
Happy parking!

## Challenges
#### National
* Bounty: Mix and Mashup

#### Victoria
* Innovation space - A City Planning for Growth
  
## Architecture

### Datasets
* On-street Parking Bay Sensors\
  https://data.melbourne.vic.gov.au/Transport-Movement/On-street-Parking-Bay-Sensors/vh2v-4nfs

* On-street Parking Bays\
  https://data.melbourne.vic.gov.au/Transport-Movement/On-street-Parking-Bays/crvt-b4kt

* On-street Car Park Bay Restrictions\
  https://data.melbourne.vic.gov.au/Transport-Movement/On-street-Car-Park-Bay-Restrictions/ntht-5rk7

### Frontend
* Terria Map

### Backend
* Flask


### APIs
Real-time park pool visualization

* ``/api/realtime-parkinfo``\
  Args: 
    `is_disabled` int (default: 0)\
    1: is disabled; 0: not disabled
    
    `latitude` float (optional default: null)\
    `longitude` float (optional default: null)\
    The target coordinates
    
  Return: GeoJSON
  ``` json
  {
    "bay_id": <str>,
    "status": <bool>,
    "only_for_disabled": <bool>,
    "properties": {
        "p_tag": <str>,
        "duration": <int>
        "is_charged": <bool>,
        "timestart": <str>,
        "timeend": <str>
    }
  }
  ```
  Related datasets:
  * On street parking bays
  
* ``/api/???``


## Dependencies
* TerriaJS\
  https://github.com/TerriaJS/terriajs
  
* Flask\
  http://flask.pocoo.org/ 
 
* GeoJSON\
  https://github.com/frewsxcv/python-geojson
