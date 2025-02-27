from bson import ObjectId
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from flask_mysqldb import MySQL
import os

load_dotenv()


app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGO_URI")

mongo = PyMongo(app)

app.config["MYSQL_HOST"]= os.getenv("MYSQL_HOST")
app.config["MYSQL_DB"]= os.getenv("MYSQL_DB")
app.config["MYSQL_USER"]= os.getenv("MYSQL_USER")
app.config["MYSQL_PASSWORD"]= os.getenv("MYSQL_PASSWORD")

mysql = MySQL(app)

@app.route('/user', methods=['POST'])
def add_user():

    nombre = request.json['nombre']
    apellido = request.json['apellido']
    color = request.json['color']

    if nombre and apellido and color:
        mongo.db.usuarios.insert_one({"nombre":nombre, "apellido":apellido, "color": color})
        return jsonify({"message": "Usuario añadido correctamente"})
    
    return jsonify({"message": "Usuario añadido correctamente"})


@app.route('/user/<id>', methods=['GET'])
def get_user(id):

    user = mongo.db.usuarios.find({"_id": ObjectId(id)})
    if user:
        return jsonify({"El usuario que buscas es =>": user})
    
    return jsonify({"message": "El usuario que buscas no se encuentra en la base de datos"})

@app.route('/user/<id>', methods=['DELETE'])
def delete_user(id):

    mongo.db.usuarios.delete_one({"_id": ObjectId(id)})
    
    return jsonify({"message": "Usuario eliminado con exito"})

@app.route('/user/<id>', methods=['PUT'])
def update_user(id):
    nombre = request.json['nombre']
    apellido = request.json['apellido']
    color = request.json['color']

    if nombre and apellido and color:
        mongo.db.usuarios.update_one({"_id": ObjectId(id)}, {"$set": {"nombre": nombre, "apellido": apellido, "color":color}})
        
        return jsonify({"message": "Usuario modificado con exito"})
    
    return jsonify({"message": "Usuario no modificado con exito"})

#################################################################
#################################################################
#################################################################


@app.route('/user_sql', methods=['POST'])
def add_user_mysql():

    nombre = request.json['nombre']
    apellido = request.json['apellido']
    color = request.json['color']

    if nombre and apellido and color:

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO usuarios (nombre, apellido, color) VALUES (%s,%s,%s)',(nombre, apellido, color))
        mysql.connection.commit()
        
        return jsonify({"message": "Usuario añadido correctamente"})
    
    return jsonify({"message": "Usuario añadido correctamente"})


@app.route('/user_sql/<id>', methods=['GET'])
def get_user_mysql(id):

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM usuarios WHERE id = %s',(id,))
    user = cur.fetchone()

    if user:
        return jsonify({"El usuario que buscas es =>": user})
    
    return jsonify({"message": "El usuario que buscas no se encuentra en la base de datos"})

@app.route('/user_sql/<id>', methods=['PUT'])
def update_user_mysql(id):
    nombre = request.json['nombre']
    apellido = request.json['apellido']
    color = request.json['color']

    if nombre and apellido and color:

        cur = mysql.connection.cursor()
        cur.execute('UPDATE usuarios SET nombre =%s, apellido= %s, color = %s WHERE id = %s', (nombre, apellido, color, id)) 
        mysql.connection.commit()       
        return jsonify({"message": "Usuario modificado con exito"})
    
    return jsonify({"message": "Usuario no modificado con exito"})


@app.route('/user_sql/<id>', methods=['DELETE'])
def delete_user_mysql(id):

    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM usuarios WHERE id=%s", (id,))  
    mysql.connection.commit()

    return jsonify({"message": "Usuario eliminado con exito"})


if __name__ == '__main__':
    app.run(debug=True)