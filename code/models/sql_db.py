import sqlite3

class SqliteConnections:
    def __init__(self):
        self.connection = sqlite3.connect('data.db', check_same_thread=False)
        self.cursor = self.connection.cursor()

    def close_connection(self):
        self.connection.commit()
        self.connection.close()


class UserTable(SqliteConnections):
    def __init__(self):
        SqliteConnections.__init__(self)
        self.table_name = "users"
        self.initialize()
    
    def initialize(self):
        create_users_table = "CREATE TABLE IF NOT EXISTS {t_n}(id INTEGER PRIMARY KEY, username text, password text)".format(t_n=self.table_name)
        self.cursor.execute(create_users_table)

    def query_by_username(self, username):
        query = "SELECT * FROM {t_n} WHERE username=?".format(t_n=self.table_name)
        result = self.cursor.execute(query, (username, ))
        return result

    def query_by_userid(self, userid):
        query = "SELECT * FROM {t_n} WHERE ID=?".format(t_n=self.table_name)
        result = self.cursor.execute(query, (userid, ))
        return result

    def insert_users_details(self, username, password):
        query = "INSERT INTO {t_n} VALUES(NULL, ?, ?)".format(t_n=self.table_name)
        self.cursor.execute(query, (username, password))


class ItemsTable(SqliteConnections):
    def __init__(self):
        SqliteConnections.__init__(self)
        self.table_name = "items"
        self.initialize()

    def initialize(self):
        create_items_table = "CREATE TABLE IF NOT EXISTS {t_n}(name text PRIMARY KEY, price real)".format(t_n=self.table_name)
        self.cursor.execute(create_items_table)

    def get_items(self):
        query = "SELECT * FROM {t_n}".format(t_n=self.table_name)
        result = self.cursor.execute(query)
        return result

    def get_item_by_name(self, name):
        query = "SELECT * FROM {t_n} WHERE name=?".format(t_n=self.table_name)
        result = self.cursor.execute(query, (name, ))
        return result

    def create_item_by_name(self, item_map):
        query = "INSERT INTO {t_n} VALUES(?, ?)".format(t_n=self.table_name)
        result = self.cursor.execute(query, (item_map['name'], item_map['price']))
        return result

    def update_item_price_by_name(self, item_map):
        query = "UPDATE {t_n} SET price=? WHERE name=?".format(t_n=self.table_name)
        result = self.cursor.execute(query, (item_map['price'], item_map['name']))
        return result

    def delete_item_by_name(self, name):
        query = "DELETE FROM {t_n} WHERE name=?".format(t_n=self.table_name)
        result = self.cursor.execute(query, (name, ))
        return result
