from model import UsersModel
from flask import jsonify
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token

class UsersService:
    def create(self, **kwargs):
        user = UsersModel.find_user_by_email(kwargs['email'])
        if user:
            return jsonify({"message": 'E-mail em uso'})
        
        new_user = UsersModel(**kwargs)
        new_user.save()
        return new_user.as_dict()
    

    def login(self, **kwargs):
        user = UsersModel.find_user_by_email(kwargs['email'])
        if user and pbkdf2_sha256.verify(kwargs['password'], user.password):
            token = create_access_token(identity=user.id)
            return {'access_token': token}
        return jsonify({'message': 'Autenticação inválida'})


              


