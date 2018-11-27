# -*- coding: utf-8 -*-

from flask import (Blueprint, flash, render_template, request,
                   redirect, url_for, session)
from flask_login import login_required, current_user
from app.src.users.supports.forms import SupportForm, SupportChatForm
from app.src.users.supports import services
from app.src.utils import helpers
from app.src.users import services as user_services
# from app.src.users.transactions import services as transaction_service
from flask import jsonify

UserSupportBP = Blueprint('UserSupportBP', __name__)


# Raise Support Request Page
@UserSupportBP.route('/support-request', methods=['GET', 'POST'])
@login_required
def support_page():
    support_form = SupportForm()
    uid = current_user.id
    basic_auth = session['user_basic']
    count_auth = user_services.get_count_auth(basic_auth)
    message_count = count_auth['message_count']
    transaction_count = count_auth['pending_transaction_count']
    if request.method == 'GET':
        return render_template('users/support.html',
                               support_form=support_form,
                               message_count=message_count,
                               transaction_count=transaction_count)
    elif request.method == 'POST':
        if support_form.validate_on_submit():
            sanitized_inputs = helpers.sanitize(request.form)
            subject = sanitized_inputs['subject']
            message = sanitized_inputs['message']
            raise_support = services.raise_support(uid, subject, message)
            print raise_support
            if raise_support.status_code == 201:
                flash('Issue has been raised to the Support Team', 'success')
                return redirect(url_for('.support_page'))

            else:
                flash('Error in raising support request', 'danger')
                return render_template('users/support.html',
                                       support_form=support_form,
                                       message_count=message_count,
                                       transaction_count=transaction_count)
        else:
            return render_template('users/support.html',
                                   support_form=support_form,
                                   message_count=message_count,
                                   transaction_count=transaction_count)


@UserSupportBP.route('/support-request/pending', methods=['GET', 'POST'])
@login_required
def pending_support_page():
    uid = current_user.id
    tickets = services.get_tickets(uid, mode='all')
    basic_auth = session['user_basic']
    count_auth = user_services.get_count_auth(basic_auth)
    message_count = count_auth['message_count']
    transaction_count = count_auth['pending_transaction_count']
    if request.method == 'GET':
        return render_template('users/support_pending.html',
                               message_count=message_count,
                               transaction_count=transaction_count,
                               tickets=tickets)


@UserSupportBP.route('/support-request/<int:support_id>',
                     methods=['GET', 'POST'])
@login_required
def message_support_page(support_id):
    uid = current_user.id
    tickets = services.get_tickets(uid, mode='all')
    support_form = SupportForm()
    basic_auth = session['user_basic']
    count_auth = user_services.get_count_auth(basic_auth)
    message_count = count_auth['message_count']
    transaction_count = count_auth['pending_transaction_count']
    if request.method == 'GET':
        return render_template('users/support_chat_message.html',
                               message_count=message_count,
                               transaction_count=transaction_count,
                               tickets=tickets,
                               msg_threads=tickets,
                               support_form=support_form)


@UserSupportBP.route('/support-request/completed', methods=['GET', 'POST'])
@login_required
def completed_support_page():
    uid = current_user.id
    tickets = services.get_tickets(uid, mode='all')
    basic_auth = session['user_basic']
    count_auth = user_services.get_count_auth(basic_auth)
    message_count = count_auth['message_count']
    transaction_count = count_auth['pending_transaction_count']
    if request.method == 'GET':
        return render_template('users/support_completed.html',
                               message_count=message_count,
                               transaction_count=transaction_count,
                               tickets=tickets)


@UserSupportBP.route('/support-tickets', methods=['GET', 'POST'])
@login_required
def support_ticket_page():
    uid = current_user.id
    tickets = services.get_tickets(uid, mode='all')
    basic_auth = session['user_basic']
    count_auth = user_services.get_count_auth(basic_auth)
    message_count = count_auth['message_count']
    transaction_count = count_auth['pending_transaction_count']
    if request.method == 'GET':
        return render_template('users/tickets.html',
                               message_count=message_count,
                               transaction_count=transaction_count,
                               tickets=tickets)


@UserSupportBP.route('/client/supportrequests', methods=['GET', 'POST'])
@login_required
def client_supportrequests_page():
    chats = user_services.support_chat_messages(current_user.id)
    if request.method == 'POST':
        support_form = SupportForm()
        if support_form.validate_on_submit():
            sanitized_inputs = helpers.sanitize(request.form)
            tickets = {
                'subject': sanitized_inputs['subject'],
                'message': sanitized_inputs['message'],
                'user_id': current_user.id
            }
            user_services.client_support_request_create(tickets)
    return jsonify(chats.json())


@UserSupportBP.route('/client/supportrequests/<string:reference_code>',
                     methods=['GET', 'POST'])
@login_required
def client_supportrequests_profile_page(reference_code):
    get_profile = user_services.support_requests_profile(reference_code)
    if request.method == 'POST':
        support_form = SupportChatForm()
        if support_form.validate_on_submit():
            sanitized_inputs = helpers.sanitize(request.form)
            conversation = {
                'reference_code': reference_code,
                'message': sanitized_inputs['message'],
                'sender_id': current_user.id,
                'sender_type': "Client"
            }
            user_services.client_support_conversations(conversation)
            get_profile = user_services.support_requests_profile(
                reference_code)
    return jsonify(get_profile.json())
