# -*- coding: utf-8 -*-

from datetime import datetime
import base64
from flask import session
from flask_login import login_user
import dateutil.parser
import dao
from app.src.utils import api_manager
from app.src.utils import constants
from models import User
from captcha.image import ImageCaptcha
from app.src.utils.captcha_audio import AudioCaptcha


def get(user_id):
    user = dao.get(user_id)
    return user


def get_count():
    url = constants.COUNT_EXEC
    req = api_manager.get_request_no_auth(url)
    return req.json()


def get_count_auth(basic_auth):
    url = constants.COUNT_EXEC
    req = api_manager.get_request(url)
    return req.json()


def register(first_name, last_name, email, password, is_subscribed,
             company_name, business_reg_number):
    user = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'password': password,
        'is_subscribed': is_subscribed,
        'company_name': company_name,
        'business_reg_number': business_reg_number
    }
    req = api_manager.post_request_no_auth(constants.USER_REGISTER, user)
    return req


def signup(first_name, last_name, email, password,
           company_name, business_reg_number):
    user = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'password': password,
        'company_name': company_name,
        'business_reg_number': business_reg_number
    }
    req = api_manager.post_request_no_auth(constants.USER_REGISTER, user)
    return req


def login(email, password):
    b64_userpass = base64.b64encode('{}:{}'.format(email, password))
    basic_auth = 'Basic {}'.format(b64_userpass)
    user_creds = {
        'email': email,
        'password': password
    }
    user = None
    req = api_manager.post_request_no_auth(constants.USER_LOGIN, user_creds)
    if req.status_code == 200:
        try:
            user_json = req.json()
            user = User(user_json)
            if 'PIONEER' in list(user_json['roles']):
                session['is_company_admin'] = True
            else:
                session['is_company_admin'] = False
            session['user_basic'] = basic_auth
            login_user(user)
        except ValueError:
            return req

    else:
        return req

    if dao.get(user.id) is None:
        dao.add(user)
    else:
        dao.update(user)
    return req


def logout(user_id):
    user = dao.get(user_id)
    if user is None:
        dao.add(user)
    else:
        dao.update(user)
    session.pop('user_basic', None)
    session.pop('current_url', None)


def get_profile(user_id):
    url = constants.USERS_ONE.format(user_id=user_id)
    req = api_manager.get_request(url)
    try:
        user = req.json()
        user['created_date'] = dateutil.parser.parse(user['created_date'])
    except ValueError:
        user = {}
    return user


def update_profile(user_id, first_name, last_name,
                   designation, description, mobile_number,
                   landline_number, is_subscribed,
                   subscribed, image_url, ):
    description.encode('utf-8')
    user = {
        # 'email': email,
        'first_name': first_name,
        'last_name': last_name,
        'designation': designation,
        'description': description,
        'mobile_number': mobile_number,
        'landline_number': landline_number,
        'is_subscribed': is_subscribed,
        'subscribed': subscribed,
        'image_url': image_url
    }
    # if birth_date:
    #     birth_date = datetime.strptime(birth_date, '%d-%m-%Y')
    #     format_bday = birth_date.date().strftime('%Y-%m-%d')
    #     user['birth_date'] = format_bday
    # else:
    #     user['birth_date'] = birth_date
    # user['description'].encode('utf-8')
    # print user['description']
    url = constants.USERS_ONE.format(user_id=user_id)
    req = api_manager.put_request(url, user)
    if req.status_code == 202:
        user = get_profile(user_id)
        user = User(user)
        login_user(user)
    else:
        return req
    if dao.get(user.id) is None:
        dao.add(user)
    else:
        dao.update(user)
    return req


def get_company(company_id):
    url = constants.COMPANY_ONE.format(company_id=company_id)
    req = api_manager.get_request(url)
    company_detail = None
    if req.status_code == 200:
        try:
            company_detail = req.json()
            company_detail['created_date'] = dateutil.parser.parse(
                company_detail['created_date'])
        except ValueError:
            company_detail = {}
    return company_detail


def get_industry():
    url = constants.COMPANY_INDUSTRY
    req = api_manager.get_request(url)
    company_industry = []
    if req.status_code == 200:
        try:
            company_industry = req.json()
        except ValueError:
            company_industry = []
    return company_industry


def update_company(company_id, name, company_info, office_number,
                   website, facebook, linkedin, unit_number,
                   block_street, postal_code, company_industry,
                   company_size, company_revenue,
                   years_of_incorporation, iso, bizsafe,
                   bca, image_url):
    company = {
        'name': name,
        'company_info': company_info,
        'office_number': office_number,
        'website': website,
        'facebook': facebook,
        'linkedin': linkedin,
        'address': [
            {
                'unit_number': unit_number,
                'block_street': block_street,
                'postal_code': postal_code,
            }
        ],
        'primary_industry': company_industry,
        'company_size': company_size,
        'company_revenue': company_revenue,
        'years_of_incorporation': years_of_incorporation,
        'iso': iso,
        'bizsafe': bizsafe,
        'bca': bca,
        'image_url': image_url
    }
    url = constants.COMPANY_ONE.format(company_id=company_id)
    req = api_manager.put_request(url, company)
    return req


