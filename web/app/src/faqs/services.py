# -*- coding: utf-8 -*-

import dateutil.parser
from app.src.utils import api_manager
from app.src.utils import constants


def get_faqs(mode='unarchived'):
    params = {'mode': mode}
    url = constants.FAQ_ALL
    req = api_manager.get_request_no_auth(url, params)
    faqs = []
    if req.status_code == 200:
        try:
            faqs = req.json()
            for faq in faqs:
                faq['created_date'] = dateutil.parser.parse(
                    faq['created_date'])
        except ValueError:
            faqs = []
    return faqs


def view_faq(faq_id):
    url = constants.FAQ_ONE.format(faq_id=faq_id)
    req = api_manager.get_request_no_auth(url)
    try:
        faq = req.json()
        faq['created_date'] = dateutil.parser.parse(faq['created_date'])
    except ValueError:
        faq = {}
    return faq


def get_questions(faq_id, mode='unarchived'):
    params = {'mode': mode}
    url = constants.FAQ_QUESTION_ALL.format(faq_id=faq_id)
    req = api_manager.get_request_no_auth(url, params)
    try:
        questions = req.json()
        for question in questions:
            question['created_date'] = dateutil.parser.parse(
                question['created_date'])
    except ValueError:
        questions = []
    return questions


def view_questions(faq_id, question_id):
    url = constants.FAQ_QUESTION_ONE.format(faq_id=faq_id,
                                            question_id=question_id)
    req = api_manager.get_request_no_auth(url)
    try:
        question = req.json()
        question['created_date'] = dateutil.parser.parse(
            question['created_date'])
    except ValueError:
        question = {}
    return question
