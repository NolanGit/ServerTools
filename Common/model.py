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


class App(peewee.Model):
    '''
        app_name, expect_price
    '''
    app_name = peewee.CharField()
    expect_price = peewee.IntegerField()
    is_valid = peewee.IntegerField()

    class Meta:
        database = database


class AppPrice(peewee.Model):
    '''
        app name, price, date, crawling_times, time
    '''
    app_name = peewee.CharField()
    price = peewee.CharField()
    date = peewee.DateField()
    crawling_times = peewee.IntegerField()
    time = peewee.TimeField()

    class Meta:
        database = database


class City(peewee.Model):
    '''
        city_name, province
    '''
    city_name = peewee.CharField()
    province_id = peewee.CharField()

    class Meta:
        database = database


class Province(peewee.Model):
    '''
        province_name
    '''
    province_name = peewee.CharField()

    class Meta:
        database = database


class Weather(peewee.Model):
    '''
        city_code, max_temp, min_temp, date, time
    '''
    city_code = peewee.CharField()
    max_temp = peewee.CharField()
    min_temp = peewee.CharField()
    date = peewee.DateField()
    time = peewee.TimeField()

    class Meta:
        database = database


class AQI(peewee.Model):
    '''
        city_code, aqi, main, pm10, pm25, no2, so2, co, o3
    '''
    city_code = peewee.CharField()
    site_name=peewee.CharField()
    aqi = peewee.CharField()
    main = peewee.CharField()
    pm10 = peewee.CharField()
    pm25 = peewee.CharField()
    no2 = peewee.CharField()
    so2 = peewee.CharField()
    co =peewee.CharField()
    o3 = peewee.CharField()
    date = peewee.DateField()
    crawling_times = peewee.IntegerField()
    time = peewee.TimeField()

    class Meta:
        database = database


# GoldPrice().create_table()
# AppPrice().create_table()
# App().create_table()
# Weather.drop_table()
# Weather().create_table()
# AQI().drop_table()
# AQI().create_table()
City().create_table()
Province().create_table()
