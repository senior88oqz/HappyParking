# HappyParking
Parkers aim to create a real-time web app for end-users, helping drivers to find a vacant spot efficiently.
It allows users to narrow down the range by distance and intended duration.

In addition, the web app also provides a visualization regarding the analysis of the parking area occupancy rate based on historical data of the past 4 years.
At the government end, the real-time parking solution can help reduce the air pollution or traffic problem that caused by circling vehicles for vacant spaces. On the other hand, the visualization shows the land utilization in a more straightforward way, which supports the government to monitor and make a decision to improve quality of life.

## Live demo
[Live demo](http://13.236.60.79/) on AWS (free tier instance).

## The Problem
Problem explanation...

Solution...

## The challenges
#### National
1.  [Bounty: Mix and Mashup](https://2018.hackerspace.govhack.org/challenges/8)\
    Some explanation...
2.  [More than apps and maps: help government decide with data](https://2018.hackerspace.govhack.org/challenges/7)\
    Some explanation...

#### Victoria
1.  [Innovation space - A City Planning for Growth](https://2018.hackerspace.govhack.org/challenges/80)\
    Some explanation...
2.  [Play Melbourne - A Creative City](https://2018.hackerspace.govhack.org/challenges/81)\
    Some explanation...
  
## Datasets
1. [On-street Parking Bay Sensors](https://data.melbourne.vic.gov.au/Transport-Movement/On-street-Parking-Bay-Sensors/vh2v-4nfs)
2. [On-street Parking Bays](https://data.melbourne.vic.gov.au/Transport-Movement/On-street-Parking-Bays/crvt-b4kt)
3. [On-street Car Park Bay Restrictions](https://data.melbourne.vic.gov.au/Transport-Movement/On-street-Car-Park-Bay-Restrictions/ntht-5rk7)
4. [On-street Car Parking Sensor Data - 2017](https://data.melbourne.vic.gov.au/Transport-Movement/On-street-Car-Parking-Sensor-Data-2017/u9sa-j86i)
5. [On-street Car Parking Sensor Data - 2016](https://data.melbourne.vic.gov.au/Transport-Movement/On-street-Car-Parking-Sensor-Data-2016/dj7e-rdx9)
6. [On-street Car Parking Sensor Data - 2015](https://data.melbourne.vic.gov.au/Transport-Movement/On-street-Car-Parking-Sensor-Data-2015/apua-t2tb)
7. [On-street Car Parking Sensor Data - 2014](https://data.melbourne.vic.gov.au/Transport-Movement/On-street-Car-Parking-Sensor-Data-2014/t6hb-9uf2)
8. [Off-street car parks with capacity and type](https://data.melbourne.vic.gov.au/Property-Planning/Off-street-car-parks-with-capacity-and-type/krh5-hhjn)

## Dependencies
* [TerriaJS](https://github.com/TerriaJS/terriajs)
* [Flask](http://flask.pocoo.org)
* [Flase-CORS](https://flask-cors.readthedocs.io/en/latest)
* [GeoPandas](http://geopandas.org)
* [Python-GeoJSON](https://github.com/frewsxcv/python-geojson)
  
## TerriaMap prerequisites and scripts
These tools are required for build and run _TerriaMap_:
* Node.js
* GDAL (try `brew install gdal`)

Therea re some useful _TerriaMap_ commands. Use these under the `terriamap` folder.
* `npm install`: Install the dependencies of the _TerriaMap_. (node_modules)
* `npm run gulp`: Build the _TerriaMap_.
* `npm start`: Start the _TerriaMap_ at `localhost:3001`. 4 processes will be started in the background.
* `npm stop`: Stop the _TerriaMap_, Terminate the 4 processes.

## API documents
#### Real-time park pool visualization
`GET` `/api/realtime-parkinfo`

##### Request parameters
| Parameter | Type | Required | Default | Description |
|:---------:|:----:|:--------:|:-------:|:-----------:|
|is_disabled|int|no|0|1 for disabled|
|latitude|float|no|null|Target address|
|longitude|float|no|null|Target address|

##### Response format: `GeoSJON`
| Property | Type | Description |
|:---------:|:----:|:----------:|
|bay_id|str||
|TODO...||

##### Response example
```
...
"properties": {
    "bay_id": "20",
    "occupied": true,
    "only_for_disabled": false,
    "restriction": {
        "p_tag": "2p",
        "duration": 120,
        "is_charged": true,
        "timestart": "8:30",
        "timeend": "17:30"
    }
}
...
```

##### Related datasets:
* On-street Parking Bay Sensors
* On-street Parking Bays
* On-street Car Park Bay Restrictions
