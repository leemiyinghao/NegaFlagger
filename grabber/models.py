from peewee import *

db = SqliteDatabase('dataset/plurks.db')
class Plurk(Model):
    id = BigIntegerField()
    content = CharField()
    content_raw = CharField()
    posted = TimestampField()

    class Meta:
        database = db

if __name__ == '__main__':
    db.create_tables([Plurk])