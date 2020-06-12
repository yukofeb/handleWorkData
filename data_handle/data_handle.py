#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
from datetime import datetime as dt
from datetime import timedelta as td
from pytz import timezone

class DataHandle():
    def __init__(self, target_data, timezone_area):
        self.target_data = target_data
        self.timezone_area = timezone_area

    def _timedelta_to_string(self, sec):
        """
        Timedelta to string for printing csv
        """
        minutes, seconds = divmod(sec, 60)
        hours, minutes = divmod(minutes, 60)
        return '{0:02d}:{1:02d}:{2:02d}'.format(int(hours), int(minutes), int(seconds))

    def _list_selected_period(self, start_date, end_date):
        for day in range((end_date - start_date).days):
                yield (start_date + td(day)).date()

    def _calculate_worktime(self, start_date, end_date):
        """
        Calculate worktime data of Toggl
        """
        # 日付、開始時間、終了時間、休憩時間をまとめたデータを作成
        ## 指定した1ヶ月のdataをDataFrameに入れる
        df = pd.read_json(self.target_data)
        df = df[['id', 'start', 'stop', 'duration']]
        df['start'] = df['start'].apply(lambda x: pd.Timestamp(x).astimezone(timezone(self.timezone_area)))
        df['stop'] = df['stop'].apply(lambda x: pd.Timestamp(x).astimezone(timezone(self.timezone_area)))
        df['worktime'] = df['duration'].apply(lambda x: td(seconds=x))
        df['start_date'] = df['start'].apply(lambda x: x.date())
        
        ## 実質労働時間
        df_actual = df.groupby(['start_date'])['worktime'].sum()

        ## 延労働時間
        df_sum_min = df.groupby(['start_date']).apply(lambda x: x['start'].min())
        df_sum_max = df.groupby(['start_date']).apply(lambda x: x['stop'].max())
        df_sum = pd.concat([df_sum_min, df_sum_max], names=['min', 'max'], axis=1).rename(columns={0: 'min', 1: 'max'})
        df_sum['wholeworktime'] = df_sum['max'] - df_sum['min']

        ## 休憩時間
        result = pd.concat([df_actual, df_sum], axis=1)
        result['breaktime'] = result['wholeworktime'] - result['worktime']

        ## 整形
        result['min'] = result['min'].apply(lambda x: x.time())
        result['max'] = result['max'].apply(lambda x: x.time())
        result['breaktime'] = result['breaktime'].apply(lambda x: self._timedelta_to_string(x.total_seconds()))

        ## 日付の範囲取得
        array_date = []
        for i in self._list_selected_period(start_date, end_date):
            array_date.append(i)
        pd_date = pd.Series(array_date)
        result = result.merge(pd_date.to_frame().rename(columns={0: 'date'}), left_on='start_date', right_on='date', how='right')
        result = result[['date', 'min', 'max', 'breaktime']].fillna('').sort_values('date').reset_index(drop=True)

        return result

    def _print_result(self, summary_data):
        """
        Print calculated data
        """
        summary_data.to_csv('summary.csv')

    def create_monthly_summary(self, start_date, end_date):
        summary = self._calculate_worktime(start_date, end_date)
        self._print_result(summary)