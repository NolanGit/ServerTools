import os
import peewee
import datetime

PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))
database = peewee.SqliteDatabase(PATH("../database.db"))


class GoldPrice(peewee.Model):
    '''
        price, date, crawling_times, time
    '''

    price = peewee.CharField()
    date = peewee.DateField()
    crawling_times = peewee.IntegerField()
    time = peewee.TimeField()

    class Meta:
        database = database

class AppPrice(peewee.Model):
    '''
        app name, price, date, crawling_times, time
    '''
    app_name= peewee.CharField()
    price = peewee.CharField()
    date = peewee.DateField()
    crawling_times = peewee.IntegerField()
    time = peewee.TimeField()

    class Meta:
        database = database

# GoldPrice().create_table()
# AppPrice().create_table()