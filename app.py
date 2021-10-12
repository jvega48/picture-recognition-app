
from flask import Flask, jsonify, request
import logging
import mysql.connector
import json
from flask_cors import CORS
from flask_restful import reqparse, Api, Resource
from mysql.connector.errors import Error
import logging
logging.basicConfig(level=logging.INFO)

server = Flask(__name__)
api = Api(server)
class DBOperations(Resource):
    def __init__(self):
        return
    
    def check_existing_table(self, database_name, table_name):
        try:
            db_connector = self.db_connector()
            crs = db_connector.cursor()
            crs.execute("SHOW TABLES")

            for x in crs:
                if x[0] == table_name:
                    return True
        except mysql.connector.Error as err:
            logging.info('error in the connector... %s', err)
            print("Something went wrong: {}".format(err))
            return None 

    # def create_table(self, database_name, table_name, fields):
    #     is_database = self.check_existing_db(database_name)
    #     connected_to_database = self.connect_to_database(database_name)
    #     if is_database:
    #         check_table = self.check_existing_table(table_name)
    #         if check_table is False:
    #             if connect_to_database:
    #                 crs = self.db_cursor(database_name)
    #                 try:
    #                     crs.execute("CREATE TABLE {} ({} {}, address VARCHAR(255))".format(table_name))
    #                 except mysql.connector.Error as err:
    #                     logging.info('error in the connector... %s', err)
    #                     print("Something went wrong: {}".format(err))
    #                 return None 

    def check_existing_db(self, database_name):
        try:
            db_connector = self.db_connector()
            crs = db_connector.cursor()
            crs.execute("SHOW DATABASES")
            
            for x in crs:
                if x[0]==database_name:
                    return True                
            return True
        except mysql.connector.Error as err:
            logging.info('error in the connector... %s', err)
            print("Something went wrong: {}".format(err))
            return None 
    
    # connected true else False
    def connect_to_database(self, database_name):
        try:
            db_connector = mysql.connector.connect(
                host='mysqldb',
                user='root',
                password='password',
                database=database_name)
            return True
        except mysql.connector.Error as err:
            logging.info('error in the connector... %s', err)
            print("Something went wrong: {}".format(err))
            return False

    def db_connector(self):
        try:
            db_connector = mysql.connector.connect(
                host='mysqldb',
                user='root',
                password='password')
            return db_connector
        except mysql.connector.Error as err:
            logging.info('error in the connector... %s', err)
            print("Something went wrong: {}".format(err))
            return None
    
    def db_cursor(self, database_name):

        logging.info('inisde the Init db...')
        # step one check if the database exist already 
        # if databse exist already don't create one 
        # if database exist and table doestn exisit
        # create a new table if datbase exisit
        # if dababse doesnt exist then table wont exist
        # create both 
        if database_name:
            found = self.check_existing_db(database_name)
            if found:
                try:
                    db_connector = mysql.connector.connect(
                        host='mysqldb',
                        user='root',
                        password='password',
                        database=database_name)
                    return db_connector
                except mysql.connector.Error as err:
                    logging.info('error in the connector... %s', err)
                    print("Something went wrong: {}".format(err))
                    return None
            else:
                try:
                    db_connector = self.db_connector()
                    cur = db_connector.cursor()
                    cur.execute("CREATE DATABASE {}".format(database_name))
                    return db_connector,
                except mysql.connector.Error as err:
                    logging.info('error in the connector... %s', err)
                    print("Something went wrong: {}".format(err))
                    return None
                
        else:
            return self.db_connector()

        # TODO: need to figure out the  error handling for issues with the connections 
class InsertPhotos(Resource):
    def insert_photo(self, name, url):
        db_opr = DBOperations()
        database_name='images_core'
        con = db_opr.db_cursor(database_name)
        cursor = con.cursor()
        if con is None:
            return str(Error("Db cursor is none cannot continue."))

        str_query = "INSERT into photos(name, url) VALUES (%s, %s);"
        
        if con is None:
            return str(Error("Db cursor is none cannot continue"))
        try:
            cursor.execute(str_query, (name,url))
            con.commit()
            logging.info("record inserted. %s", cursor.rowcount, )
            return str("Db insert documents successful : {}".format(True))
        except mysql.connector.Error as err:
            print("Something went wrong when inserting record: {}".format(err))
            return str("Db insert documents successful : {}".format(False))
    
    def post(self, name, url):
        message = self.insert_photo(name, url)
        return jsonify({'message': message})

    # def get(self):
    #     data = GetPhotos.get_all_images()
    #     return jsonify({'data': data})
class GetPhotos(Resource):
    def get_all_images(self):
        db_opr = DBOperations()
        database_name ='images_core'
        con = db_opr.db_cursor(database_name)

        if con is None:
            return str(Error("Db cursor is none cannot continue. {}".format(con)))
        
        query = con.cursor(buffered=True).execute("SELECT * FROM photos")
        results = None

        if query:        
            row_headers = [x[0] for x in con.cursor().description]
            results = con.cursor().fetchall()
        
        json_data = []
        if results:
            for result in results:
                json_data.append(result)


            return json.dumps(json_data)
        else:
            return json.dumps(json_data)
    
    # def post(self, name, url):
    #     message = InsertPhotos.insert_photo(name, url)
    #     return jsonify({'message': message})

    def get(self):
        data = self.get_all_images()
        return jsonify({'data': data})

api.add_resource(InsertPhotos, '/insert_photo/<string:name>/<string:url>/')
api.add_resource(GetPhotos, '/get_all_photos')


if __name__ == '__main__':
    server.run(host='0.0.0.0')
    server.run(debug=True)