from flask import Flask, request,Response
from flask_cors import CORS
from server.bay_sensor import getRealTimeData

app = Flask(__name__)

#Let all URLs of this server allow cross-domain requests
CORS(app, resources=r'/*')

@app.route("/api/realtime-parkinfo")
def realtimePark():
    json_data = getRealTimeData()
    if request.args.get('is_disabled'):
        print("filter data disabled parameter")
    if request.args.get('latitude') and request.args.get('longitude'):
        print("filter data location")

    return Response(
        response=json_data,
        mimetype="application/json",
        status=200
    )


@app.errorhandler(404)
def page_not_found(e):
    return "404"

if __name__ == '__main__':
    app.run()

