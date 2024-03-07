from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.sql_db import ItemsTable

class Items(Resource):
    @jwt_required()
    def get(self):
        items_db_conns = ItemsTable()
        result = items_db_conns.get_items()
        items = list()
        for row in result:
            items.append({'name': row[0], 'price': row[1]})
        items_db_conns.close_connection()
        return {'items': items}, 200


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("name", 
                        type=str, 
                        required=True, 
                        help="name of the item is a mandatory input")
    parser.add_argument("price", 
                        type=float, 
                        required=True, 
                        help="price of the item is a mandatory input")

    def get(self, name):
        items_db_conns = ItemsTable()
        result = items_db_conns.get_item_by_name(name=name)
        row = result.fetchone()
        if row:
            item_details = {"name": row[0], "price": row[1]}
        else:
            item_details = "item '{item_name}' doesn't exist".format(item_name=name)
        items_db_conns.close_connection()
        return item_details, 200

    def post(self, name):
        data = self.parser.parse_args()
        item_map = {"name": data['name'], "price": data['price']}
        items_db_conns = ItemsTable()
        result = items_db_conns.get_item_by_name(name=item_map['name'])
        row = result.fetchone()
        if row:
            create_item_details = {"error_message": "Item with name '{n}' already exists.".format(n=name)}
        else:
            items_db_conns.create_item_by_name(item_map=item_map)
            create_item_details = {"message": "Successfully created the new item with name '{n}'\n{i}".format(n=name, i=item_map)}
        items_db_conns.close_connection()
        return create_item_details, 201

    def put(self, name):
        data = self.parser.parse_args()
        item_map = {"name": data['name'], "price": data['price']}
        items_db_conns = ItemsTable()
        result = items_db_conns.get_item_by_name(name=item_map['name'])
        row = result.fetchone()
        if row:
            items_db_conns.update_item_price_by_name(item_map=item_map)
            create_item_details = {"message": "Successfully updated the item with name '{n}'\n{i}".format(n=name, i=item_map)}
        else:
            items_db_conns.create_item_by_name(item_map=item_map)
            create_item_details = {"message": "Item doesn't already exist. So, created the new item with name '{n}'\n{i}".format(n=name, i=item_map)}
        items_db_conns.close_connection()
        return create_item_details, 201

    def delete(self, name):
        items_db_conns = ItemsTable()
        result = items_db_conns.delete_item_by_name(name=name)
        delete_item_details = {"message": "Successfully deleted the item with name '{n}'".format(n=name)}
        items_db_conns.close_connection()
        return delete_item_details, 201
