# -*- coding: utf-8 -*-

import dateutil.parser
from app.src.utils import api_manager
from app.src.utils import constants


def get_transactions(user_id, mode='unarchived'):
    params = {'mode': mode}
    url = constants.USER_TRANSACTIONS.format(user_id=user_id)
    req = api_manager.get_request(url, params)
    try:
        transactions = req.json()
        for transaction in transactions:
            transaction['booking_start_date'] = dateutil.parser.parse(
                transaction['booking_start_date'])
            transaction['booking_end_date'] = dateutil.parser.parse(
                transaction['booking_end_date'])
            formatted_price = ('%.2f' % transaction['resource']['price'])
            transaction['resource']['price'] = formatted_price
    except ValueError:
        transactions = []
    return transactions


def get_selling_transactions(user_id, mode='unarchived'):
    params = {'mode': mode}
    url = constants.USER_TRANSACTIONS_SELLING.format(user_id=user_id)
    req = api_manager.get_request(url, params)
    try:
        selling_transactions = req.json()
        for transaction in selling_transactions:
            transaction['booking_start_date'] = dateutil.parser.parse(
                transaction['booking_start_date'])
            transaction['booking_end_date'] = dateutil.parser.parse(
                transaction['booking_end_date'])
            formatted_price = ('%.2f' % transaction['resource']['price'])
            transaction['resource']['price'] = formatted_price
            url_agreement = constants.GET_RESOURCE_AGREEMENT.format(reference_code=transaction['reference_code'])
            req_agreement = api_manager.get_request(url_agreement, params)
            transaction['agreements'] = req_agreement.json()
    except ValueError:
        selling_transactions = []
    return selling_transactions


def get_buying_transactions(user_id, mode='unarchived'):
    params = {'mode': mode}
    url = constants.USER_TRANSACTIONS_BUYING.format(user_id=user_id)
    req = api_manager.get_request(url, params)
    try:
        buying_transactions = req.json()
        for transaction in buying_transactions:
            transaction['booking_start_date'] = dateutil.parser.parse(
                transaction['booking_start_date'])
            transaction['booking_end_date'] = dateutil.parser.parse(
                transaction['booking_end_date'])
            formatted_price = ('%.2f' % transaction['resource']['price'])
            transaction['resource']['price'] = formatted_price
            url_agreement = constants.GET_RESOURCE_AGREEMENT.format(reference_code=transaction['reference_code'])
            req_agreement = api_manager.get_request(url_agreement, params)
            transaction['agreements'] = req_agreement.json()
    except ValueError:
        buying_transactions = []
    return buying_transactions


def get_transaction_details(user_id, transaction_id, mode='unarchived'):
    url = constants.USER_TRANSACTION_DETAIL.format(
        user_id=user_id, transaction_id=transaction_id)
    req = api_manager.get_request(url)
    try:
        transaction = req.json()
        transaction['booking_start_date'] = dateutil.parser.parse(
            transaction['booking_start_date'])
        transaction['booking_end_date'] = dateutil.parser.parse(
            transaction['booking_end_date'])
        formatted_price = ('%.2f' % transaction['resource']['price'])
        transaction['resource']['price'] = formatted_price
        url_agreement = constants.GET_RESOURCE_AGREEMENT.format(reference_code=transaction['reference_code'])
        req_agreement = api_manager.get_request(url_agreement, {'mode': mode})
        transaction['agreements'] = req_agreement.json()
    except ValueError:
        transaction = {}
    return transaction


def submit_transaction(user_id, resource):
    url = constants.USER_TRANSACTIONS.format(user_id=user_id)
    req = api_manager.post_request(url, resource)
    return req


def cancel_transaction(user_id, transaction_id):
    url = constants.USER_TRANSACTION_DETAIL.format(
        user_id=user_id,
        transaction_id=transaction_id)
    req = api_manager.delete_request(url)
    return req


def accept_transaction(user_id, transaction_id):
    url = constants.USER_TRANSACTION_ACCEPT.format(
        user_id=user_id,
        transaction_id=transaction_id)
    req = api_manager.put_request(url)
    return req

def reject_transaction(user_id, transaction_id):
    url = constants.USER_TRANSACTION_REJECT.format(
        user_id=user_id,
        transaction_id=transaction_id)
    req = api_manager.post_request(url)
    return req

def complete_transaction(user_id, transaction_id):
    url = constants.USER_TRANSACTION_COMPLETE.format(
        user_id=user_id,
        transaction_id=transaction_id)
    req = api_manager.post_request(url)
    return req

def rate_transaction(user_id, transaction_id, rating, message):
    params = {
        'message': message,
        'rate': rating
    }
    url = constants.USER_TRANSACTION_RATE.format(user_id=user_id,
                                                 transaction_id=transaction_id)
    req = api_manager.post_request(url, data=params)
    return req

def get_resource_agreement(reference_code):
    url = constants.GET_RESOURCE_AGREEMENT.format(
        reference_code=reference_code)
    req = api_manager.get_request(url)
    return req

def save_seller_resource_agreement(agreement):
    url = constants.SELLER_RESOURCE_AGREEMENT
    req = api_manager.post_request(url, agreement)
    return req

def save_buyer_resource_agreement_accept(agreement):
    url = constants.BUYER_RESOURCE_AGREEMENT_ACCEPT
    req = api_manager.put_request(url, agreement)
    return req

def edit_agreement(agreement):
    url = constants.SELLER_RESOURCE_AGREEMENT
    req = api_manager.put_request(url, agreement)
    return req
