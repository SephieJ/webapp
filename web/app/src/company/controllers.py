# -*- coding: utf-8 -*-

from flask import (Blueprint, render_template, request,
                   flash, redirect, url_for, session)
from flask_login import current_user
from app.src.users import services as user_service
# from app.src.users.transactions import services as transaction_services
import services
from app.src.utils import helpers
from app.src.company.forms import ContactForm

CompanyBP = Blueprint('CompanyBP', __name__)


# About Us Page
@CompanyBP.route('/about-us', methods=['GET'])
def about_us_page():
    sPage = 'about-us'
    cPage = 'contact-us'
    if request.method == 'GET':
        if current_user.is_authenticated:
            wishlists = user_service.get_wishlists(mode='unarchived')
            basic_auth = session['user_basic']
            count_auth = user_service.get_count_auth(basic_auth)
            message_count = count_auth['message_count']
            transaction_count = count_auth['pending_transaction_count']
            return render_template("company/about-us.html",
                                   message_count=message_count,
                                   transaction_count=transaction_count,
                                   wishlists=wishlists,
                                   sPage=sPage, cPage=cPage
                                   )
        else:
            return render_template("company/about-us.html", sPage=sPage,
                                   cPage=cPage)


# Terms & Conditions Page
@CompanyBP.route('/private-policy-and-terms-of-use', methods=['GET'])
def policies_page():
    if request.method == 'GET':
        return render_template("company/terms.html")


# Contest Page
@CompanyBP.route('/contest', methods=['GET'])
def contest_page():
    if request.method == 'GET':
        return render_template("company/contest.html")


# Contact Us Page
@CompanyBP.route('/contact-us', methods=['GET', 'POST'])
def contact_us_page():
    sPage = 'contact-us'
    contact_form = ContactForm()
    if request.method == 'GET':
        if current_user.is_authenticated:
            wishlists = user_service.get_wishlists(mode='unarchived')
            basic_auth = session['user_basic']
            count_auth = user_service.get_count_auth(basic_auth)
            message_count = count_auth['message_count']
            transaction_count = count_auth['pending_transaction_count']
            return render_template("company/contact-us.html",
                                   message_count=message_count,
                                   transaction_count=transaction_count,
                                   wishlists=wishlists,
                                   sPage=sPage, contact_form=contact_form)
        else:
            return render_template("company/contact-us.html",
                                   sPage=sPage, contact_form=contact_form)
    elif request.method == 'POST':
        if contact_form.validate_on_submit():
            sanitize_inputs = helpers.sanitize(request.form)
            name = sanitize_inputs['name']
            email = sanitize_inputs['email']
            message = sanitize_inputs['message']

            send_message = services.send_inquiry(name, email, message)
            print send_message.status_code

            if send_message.status_code == 202:
                flash('Message inquiry has been successfully sent.',
                      'success')
            else:
                flash('Error in sending message. Please try again.',
                      'danger')
            return redirect(url_for('.contact_us_page'))
        else:
            return redirect(url_for('.contact_us_page'))


# Company Details Page
@CompanyBP.route('/company-details/<int:company_id>', methods=['GET'])
def view_company_page(company_id):
    if request.method == 'GET':
        if current_user.is_authenticated:
            wishlists = user_service.get_wishlists(mode='unarchived')
            basic_auth = session['user_basic']
            count_auth = user_service.get_count_auth(basic_auth)
            message_count = count_auth['message_count']
            transaction_count = count_auth['pending_transaction_count']
            company = services.get_company(company_id)
            members = services.company_members(company_id)
            return render_template("company/index.html",
                                   message_count=message_count,
                                   transaction_count=transaction_count,
                                   wishlists=wishlists,
                                   company=company, members=members)
        else:
            return render_template("company/index.html",
                                   company=company)
