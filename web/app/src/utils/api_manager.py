# -*- coding: utf-8 -*-

import requests
from flask import session, abort


def get_request(url, data=None):
    req = None
    basic_auth = session['user_basic']
    headers = {
        'Authorization': basic_auth
    }
    try:
        if data:
            req = requests.get(url, params=data, headers=headers)
        else:
            req = requests.get(url, headers=headers)
    except requests.exceptions.ConnectionError:
        abort(503)
    if req.status_code == 401:
        abort(401)
    return req


def post_request(url, data=None, files=None):
    basic_auth = session['user_basic']
    headers = {
        'Authorization': basic_auth
    }
    if files:
        req = requests.post(url, files=files, headers=headers)
    elif data:
        req = requests.post(url, json=data, headers=headers)
    else:
        req = requests.post(url, headers=headers)
    if req.status_code == 401:
        abort(401)
    return req


def put_request(url, data=None):
    basic_auth = session['user_basic']
    headers = {
        'Authorization': basic_auth
    }
    if data:
        req = requests.put(url, json=data, headers=headers)
    else:
        req = requests.put(url, headers=headers)
    return req


def delete_request(url, data=None):
    basic_auth = session['user_basic']
    headers = {
        'Authorization': basic_auth
    }
    if data:
        req = requests.delete(url, json=data, headers=headers)
    else:
        req = requests.delete(url, headers=headers)
    return req


def get_request_no_auth(url, data=None):
    req = None
    try:
        if data:
            req = requests.get(url, params=data)
        else:
            req = requests.get(url)
    except requests.exceptions.ConnectionError:
        abort(503)
    return req


def post_request_no_auth(url, data):
    req = requests.post(url, json=data)
    return req


def post_request_profanity(url, data):
    req = requests.post(url, data=data)
    return req


def put_request_no_auth(url, data):
    req = requests.put(url, json=data)
    return req


def delete_request_no_auth(url):
    req = requests.delete(url)
    return req
