from flask import Flask, request, Response
from flask_cors import CORS
from bay_sensor import getRealTimeData, getData
from area_searching import availableParks

app = Flask(__name__)

# On-street Parking Bays
park_bays = "wuf8-susg"
# On-street Parking Bay Sensors
park_bay_sensor = "dtpv-d4pf"
# On-street Car Park Bay Restrictions
park_bay_restrictions = "rzb8-bz3y"

# Let all URLs of this server allow cross-domain requests
CORS(app, resources=r'/*')

# all parking areas info
bays_data = None


@app.route("/api/realtime-parkinfo")
def realtimePark():
    json_data = getRealTimeData(bays_data)
    if request.args.get('is_disabled'):
        print("filter data disabled parameter")
    if request.args.get('latitude') and request.args.get('longitude'):
        print("filter data location")

    return Response(
        response=json_data,
        mimetype="application/json",
        status=200
    )


@app.route("/api/area-search")
def area_search():
    data = getRealTimeData(bays_data)
    avail_parks = availableParks(data)
    fp = open('output.txt', 'w')
    fp.write(avail_parks)
    fp.close()
    return Response(
        response='{"aaa": 1}',
        mimetype="application/json",
        status=200
    )


@app.errorhandler(404)
def page_not_found(e):
    return "404"


def initialization():
    # get bays data
    global bays_data
    bays_data = getData(park_bays)


if __name__ == '__main__':
    initialization()
    app.run(host='0.0.0.0')