def add_company(name, company_info, business_reg_number, office_number,
                mobile_number, block_street, unit_number, postal_code):
    company = {
        'name': name,
        'company_info': company_info,
        'business_reg_number': business_reg_number,
        'office_number': office_number,
        'mobile_number': mobile_number,
        'address':
            {
                'block_street': block_street,
                'unit_number': unit_number,
                'postal_code': postal_code,
                'latitude': 1,
                'longitude': 2,
            }
    }
    url = constants.COMPANY_REGISTER
    req = api_manager.post_request(url, company)
    return req


def change_password(user_id, old_password, new_password, confirm_password,
                    email):
    user_creds = {
        'old_password': old_password,
        'password': new_password,
        'confirm_password': confirm_password
    }
    url = constants.USER_PASSWORD.format(user_id=user_id)
    req = api_manager.put_request(url, user_creds)
    if req.status_code == 202:
        b64_userpass = base64.b64encode('{}:{}'.format(email, new_password))
        basic_auth = 'Basic {}'.format(b64_userpass)
        session['user_basic'] = basic_auth
    return req


def forgot_password(email):
    user_creds = {
        'email': email
    }
    req = api_manager.post_request_no_auth(constants.USER_FORGOT_PASSWORD,
                                           user_creds)
    return req


def resend_email(email):
    user_creds = {'email': email}
    req = api_manager.post_request_no_auth(constants.USER_RESEND_EMAIL,
                                           user_creds)
    return req


def reset_password(email, token, password, confirm_password):
    user_creds = {
        'email': email,
        'token': token,
        'password': password,
        'confirm_password': confirm_password
    }
    req = api_manager.post_request_no_auth(constants.USER_RESET_PASSWORD,
                                           user_creds)
    return req


def activate(code, aid):
    data = {
        'code': code,
        'aid': aid
    }
    req = api_manager.get_request_no_auth(constants.USER_ACTIVATE,
                                          data=data)
    return req


def get_favorites(user_id, mode='unarchived'):
    params = {'mode': mode}
    url = constants.USER_FAVORITE.format(user_id=user_id)
    req = api_manager.get_request(url, params)
    try:
        resources = req.json()
        if resources is not None:
            for resource in resources:
                resource['created_date'] = dateutil.parser.parse(
                    resource['created_date'])
                resource['price'] = ('%.2f' % resource['price'])
    except ValueError:
        resources = []
    return resources


def mark_favorite(user_id, resource_id):
    url = constants.RESOURCE_FAVORITE.format(resource_id=resource_id)
    params = {'account_id': user_id}
    req = api_manager.post_request(url, params)
    return req.text


def get_resources(user_id, min_price=None, max_price=None, sort=None,
                  mode='unarchived'):
    params = {}
    params['mode'] = mode
    if min_price:
        params['min_price'] = min_price
    if max_price:
        params['max_price'] = max_price
    if sort:
        params['sort'] = sort
    url = constants.USER_RESOURCE_ALL.format(user_id=user_id)
    req = api_manager.get_request(url, params)
    try:
        resources = req.json()
        for resource in resources:
            resource['created_date'] = dateutil.parser.parse(
                resource['created_date'])
            resource['price'] = ('%.2f' % resource['price'])
    except ValueError:
        resources = []
    return resources


def get_archived_resources(user_id, min_price=None, max_price=None, sort=None,
                           mode='archived'):
    params = {}
    params['mode'] = mode
    if min_price:
        params['min_price'] = min_price
    if max_price:
        params['max_price'] = max_price
    if sort:
        params['sort'] = sort
    url = constants.USER_RESOURCE_ALL.format(user_id=user_id)
    req = api_manager.get_request(url, params)
    try:
        resources = req.json()
        for resource in resources:
            resource['created_date'] = dateutil.parser.parse(
                resource['created_date'])
            resource['price'] = ('%.2f' % resource['price'])
    except ValueError:
        resources = []
    return resources


def get_transactions(user_id, mode='archived'):
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


def rate_transaction(user_id, transaction_id, rating):
    url = constants.USER_TRANSACTION_RATE.format(user_id=user_id,
                                                 transaction_id=transaction_id)
    req = api_manager.post_request(url, rating)
    return req


