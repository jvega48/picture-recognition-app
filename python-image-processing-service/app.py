
from flask import Flask
import logging
import mysql.connector
import json

server = Flask(__name__)

# set up home route the app

@server.route("/")
def home():
    logging.info("logging into the home page")
    return "Home"

@server.route("/images")
def get_images():
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
        json_data.append(dict(zip(row_headers, results)))

    cursor.close()

    return json.dumps(json_data)



@server.route('/init_db')
def db_init():
  mydb = mysql.connector.connect(
    host="mysqldb",
    user="root",
    password="password"
  )
  cursor = mydb.cursor()

  cursor.execute("DROP DATABASE IF EXISTS images_core")
  cursor.execute("CREATE DATABASE images_core")
  cursor.close()

  mydb = mysql.connector.connect(
    host="mysqldb",
    user="root",
    password="password",
    database="images_core"
  )
  cursor = mydb.cursor()

  cursor.execute("DROP TABLE IF EXISTS photos")
  cursor.execute("CREATE TABLE photos (name VARCHAR(255), url VARCHAR(255))")
  cursor.close()

  return 'init database'


def home():
    logging.info("logging into the home page")
    return "Home"


if __name__ == '__main__':
    server.run(host='0.0.0.0')
    server.run(debug=True)