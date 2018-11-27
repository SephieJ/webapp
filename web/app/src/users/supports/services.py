# -*- coding: utf-8 -*-

import dateutil.parser
from app.src.utils import api_manager
from app.src.utils import constants


# Create Support Tickets
def raise_support(user_id, subject, message):
    ticket = {
        'subject': subject,
        'message': message
    }
    url = constants.RAISE_SUPPORT.format(user_id=user_id)
    req = api_manager.post_request(url, ticket)
    return req


# Get Support Requests
def get_tickets(user_id, mode='unarchived'):
    params = {'mode': mode}
    url = constants.TICKET_ALL.format(user_id=user_id)
    req = api_manager.get_request(url, params)
    tickets = req.json()
    for ticket in tickets:
        ticket['created_date'] = dateutil.parser.parse(ticket['created_date'])
    return tickets


# Get Support Requests
def get_support_message(user_id, mode='unarchived'):
    params = {'mode': mode}
    url = constants.TICKET_ALL.format(user_id=user_id)
    req = api_manager.get_request(url, params)
    try:
        support_threads = req.json()
        for support_thread in support_threads:
            support_thread['date_created'] = dateutil.parser.parse(
                support_thread['date_created'])
    except ValueError:
        support_threads = []
    return support_threads
