from flask_restful import Resource, reqparse

from models.sql_db import UserTable


class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        user_table_conns = UserTable()
        result = user_table_conns.query_by_username(username=username)
        row = result.fetchone()
        if row:
            user_details = cls(*row)
        else:
            user_details = None
        user_table_conns.close_connection()
        return user_details

    @classmethod
    def find_by_userid(cls, userid):
        user_table_conns = UserTable()
        result = user_table_conns.query_by_userid(userid=userid)
        row = result.fetchone()
        if row:
            user_details = cls(*row)
        else:
            user_details = None
        user_table_conns.close_connection()
        return user_details


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username", 
                        type=str, 
                        required=True, 
                        help="This field shouldn't be left blank")
    parser.add_argument("password", 
                        type=str, 
                        required=True, 
                        help="This field shouldn't be left blank")

    def post(self):
        data = self.parser.parse_args()
        is_user_already_exist = User.find_by_username(data['username'])
        if is_user_already_exist:
            return {"message": "Username '{u_name}' already exists".format(u_name=data['username'])}, 400

        # Add new user into database
        user_table_conns = UserTable()
        user_table_conns.insert_users_details(username=data['username'], password=data['password'])
        user_table_conns.close_connection()
        return {"message": "User '{u_name}' created successfully".format(u_name=data['username'])}, 201
