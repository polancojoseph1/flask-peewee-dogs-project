from peewee import *

db = PostgresqlDatabase('dogs',
                        user='jefe', password='123',
                        host='localhost', port=5432)

db.connect()


class BaseModel(Model):
    class Meta:
        database = db


class Dog(BaseModel):
    name = CharField()
    breed = CharField()
    age = IntegerField()


db.drop_tables(Dog)

db.create_tables([Dog])

charlie = Dog(name="Charlie", breed="Schnauzer", age=1)

charlie.save()
