from peewee import *

db = PostgresqlDatabase('galbot')


class BaseModel(Model):

    class Meta:
        database = db


class UserSettings(BaseModel):
    chat_id = BigIntegerField()
    filter_settings = CharField()
    create_date = DateTimeField()
    last_updated = DateTimeField()
