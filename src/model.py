from peewee import *
from datetime import datetime

db = PostgresqlDatabase('galbot')


class BaseModel(Model):

    class Meta:
        database = db


class UserSettings(BaseModel):
    chat_id = BigIntegerField(unique=True)
    filter_settings = CharField()
    create_date = DateTimeField()
    last_updated = DateTimeField()

    def addUser(**kwargs):
        try:
            kwargs['last_updated'] = timeNow()
            print(kwargs)
            UserSettings.create(**kwargs)
        except IntegrityError:
            db.rollback()
            UserSettings.updateUserSettings(**kwargs)

    def updateUserSettings(**kwargs):
        user_id_query = kwargs['chat_id']
        query = UserSettings.update(filter_settings=kwargs[
                                    'filter_settings'], last_updated=timeNow()).where(UserSettings.chat_id == user_id_query)
        query.execute()


def timeNow():
    return datetime.now()


def create_tables():
    db.create_tables([UserSettings], True)


UserSettings.addUser(chat_id='12345', filter_settings='Z',
                     create_date=datetime.now())

# UserSettings.updateUserSettings(chat_id='12345', filter_settings='G')
# UserSettings.create(chat_id=1234565, filter_settings='N',
#                     create_date=datetime.now(), last_updated=datetime.now())

# print(UserSettings.select().where(
#     UserSettings.chat_id == 1234565))

# query = UserSettings.update(filter_settings='C', last_updated=datetime.now()).where(
#     UserSettings.chat_id == 1234565)
# query.execute()
