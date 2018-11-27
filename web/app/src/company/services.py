# -*- coding: utf-8 -*-

import dateutil.parser
from app.src.utils import api_manager
from app.src.utils import constants


# Get Company
def get_company(company_id):
    url = constants.COMPANY_ONE.format(company_id=company_id)
    req = api_manager.get_request_no_auth(url)
    try:
        company = req.json()
        company['created_date'] = dateutil.parser.parse(
            company['created_date'])
    except ValueError:
        company = {}
    return company


# Get Company's Members
def company_members(company_id):
    url = constants.COMPANY_MEMBERS.format(company_id=company_id)
    req = api_manager.get_request_no_auth(url)
    members = []
    if req.status_code == 200:
        try:
            members = req.json()
            for member in members:
                member['created_date'] = dateutil.parser.parse(
                    member['created_date'])
        except ValueError:
            members = []
    return members


# Send Inquiry via Contact Us
def send_inquiry(name, email, message):
    contact_us = {
        'name': name,
        'email': email,
        'message': message
    }
    url = constants.CONTACT_US
    req = api_manager.post_request_no_auth(url, contact_us)
    return req
