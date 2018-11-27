# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, session
import services
from flask_login import current_user
from app.src.users import services as user_service
# from app.src.users.transactions import services as transaction_services
FaqBP = Blueprint('FaqBP', __name__)


# FAQS Page
@FaqBP.route('/faqs/', methods=['GET'])
def faq_page():
    sPage = 'faqs'
    if request.method == 'GET':
        faqs = services.get_faqs()
        if current_user.is_authenticated:
            wishlists = user_service.get_wishlists(mode='unarchived')
            basic_auth = session['user_basic']
            count_auth = user_service.get_count_auth(basic_auth)
            message_count = count_auth['message_count']
            transaction_count = count_auth['pending_transaction_count']
            return render_template('faqs/index.html',
                                   faqs=faqs,
                                   message_count=message_count,
                                   transaction_count=transaction_count,
                                   wishlists=wishlists,
                                   sPage=sPage)
        else:
            return render_template("faqs/index.html", faqs=faqs,
                                   sPage=sPage)


# View FAQ Detail
@FaqBP.route('/faqs/<int:faq_id>', methods=['GET'])
def view_faq_page(faq_id):
    if request.method == 'GET':
        faq = services.view_faq(faq_id)
        if current_user.is_authenticated:
            wishlists = user_service.get_wishlists(mode='unarchived')
            basic_auth = session['user_basic']
            count_auth = user_service.get_count_auth(basic_auth)
            message_count = count_auth['message_count']
            transaction_count = count_auth['pending_transaction_count']
            return render_template('faqs/index.html',
                                   faq=faq,
                                   message_count=message_count,
                                   transaction_count=transaction_count,
                                   wishlists=wishlists)
        else:
            return render_template("faqs/index.html", faq=faq)


# Questions Page
@FaqBP.route('/faqs/<int:faq_id>/questions', methods=['GET'])
def question_page(faq_id):
    sPage = 'faqs'
    if request.method == 'GET':
        questions = services.get_questions(faq_id)
        faqs = services.get_faqs()
        faq = services.view_faq(faq_id)
        if current_user.is_authenticated:
            wishlists = user_service.get_wishlists(mode='unarchived')
            basic_auth = session['user_basic']
            count_auth = user_service.get_count_auth(basic_auth)
            message_count = count_auth['message_count']
            transaction_count = count_auth['pending_transaction_count']
            return render_template('faqs/index.html',
                                   faq=faq, faqs=faqs,
                                   questions=questions,
                                   message_count=message_count,
                                   transaction_count=transaction_count,
                                   wishlists=wishlists,
                                   sPage=sPage)
        else:
            return render_template("faqs/index.html",
                                   faq=faq, faqs=faqs,
                                   questions=questions,
                                   sPage=sPage)


# # View Questions by FAQ Category
# @FaqBP.route('/faqs/<int:faq_id>/view-questions/<int:question_id>',
#       methods=['GET'])
# def view_question_page(faq_id, question_id):
#     if request.method == 'GET':
#         question = services.view_questions(faq_id, question_id)
#         faq = services.view_faq(faq_id)
#         return redirect(url_for('faq_page', faq=faq, question=question))


# Getting Started
# FAQS Page
@FaqBP.route('/getting-started', methods=['GET'])
def getting_started_page():
    if current_user.is_authenticated:
        wishlists = user_service.get_wishlists(mode='unarchived')
        basic_auth = session['user_basic']
        count_auth = user_service.get_count_auth(basic_auth)
        message_count = count_auth['message_count']
        transaction_count = count_auth['pending_transaction_count']
        return render_template("faqs/getting_started.html",
                               wishlists=wishlists,
                               message_count=message_count,
                               transaction_count=transaction_count)
    else:
        return render_template("faqs/getting_started.html")
