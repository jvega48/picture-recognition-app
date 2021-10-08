
from flask import Flask
import logging
import mysql.connector
import json
from flask_cors import CORS
from flask_restful import reqparse, Api, Resource
from mysql.connector.errors import Error

server = Flask(__name__)

# set up home route the app

@server.route("/")
def home():
    logging.info("logging into the home page")
    return "Home"





class db_operations(self):
    def db_cursor(database_name, table_name, table_info):
        cursor = None
        if database_name is None or database_name is None:
            return NotImplementedError
        
        if database_name is None:
            try:
                db_connector = mysql.connector.connect(
                    host='mysqldb',
                    user='root',
                    password='password',
                    database=database_name)
                cursor = db_connector.cursor()
                return cursor
            except mysql.connector.Error as err:
                print("Something went wrong: {}".format(err))
                return
        elif database_name and table_name is not None:
            str_query_drop_table = "DROP TABLE IF EXISTS{}".format(table_name)
            str_query_create_table = "CREATE TABLE {} (name VARCHAR(255), url VARCHAR(255))".format(table_name)
            try:
                db_connector = mysql.connector.connect(
                    host='mysqldb',
                    user='root',
                    password='password',
                    database=database_name)
                cursor = db_connector.cursor()
                return cursor
            except mysql.connector.Error as err:
                print("Something went wrong: {}".format(err))
                return

            cursor.close()

            cursor.execute(str_query_drop_table)
            cursor.execute(str_query_create_table)
            cursor.close()

        # TODO: need to figure out the  error handling for issues with the connections 
        return False

    def insert_photo(name, url):
        database_name='images_core'
        cursor = db_cursor(database_name)
        str_query = "INSERT into photos(name, url) VALUES ({},{});".format(name, url)
        
        if cursor is None:
            return str(Error("Db cursor is none cannot continue"))
        try:
            cursor.excute(str_query)
            cursor.commit()
            return True
        except mysql.connector.Error as err:
            print("Something went wrong when inserting record: {}".format(err))
            return False

    def get_all_images():
        mydb = mysql.connector.connect(
            host='mysqldb',
            user='root',
            password='password',
            database='images_core')
        cursor = mydb.cursor()


        cursor.execute("SELECT * FROM photos")

        #describ the headers
        row_headers = [x[0] for x in cursor.description]
        results = cursor.fetchall()

        json_data = []

        for result in results:
            json_data.append(dict(zip(row_headers, result)))

        cursor.close()

        return json.dumps(json_data)
    


@server.route('/init_db')
def db_init():
    object_a = db_operations()
    print(object_a)
    e = object_a.db_cursor('images_core', 'photos')
    if e:
        return 'non init database'
    return 'init database'



if __name__ == '__main__':
    server.run(host='0.0.0.0')
    server.run(debug=True)