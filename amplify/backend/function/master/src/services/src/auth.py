import json
import dataclasses
from flask import request
from models.auth.main import Auth
from flask_restful import Resource
from models.interfaces import UserAuthInput, Output


class AuthService(Resource):

    def post(self) -> dict:
        input = json.loads(request.get_data())
        input = UserAuthInput(**input)
        output = Auth(input).process()
        output = dataclasses.asdict(output)

        return output


