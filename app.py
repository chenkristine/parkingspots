from flask import Flask
from flask_restful import Api, Resource, reqparse
import requests

app = Flask(__name__)
api = Api(app)

spots = [
	{
		"id": 1,
		"lat": 37.5,
		"lon": -122.4
	},
	{
		"id": 2,
		"lat": 37.6,
		"lon": -122.2
	},
	{
		"id": 3,
		"lat": 36.9,
		"lon": -121.1
	},
	{
		"id": 4,
		"lat": 36.6,
		"lon": -122.6
	},
	{
		"id": 5,
		"lat": 37.7,
		"lon": -122.4
	},
	{
		"id": 6,
		"lat": 37.3,
		"lon": -122.2
	},
	{
		"id": 7,
		"lat": 35.3,
		"lon": -120.5
	},
	{
		"id": 8,
		"lat": 33.9,
		"lon": -121.7
	},
	{
		"id": 9,
		"lat": 37.8,
		"lon": -121.4
	},
	{
		"id": 10,
		"lat": 38.1,
		"lon":  -122.3
	}
]

available = []

class User(Resource):
	def get(self, id):
		for spot in available:
			if (id == spot["id"]):
				available.remove(spot)

	def post(self, id, lat, lon):
		parser = reqparse.RequestParser()
		parser.add_argument("lat_arg")
		parser.add_argument("lon_arg")
		parser.add_argument("radius")
		args = parser.parse_args()
		
		lat_arg = args["lat"]
		lon_arg = args["lon"]
		r = args["radius"]

		for spot in spots:
			dist = sqrt(((spot["lat"] - lat_arg)**2 + (spot["lon"] - lon_arg)**2))
			if (dist <= r):
				available.append(spot)

		return available, 200

api.add_resource(User,"/user/<string:name>")
app.run(debug=True)

"""url = "/api/v1/parkingspots/reserve/{id}"
PARAMS = {'id': 1}
r = requests.get(url = url, params = PARAMS)
data = r.json()

endpoint = "/api/v1/parkingspots/available"
postdata = {"lat": 35,
	    "lon": 120,
	    "radius": 1}
headers = {'content-type': 'application/json'}
response = requests.post(url = endpoint, data=json.dumps(postdata), headers=headers)"""
