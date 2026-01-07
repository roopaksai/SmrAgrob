from models.common import Common
from passlib.hash import pbkdf2_sha256
from db.user import get_user_collection
from models.constants import OutputStatus
from models.interfaces import UserAuthInput as Input, Output, User
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required


class Compute:
    def __init__(self, input: Input) -> None:
        self.input = input
        self.query = self.build_user_query()
        self.user_collection = get_user_collection()

    def build_user_query(self) -> str:
        query = {}
        if self.input.phoneNumber:
            query['phoneNumber'] = self.input.phoneNumber
        if self.input.email:
            query['email'] = self.input.email
        return query

    def validate_user_exists(self) -> bool:
        if self.user_collection.find_one(self.query):
            return True
        return False

    def generate_tokens(self, user_id: str) -> dict:
        access_token = create_access_token(identity=user_id)
        refresh_token = create_refresh_token(identity=user_id)
        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }

    def _sign_up(self) -> Output:
        if self.validate_user_exists():
            return Output(
                output_message='User already exists.',
                output_status=OutputStatus.FAILURE
            )

        user = Common.clean_dict(self.input.__dict__, User)
        user = User(**user)
        user.password = pbkdf2_sha256.hash(self.input.password)

        user._id = self.user_collection.insert_one(
            Common.filter_none_values(user.__dict__)
        ).inserted_id

        user_data = user.__dict__
        user_data.pop('password', None)

        return Output(
            output_details={
                **self.generate_tokens(str(user._id)),
                'user': Common.jsonify(user_data)
            },
            output_message='Successfully signed up.'
        )

    def _sign_in(self) -> Output:
        user_data = self.user_collection.find_one(self.query)
        if not user_data:
            return Output(
                output_message='User not found.',
                output_status=OutputStatus.FAILURE
            )

        user = Common.clean_dict(user_data, User)
        user = User(**user)

        if not user or not pbkdf2_sha256.verify(self.input.password, user.password):
            return Output(
                output_message='Invalid credentials.',
                output_status=OutputStatus.FAILURE
            )

        user_data = user.__dict__
        user_data.pop('password', None)

        return Output(
            output_details={
                **self.generate_tokens(str(user._id)),
                'user': Common.jsonify(user_data)
            },
            output_message='Successfully signed in.'
        )

    @jwt_required(refresh=True)
    def _refresh_token(self) -> Output:
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return Output(
            output_details={'access_token': access_token},
            output_status=OutputStatus.SUCCESS,
            output_message='Successfully refreshed token'
        )

    def compute(self) -> Output:
        if self.input.action == 'sign_up':
            return self._sign_up()
        elif self.input.action == 'sign_in':
            return self._sign_in()
        elif self.input.action == 'refresh':
            return self._refresh_token()
        else:
            return Output(
                output_message='Invalid action.',
                output_status=OutputStatus.FAILURE,
            )
