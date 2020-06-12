#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import click
import sys
import configparser
import datetime as dt
from api import toggl_api
from data_handle import data_handle

conf = configparser.ConfigParser()
conf.read('config.ini')
APIKEY = conf['toggl']['APIKEY']
TIMEZONE = conf['toggl']['TIMEZONE']
TIMEZONE_AREA = conf['toggl']['TIMEZONE_AREA']

@click.command()
@click.argument('year')
@click.argument('month')
def make_monthly_summary(year, month):
    # データ取得
    t_api = toggl_api.TogglApi(APIKEY, TIMEZONE)

    start_date = dt.datetime(year=int(year), month=int(month), day=1, hour=0)
    end_date = dt.datetime(year=int(year), month=int(month)+1, day=1, hour=0)
    response = t_api.lists_time_entries(start_date=start_date, end_date=end_date)
    if response.status_code != 200:
        print('[Error]Invalid Response Code from Toggl API.')
        sys.exit()

    # データ加工、結果出力
    d_handle = data_handle.DataHandle(response.text, TIMEZONE_AREA)
    d_handle.create_monthly_summary(start_date=start_date, end_date=end_date)

if __name__ == '__main__':
    make_monthly_summary()