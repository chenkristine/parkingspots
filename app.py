from flask import Flask, render_template
from flask_restful import Api, Resource, reqparse
import requests
import math

app = Flask(__name__)
api = Api(app)

@app.route('/<string:page_name>/')
def static_page(page_name):
    return render_template('%s.html' % page_name)

spots = [
	{
		"id": 1,
		"lat": 50.2,
		"lon": 100.1
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

available = spots
reserved = []

class ParkingSpot(Resource):
	def get(self, id_num):
		parser = reqparse.RequestParser()
		parser.add_argument("id_num")
		
		args = parser.parse_args()
		
		id_num = int(args["id_num"])
		for spot in reserved:
			if (int(id_num) == spot["id"]):
				return "This parking spot has already been reserved."
		for spot in available:
			if (int(id_num) == spot["id"]):
				reserved.append(spot)
				available.remove(spot)
				return available, 200
		return "There is no existing spot with that ID."

	def post(self, id_num):
		parser = reqparse.RequestParser()
		parser.add_argument("lat")
		parser.add_argument("lon")
		parser.add_argument("radius")
		args = parser.parse_args()
		
		lat_arg = float(args["lat"])
		lon_arg = float(args["lon"])
		radius = float(args["radius"])

		spots_in_radius = []
		
		for spot in spots:
			dist = math.sqrt(((spot["lat"] - lat_arg)**2 + (spot["lon"] - lon_arg)**2))
			if (dist <= radius):
				spots_in_radius.append(spot)

		return spots_in_radius, 200

routes = ['/api/v1/parkingspots/available/<string:id_num>',
		  '/api/v1/parkingspots/reserve/<string:id_num>']

api.add_resource(ParkingSpot,*routes)

if __name__ == '__main__':
	app.run(debug=True)

