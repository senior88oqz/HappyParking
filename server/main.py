from flask import Flask, request
app = Flask(__name__)



@app.route("/api/realtime-parkinfo")
def realtimePark():
    if request.args.get('is_disabled'):
        print("filter data disabled parameter")
    if request.args.get('latitude') and request.args.get('longitude'):
        print("filter data location")
    return "geo-json result"


@app.errorhandler(404)
def page_not_found(e):
    return "404"

if __name__ == '__main__':
    app.run()

