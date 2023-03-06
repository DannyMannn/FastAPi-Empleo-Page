from peewee import *
from modelo import connection as database

class Empleo(Model):
    pagoMensual = CharField(max_length = 20, unique = True)
    descripcion = CharField(max_length = 100, unique = True)

    def __str__(self):
        return self.descripcion

    class Meta:
        database = database
        table_name = "Empleo"