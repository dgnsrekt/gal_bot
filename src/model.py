from peewee import PostgresqlDatabase, Model
from peewee import BigIntegerField, CharField, DateTimeField
from peewee import IntegrityError
from datetime import datetime
from logger import getLogger

_logger = getLogger()

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
            kwargs['create_date'] = timeNow()
            kwargs['last_updated'] = timeNow()
            UserSettings.create(**kwargs)
            _logger.info(
                'User {} added to the database.'.format(kwargs['chat_id']))
        except IntegrityError:
            db.rollback()
            UserSettings.updateUserSettings(**kwargs)
            _logger.info(
                'User {} already exists database updated.'.format(kwargs['chat_id']))

    def updateUserSettings(**kwargs):
        try:
            user_id_Q = kwargs['chat_id']
            query = UserSettings.update(filter_settings=kwargs[
                                        'filter_settings'],
                                        last_updated=timeNow()).where(UserSettings.chat_id == user_id_Q)
            query.execute()
            _logger.info(
                'User {} updated in database.'.format(kwargs['chat_id']))
        except UserSettings.DoesNotExist:
            _logger.info(
                'User {} doesnot exist in database.'.format(kwargs['chat_id']))
            UserSettings.addUser(**kwargs)

    def getUserSettings(**kwargs):
        try:
            return UserSettings.get(UserSettings.chat_id == kwargs['chat_id']).filter_settings

        except UserSettings.DoesNotExist:
            _logger.info(
                'User {} doesnot exist in database.'.format(kwargs['chat_id']))
            UserSettings.addUser(filter_settings='N', **kwargs)
            return UserSettings.get(UserSettings.chat_id == kwargs['chat_id']).filter_settings


def timeNow():
    return datetime.now()


def createTables():
    db.create_tables([UserSettings], True)

if __name__ == '__main__':
    createTables()
