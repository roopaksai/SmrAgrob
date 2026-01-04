import json
import dataclasses
from flask import request
from flask_restful import Resource
from models.helloworld.main import HelloWorld
from models.interfaces import HelloWorldInput


class HelloWorldService(Resource):
    def post(self):
        data = json.loads(request.get_data())
        input_data = HelloWorldInput(**data)
        output = HelloWorld(input_data).process()
        output = dataclasses.asdict(output)
        return output
