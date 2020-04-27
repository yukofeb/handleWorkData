#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from urllib.parse import urlencode
from requests.auth import HTTPBasicAuth

class TogglApi():
    def __init__(self, api_token, timezone):
        self.api_token = api_token
        self.timezone = timezone

    def _create_url(self, type, params={}):
        """
        Make Request URL
        """
        url = 'https://www.toggl.com/api/v8/{}'.format(type)
        if len(params) > 0:
            url = '{0}?{1}'.format(url, urlencode(params))
        return url

    def _request(self, url, method):
        """
        Request to Toggl API
        """
        headers = {'content-type': 'application/json'}
        if method == 'GET':
            return requests.get(url, headers=headers, auth=HTTPBasicAuth(self.api_token, 'api_token'))
        elif method == 'POST':
            return requests.post(url, headers=headers, auth=HTTPBasicAuth(self.api_token, 'api_token'))
        else:
            raise ValueError('Invalid REST method "{}"'.format(method))

    def lists_projects(self):
        """
        [Not Using]
        Lists projects data
        """
        url = self._create_url(type='workspaces')
        return self._request(url=url, method='GET')

    def lists_time_entries(self, start_date, end_date):
        """
        Lists time entries
        """
        start_date = '{0}{1}'.format(start_date.isoformat(), self.timezone)
        end_date = '{0}{1}'.format(end_date.isoformat(), self.timezone)
        url = self._create_url(type='time_entries', params={'start_date': start_date, 'end_date': end_date})
        return self._request(url=url, method='GET')