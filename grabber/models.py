from peewee import *
from playhouse.migrate import *

db = SqliteDatabase('dataset/plurks.db')


class Plurk(Model):
    id = BigIntegerField()
    content = CharField()
    content_raw = CharField()
    posted = TimestampField()
    # 20201126 add
    auto_tagged = BooleanField(default=False)
    manual_tagged = BooleanField(default=False)

    class Meta:
        database = db


if __name__ == '__main__':
    '''init'''
    # db.create_tables([Plurk])

    migrator = SqliteMigrator(db)
    
    '''migration: tagged fields'''
    # auto_tagged = BooleanField(default=False)
    # manual_tagged = BooleanField(default=False)
    # migrate(
    #     migrator.add_column('plurk', 'auto_tagged', auto_tagged),
    #     migrator.add_column('plurk', 'manual_tagged', manual_tagged),
    # )
