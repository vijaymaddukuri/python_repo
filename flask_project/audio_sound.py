"""
Start the flask server:
python audio_sound.py

HTTP Request:

Get request:  curl http://127.0.0.1:5000/deviceid/5

response:
{
    "result": "Bing"
}

"""
from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class Speaker(Resource):
    def get(self, num):
        a = num%3
        b = num%5
        
        if not a and not b:
            return {'result': "Boom"}
        elif not a:
            return {'result': "Bing"}
        elif not b:
            return {'result': "Bang"}

        return {'result': "Meh"}

api.add_resource(Speaker, '/deviceid/<int:num>')

if __name__ == '__main__':
    app.run(debug=True)