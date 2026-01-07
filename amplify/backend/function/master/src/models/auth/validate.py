from bson import ObjectId
from db.user import get_user_collection
from models.interfaces import UserAuthInput as Input, UserType
from flask_jwt_extended import jwt_required, get_jwt_identity


class Validator:
    def __init__(self, input: Input) -> None:
        self.input = input
        self.user_collection = get_user_collection()

    def validate_admin_access(self, user_id: str) -> bool:
        admin = self.user_collection.find_one({'_id': ObjectId(user_id)})
        if not admin:
            return False
        if self.input.user_type == UserType.emp.value:
            return admin.get('user_type') in [UserType.admin.value, UserType.super.value]
        if self.input.user_type == UserType.admin.value:
            return admin.get('user_type') == UserType.super.value
        if self.input.user_type == UserType.super.value:
            return admin.get('user_type') == UserType.super.value
        return True

    @jwt_required()
    def check_privileges(self) -> bool:
        user_id = get_jwt_identity()
        return self.validate_admin_access(user_id)

    def validate_input(self) -> tuple[bool, str]:
        if self.input.action not in ['sign_up', 'sign_in', 'refresh']:
            return False, "Invalid action specified."

        if not (self.input.email or self.input.phoneNumber):
            return False, "Either email or phone number must be provided."

        if self.input.user_type and self.input.user_type not in UserType.__members__:
            return False, "Invalid user type provided."

        if self.input.action in ['sign_up', 'sign_in'] and not self.input.password:
            return False, "Password must be provided for sign up or sign in."

        if self.input.action == 'sign_up' and not self.input.name:
            return False, "Name must be provided for sign up."

        if self.input.user_type != UserType.user.value:
            if self.input.action == 'sign_up' and not self.check_privileges():
                return False, "Insufficient privileges to create this user type."

        return True, ""
