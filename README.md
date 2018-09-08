# HappyParking
Parkers aim to create a real-time web app for end-users, helping drivers to find a vacant spot efficiently.
It allows users to narrow down the range by distance and intended duration.
In addition, the web app also provides a visualization regarding the analysis of the parking area occupancy rate based on historical data of the past 4 years.
At the government end, the real-time parking solution can help reduce the air pollution or traffic problem that caused by circling vehicles for vacant spaces. On the other hand, the visualization shows the land utilization in a more straightforward way, which supports the government to monitor and make a decision to improve quality of life.

## Challenges
#### National
* Bounty: Mix and Mashup\
  https://2018.hackerspace.govhack.org/challenges/8

#### Victoria
* Innovation space - A City Planning for Growth\
  https://2018.hackerspace.govhack.org/challenges/80
  
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

## Dependencies
* TerriaJS\
  https://github.com/TerriaJS/terriajs
  
* Flask\
  http://flask.pocoo.org/ 
 
* GeoJSON\
  https://github.com/frewsxcv/python-geojson
  
## TerriaMap prerequisites and scripts

These tools are required for build and run TerriaMap:

* Node.js
* GDAL (try `brew install gdal`)

Scripts (.sh files) under the `scripts` folder are snippets for command line commands.

* `terriamap-install.sh`: Install the dependencies of the _TerriaMap_. (node_modules)
* `terriamap-build.sh`: Build the _TerriaMap_.
* `terriamap-start.sh`: Start the _TerriaMap_ at `localhost:3001`. 4 processes will be started in the background.
* `terriamap-stop.sh`: Stop the _TerriaMap_, Terminate the 4 processes.

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
