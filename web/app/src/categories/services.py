# -*- coding: utf-8 -*-

import dateutil.parser
from app.src.utils import api_manager
from app.src.utils import constants


def get_categories(mode='unarchived'):
    params = {'mode': mode}
    req = api_manager.get_request_no_auth(constants.CATEGORY_ALL, params)
    categories = []
    if req.status_code == 200:
        try:
            categories = req.json()
            for category in categories:
                category['created_date'] = dateutil.parser.parse(
                    category['created_date'])
        except ValueError:
            categories = []

    return categories


def get_category(category_id, mode='unarchived'):
    params = {'mode': mode}
    url = constants.CATEGORY_ONE.format(category_id=category_id)
    req = api_manager.get_request_no_auth(url, params)
    category = None
    if req.status_code == 200:
        try:
            category = req.json()
            category['created_date'] = dateutil.parser.parse(
                category['created_date'])
        except ValueError:
            category = {}

    return category


def get_subcategories(category_id, mode='unarchived'):
    url = constants.SUBCATEGORIES_ALL.format(category_id=category_id)
    req = api_manager.get_request_no_auth(url)
    subcategories = []
    if req.status_code == 200:
        try:
            subcategories = req.json()
            for subcategory in subcategories:
                subcategory['created_date'] = dateutil.parser.parse(
                    subcategory['created_date'])
        except ValueError:
            subcategories = []
    return subcategories


def get_subcategory(category_id, subcategory_id, mode='unarchived'):
    url = constants.SUBCATEGORIES_ONE.format(category_id=category_id,
                                             subcategory_id=subcategory_id)
    req = api_manager.get_request_no_auth(url)
    subcategory = None
    if req.status_code == 200:
        try:
            subcategory = req.json()
            subcategory['created_date'] = dateutil.parser.parse(
                subcategory['created_date'])
        except ValueError:
            subcategory = {}
    return subcategory
