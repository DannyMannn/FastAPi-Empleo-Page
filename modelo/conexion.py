from peewee import *

connection = MySQLDatabase(
    "Empleo",
    user = "root", password = "",
    host = "localhost", port = 3306
)