def generate_captcha(random_string):
    captcha = {}
    image = ImageCaptcha()
    audio = AudioCaptcha(voicedir=constants.AUDIO_CAPTCHA_DIR)

    # Image
    data = image.generate(random_string)
    image_format = 'data:image/png;base64,'
    base64_captcha = image_format + base64.b64encode(data.getvalue())

    # Audio
    data_audio = audio.generate(random_string)
    audio_format = 'data:audio/wav;base64,'
    base64_audio = audio_format + base64.b64encode(data_audio)

    captcha['image'] = base64_captcha
    captcha['audio'] = base64_audio
    return captcha


def get_user_messages(user_id, mode='unarchived'):
    params = {'mode': mode}
    url = constants.USER_MESSAGES.format(user_id=user_id)
    req = api_manager.get_request(url, params)
    try:
        messages = req.json()
        for message in messages:
            message['date_created'] = dateutil.parser.parse(message['date_created'])
            if message.has_key('last_message'):
                message['last_message']['date_created'] = dateutil.parser.parse(
                    message['last_message']['date_created'])
            formatted_price = ('%.2f' % message['resource']['price'])
            message['resource']['price'] = formatted_price
    except ValueError:
        messages = []
    return messages


def get_user_message(user_id, message_id):
    url = constants.USER_MESSAGE_THREAD.format(user_id=user_id,
                                               message_id=message_id)
    req = api_manager.get_request(url)
    try:
        message_thread = req.json()
        for message in message_thread:
            message['date_created'] = dateutil.parser.parse(
                message['date_created'])
    except ValueError:
        message_thread = []
    return message_thread


def send_reply_message(user_id, message_id, message_reply):
    url = constants.USER_MESSAGE_REPLY.format(user_id=user_id,
                                              message_id=message_id)
    req = api_manager.post_request(url, message_reply)

    return req


def send_new_message(user_id, message_reply):
    url = constants.USER_MESSAGES.format(user_id=user_id)
    req = api_manager.post_request(url, message_reply)
    return req


def get_wishlists(mode='unarchived'):
    params = {'mode': mode}
    url = constants.WISHLIST_NEW
    req = api_manager.get_request(url, params)
    try:
        wishlists = req.json()
        # for wishlist in wishlists:
        #     print 'hello'
        #     print wishlist
    except ValueError:
        wishlists = []
    return wishlists


def get_user_wishlists(user_id, mode='unarchived'):
    params = {'mode': mode}
    url = constants.USER_WISHLIST_ALL.format(user_id=user_id)
    req = api_manager.get_request(url, params)
    try:
        wishlists = req.json()
        for wishlist in wishlists:
            wishlist['created_date'] = dateutil.parser.parse(
                wishlist['created_date'])
    except ValueError:
        wishlists = []
    return wishlists


def get_archive_wishlists(user_id, mode='archived'):
    params = {'mode': mode}
    url = constants.USER_WISHLIST_ALL.format(user_id=user_id)
    req = api_manager.get_request(url, params)
    try:
        wishlists = req.json()
        for wishlist in wishlists:
            wishlist['created_date'] = dateutil.parser.parse(
                wishlist['created_date'])
    except ValueError:
        wishlists = []
    return wishlists


def archive_threads(user_id, message_id):
    url = constants.USER_MESSAGE_THREAD.format(user_id=user_id,
                                               message_id=message_id)
    req = api_manager.delete_request(url)
    return req


def archived_user_messages(user_id, mode='archived'):
    params = {'mode': mode}
    url = constants.USER_MESSAGES.format(user_id=user_id)
    req = api_manager.get_request(url, params)
    try:
        messages = req.json()
        for message in messages:
            message['date_created'] = dateutil.parser.parse(message['date_created'])
            if message.has_key('last_message'):
                message['last_message']['date_created'] = dateutil.parser.parse(
                    message['last_message']['date_created'])
            formatted_price = ('%.2f' % message['resource']['price'])
            message['resource']['price'] = formatted_price
    except ValueError:
        messages = []
    return messages


def support_chat_messages(user_id):
    url = constants.CLIENT_SUPPORT_REQUEST.format(user_id=user_id)
    req = api_manager.get_request(url)
    return req


def client_support_request_create(tickets):
    url = constants.CLIENT_SUPPORT_REQUEST_CREATE
    req = api_manager.post_request(url, tickets)
    return req


def support_requests_profile(reference_code):
    url = constants.CLIENT_SUPPORT_REQUEST_PROFILE.format(
        reference_code=reference_code)
    req = api_manager.get_request(url)
    return req


def client_support_conversations(conversations):
    url = constants.CLIENT_SUPPORT_CONVERSATION
    req = api_manager.post_request(url, conversations)
    return req


def unsubsribe_email(type_id):
    url = constants.USER_UNSUBSCRIBE_EMAIL.format(type_id=0)
    req = api_manager.get_request(url)
    return req


def unsubsribe_newsletter(type_id):
    url = constants.USER_UNSUBSCRIBE_NEWSLETTER.format(type_id=1)
    req = api_manager.get_request(url)
    return req
