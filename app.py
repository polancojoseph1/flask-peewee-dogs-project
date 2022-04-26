from flask import Flask, request, jsonify
# import json
from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model

db = PostgresqlDatabase('dogs',
                        user='jefe', password='123',
                        host='localhost', port=5432)


class BaseModel(Model):
    class Meta:
        database = db


class Dog(BaseModel):
    name = CharField()
    breed = CharField()
    age = IntegerField()


db.connect()


app = Flask(__name__)


@app.route('/dogs/', methods=['GET', 'POST'])
@app.route('/dogs/<id>', methods=['GET', 'PUT', 'DELETE'])
def endpoint(id=None):

    # get request
    if request.method == 'GET':
        # if there is an id get a specific person
        if id:
            return jsonify(model_to_dict(Dog.get(Dog.id == id)))
        # else if there is no id get all people
        else:
            dogsList = []
            for dog in Dog.select():
                dogsList.append(model_to_dict(dog))
            return jsonify(dogsList)

    # put request
    if request.method == 'PUT':
        old_dog = Dog.get(Dog.id == id)
        new_dog = dict_to_model(Dog, request.get_json())
        old_dog.age = new_dog.age
        old_dog.breed = new_dog.breed
        old_dog.name = new_dog.name
        old_dog.save()
        return jsonify(model_to_dict(Dog.get(Dog.id == id)))

    # post request, creates a new person
    if request.method == 'POST':
        new_dog = dict_to_model(Dog, request.get_json())
        new_dog.save()
        return jsonify({"success": True})

    # delete request
    if request.method == 'DELETE':
        dog = Dog.get(Dog.id == id)
        dog.delete_instance()
        return jsonify({"deleted": True})


app.run(port=9000, debug=True)
