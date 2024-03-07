import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()


# # Create 'users' table
# create_users_table = "CREATE TABLE users(id INTEGER PRIMARY KEY, username text, password text)"
# cursor.execute(create_users_table)

# # Insert an user details into db
# user_details = ("1", "akh1", "akh1_pass")
# insert_user = "INSERT INTO users values(?, ?, ?)"
# cursor.execute(insert_user, user_details)

# # Insert list of users' details into db
# users_details_list = [ 
#     ("2", "akh2", "akh2_pass"), 
#     ("3", "akh3", "akh3_pass"),
# ]
# insert_multiple_users = "INSERT INTO users values(?, ?, ?)"
# cursor.executemany(insert_multiple_users, users_details_list)

# Verify if data is replicated in db
select_query = "SELECT * FROM users"
for row in cursor.execute(select_query):
    print(row)


# Save the data into disk
connection.commit()

# Close the connection
connection.close()
