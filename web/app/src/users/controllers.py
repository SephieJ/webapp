# -*- coding: utf-8 -*-

from flask import (Blueprint, flash, redirect, render_template,
                   request, url_for, session, jsonify, json)
from flask_login import login_required, logout_user, current_user
from forms import (LoginForm, ChangePasswordForm, UserProfileForm,
                   RegisterForm, ForgotPasswordForm, ResetPasswordForm,
                   CompanyProfileForm, MessageForm, SignupForm,
                   ResendEmailForm)
from app.src.resources.forms import WishlistForm
import services
import random, HTMLParser
from app.src.resources import services as resource_services
# from app.src.users.transactions import services as transaction_services
from app.src.utils import helpers
from app.src.utils.pagination import Pagination
from app.src.utils.constants import PER_PAGE, PAGES, ONE_MAP_URL
import time

UserBP = Blueprint('UserBP', __name__)


# Home page
@UserBP.route('/', methods=['GET'])
def home_page():
    if request.method == 'GET':
        session['selected_category'] = None
        session['selected_subcategory'] = None
        sorting = ''
        sort = request.args.get('sort')
        min_price = request.args.get('min_price')
        max_price = request.args.get('max_price')
        page = request.args.get('page')
        

        count_exec = services.get_count()

        count_resource = count_exec['resources_count']

        if page is None:
            page = 1
        else:
            page = int(page)
        if sort:
            sorting = sort
            if min_price or max_price:
                resources = resource_services.get_paginated_resources(
                    offset=(page * 15 - 15),
                    sort=sort,
                    min_price=min_price,
                    max_price=max_price)
            else:
                resources = resource_services.get_paginated_resources(
                    offset=(page * 15 - 15), sort=sort)

        else:

            resources = resource_services.get_paginated_resources(
                offset=(page * 15 - 15))

        pagination = Pagination(page, PER_PAGE, count_resource)
        resources = pagination.paginate_limited(resources)
        # return jsonify(resources)
        if current_user.is_authenticated:
            # s = time.time()
            basic_auth = session['user_basic']
            count_auth = services.get_count_auth(basic_auth)
            message_count = count_auth['message_count']
            transaction_count = count_auth['pending_transaction_count']

            wishlists = services.get_wishlists(mode='unarchived')
            # e = time.time()
            # print(e - s)
            return render_template('home.html',
                                   resources=resources,
                                   sorting=sorting,
                                   min_price=min_price,
                                   max_price=max_price,
                                   count_resource=count_resource,
                                   page=page,
                                   pagination=pagination,
                                   wishlists=wishlists,
                                   message_count=message_count,
                                   transaction_count=transaction_count)
        else:
            return render_template('home.html',
                                   resources=resources,
                                   sorting=sorting,
                                   min_price=min_price,
                                   max_price=max_price,
                                   count_resource=count_resource,
                                   page=page,
                                   pagination=pagination)


# AJAX Home Page
@UserBP.route('/homepage', methods=['GET'])
def ajax_homepage():
    session['selected_category'] = None
    session['selected_subcategory'] = None
    sorting = ''
    sort = request.args.get('sort')
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')
    page = request.args.get('page')

    count_exec = services.get_count()

    count_resource = count_exec['resources_count']

    if page is None:
        page = 1
    else:
        page = int(page)
    if sort:
        sorting = sort
        if min_price or max_price:
            resources = resource_services.get_paginated_resources(
                offset=(page * 15 - 15),
                sort=sort,
                min_price=min_price,
                max_price=max_price)
        else:
            resources = resource_services.get_paginated_resources(
                offset=(page * 15 - 15), sort=sort)

    else:

        # resources = resource_services.get_paginated_resources(
        #     offset=(page * 15 - 15))
        resources = list(map(lambda resource: {
            "name": str(resource['name']),
            "price": float(resource['price']),
            "reference": url_for('ResourceBP.resource_page',
                                 slug=resource['reference']),
            "rate": str(resource['resource_rate']),
            "image_url": resource['image_url']
        }, resource_services.get_paginated_resources(offset=(page * 15 - 15))))

    pagination = Pagination(page, PER_PAGE, count_resource)
    resources = pagination.paginate_limited(resources)
    return jsonify(resources)
    return pagination, sorting, page, min_price, max_price


# Register
@UserBP.route('/register', methods=['GET', 'POST'])
def register_page():
    sPage = 'register'
    register_form = RegisterForm()
    if request.method == 'GET':
        captcha_string = helpers.generate_random_chars(4)
        session['captcha_string'] = captcha_string
        captcha = services.generate_captcha(captcha_string)
        if current_user.is_authenticated:
            return redirect(url_for('.home_page'))
        else:
            return render_template('users/register.html',
                                   register_form=register_form,
                                   captcha=captcha['image'],
                                   audio_captcha=captcha['audio'],
                                   sPage=sPage)
    elif request.method == 'POST':
        captcha_string = helpers.generate_random_chars(4)
        captcha = services.generate_captcha(captcha_string)
        if register_form.validate_on_submit():
            sanitized_inputs = helpers.sanitize(request.form)
            first_name = sanitized_inputs['first_name']
            last_name = sanitized_inputs['last_name']
            email = sanitized_inputs['email']
            password = sanitized_inputs['password']
            captcha_text = sanitized_inputs['captcha_text']
            company_name = sanitized_inputs['company_name']
            business_reg_number = sanitized_inputs['business_reg_number']
            is_subscribed = register_form.is_subscribed.data
            if captcha_text.upper() != session['captcha_string']:
                session['captcha_string'] = captcha_string
                print captcha_string
                flash('Captcha validation failed', 'danger')
                return render_template("users/register.html",
                                       register_form=register_form,
                                       captcha=captcha['image'],
                                       audio_captcha=captcha['audio'])
            req = services.register(first_name, last_name, email, password,
                                    is_subscribed, company_name,
                                    business_reg_number)
            print req
            if req.status_code == 201:
                flash('Registration Successful. Please check your email for \
                      the activation link and verify your account. \
                      Thank you for being part of the B2B \
                      resource sharing movement!',
                      'success')
                print 'helllo'
                return redirect(url_for('.register_page'))
            elif req.status_code == 409:
                register_form.captcha_text.data = ''
                session['captcha_string'] = captcha_string
                flash('Email address already been registered. \
                      Please check your spam/junk mail for the \
                      activation link.', 'danger')
                return render_template("users/register.html",
                                       register_form=register_form,
                                       captcha=captcha['image'],
                                       audio_captcha=captcha['audio'],
                                       sPage=sPage)
            else:
                register_form.captcha_text.data = ''
                session['captcha_string'] = captcha_string
                flash('Business Register Number does not exist.', 'danger')
                return render_template("users/register.html",
                                       register_form=register_form,
                                       captcha=captcha['image'],
                                       audio_captcha=captcha['audio'],
                                       sPage=sPage)
        else:
            register_form.captcha_text.data = ''
            session['captcha_string'] = captcha_string
            return render_template("users/register.html",
                                   register_form=register_form,
                                   captcha=captcha['image'],
                                   audio_captcha=captcha['audio'],
                                   sPage=sPage)


# Sign Up
@UserBP.route('/prelaunch', methods=['GET', 'POST'])
def signup_page():
    signup_form = SignupForm()
    if request.method == 'GET':
        return render_template('users/sign_up.html',
                               signup_form=signup_form)
    elif request.method == 'POST':
        if signup_form.validate_on_submit():
            sanitized_inputs = helpers.sanitize(request.form)
            first_name = sanitized_inputs['first_name']
            last_name = sanitized_inputs['last_name']
            email = sanitized_inputs['email']
            password = 'Pr3l@unch'
            company_name = sanitized_inputs['company_name']

            if not sanitized_inputs['business_reg_number']:
                business_reg_number = "012345ABCDE"
            else:
                business_reg_number = sanitized_inputs['business_reg_number']
            req = services.signup(first_name, last_name, email, password,
                                  company_name, business_reg_number)
            if req.status_code == 201:
                return render_template("users/success.html")
            else:
                flash('Email address has already been registered.', 'danger')
                return render_template("users/sign_up.html",
                                       signup_form=signup_form)
        else:
            return render_template("users/sign_up.html",
                                   signup_form=signup_form)


# Login Page
@UserBP.route('/login', methods=['GET', 'POST'])
def login_page():
    sPage = 'login'
    login_form = LoginForm()
    resend_email_form = ResendEmailForm()
    if request.method == 'GET':
        next_url = request.args.get('next')
        rid = request.args.get('rid')
        if current_user.is_authenticated:
            return redirect(url_for('.home_page'))
        else:
            return render_template('users/login.html', login_form=login_form,
                                   resend_email_form=resend_email_form,
                                   next=next_url, rid=rid, sPage=sPage)
    elif request.method == 'POST':
        next_url = request.form['next']
        if login_form.validate_on_submit():
            sanitized_inputs = helpers.sanitize(request.form)
            email = sanitized_inputs['email']
            password = sanitized_inputs['password']
            login = services.login(email, password)
            if login.status_code == 200:
                if next_url:
                    resource_id = request.form['rid']
                    if resource_id:
                        services.mark_favorite(current_user.id, resource_id)
                    return redirect(next_url)
                else:
                    return redirect(url_for('.home_page'))
            else:
                if 'unverified' in str(login.text).lower():
                    return render_template('users/login.html',
                                           login_form=login_form,
                                           resend_email_form=resend_email_form,
                                           sPage=sPage,
                                           email=email)
                else:
                    flash(login.text, 'danger')
                    return render_template('users/login.html',
                                           login_form=login_form,
                                           resend_email_form=resend_email_form,
                                           sPage=sPage)
        else:
            return render_template('users/login.html', login_form=login_form,
                                   resend_email_form=resend_email_form,
                                   sPage=sPage)


# Logout Page
@UserBP.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    services.logout(current_user.id)
    logout_user()
    return redirect(url_for('.home_page'))


# Profile Page
@UserBP.route('/<int:user_id>', methods=['GET'])
@login_required
def user_profile_page(user_id):
    user = services.get_profile(user_id)
    if current_user.id != user['id']:
        return render_template('error_pages/401.html')
    sorting = ''
    sort = request.args.get('sort')
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')

    page = request.args.get('page')

    if page is None:
        page = 1
    else:
        page = int(page)

    if sort:
        sorting = sort
        if min_price or max_price:
            resources = services.get_resources(user_id,
                                               sort=sort,
                                               min_price=min_price,
                                               max_price=max_price)
        else:
            resources = services.get_resources(user_id, sort=sort)

    else:
        resources = services.get_resources(user_id)

    count = len(resources)
    pagination = Pagination(page, PER_PAGE, count)
    resources = pagination.paginate(resources)

    basic_auth = session['user_basic']
    count_auth = services.get_count_auth(basic_auth)
    message_count = count_auth['message_count']
    transaction_count = count_auth['pending_transaction_count']

    return render_template('users/profile.html',
                           user=user,
                           resources=resources,
                           sorting=sorting,
                           min_price=min_price,
                           max_price=max_price,
                           page=page,
                           pagination=pagination,
                           message_count=message_count,
                           transaction_count=transaction_count)


# View Profile Page
@UserBP.route('/view-profile/<int:user_id>', methods=['GET'])
def view_profile_page(user_id):

    user = services.get_profile(user_id)
    sorting = ''
    sort = request.args.get('sort')
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')

    page = request.args.get('page')
    if page is None:
        page = 1
    else:
        page = int(page)

    if sort:
        sorting = sort
        if min_price or max_price:
            resources = services.get_resources(user_id,
                                               sort=sort,
                                               min_price=min_price,
                                               max_price=max_price)
        else:
            resources = services.get_resources(user_id, sort=sort)

    else:
        resources = services.get_resources(user_id)

    count = len(resources)
    pagination = Pagination(page, PER_PAGE, count)
    resources = pagination.paginate(resources)

    basic_auth = session['user_basic']
    count_auth = services.get_count_auth(basic_auth)
    message_count = count_auth['message_count']
    transaction_count = count_auth['pending_transaction_count']

    return render_template('users/view_profile.html',
                           user=user,
                           resources=resources,
                           sorting=sorting,
                           min_price=min_price,
                           max_price=max_price,
                           page=page,
                           pagination=pagination,
                           message_count=message_count,
                           transaction_count=transaction_count)


# User Company Page
@UserBP.route('/company/<int:company_id>', methods=['GET', 'POST'])
@login_required
def user_company_page(company_id):
    uid = current_user.id
    user = services.get_profile(uid)
    company_details = services.get_company(company_id)
    if 'PIONEER' not in user['roles']:
        return render_template('error_pages/401.html')
    if company_details['id'] != user['company']['id']:
        return render_template('error_pages/401.html')
    company_form = CompanyProfileForm()
    # count_transactions = transaction_services.get_transactions(
    #     uid, mode='unarchived')
    # data_transaction = []
    # status_transaction = 0

    # count_messages = services.get_user_messages(uid,
    #                                             mode='unarchived')
    # data_message = []
    # status_message = 0
    company_industries = sorted(services.get_industry(), key=lambda industry: industry['industry_name'])
    others = filter(lambda industry: industry['industry_name'] == 'Others', company_industries)
    company_industries = filter(lambda industry: industry['industry_name'] != 'Others', company_industries)
    company_industries.extend(others)

    # for transaction in count_transactions:
    #     if transaction['status'] == 'PENDING':
    #         status_transaction += 1
    #         data_transaction = status_transaction

    # for message_stat in count_messages:
    #     if message_stat['unread_message_count'] >= 1:
    #         status_message += 1
    #         data_message = status_message
    # company_form.company_industry.choices = [(i['id'], i['industry_name'])
    #                                          for i in company_industries]

    basic_auth = session['user_basic']
    count_auth = services.get_count_auth(basic_auth)
    message_count = count_auth['message_count']
    transaction_count = count_auth['pending_transaction_count']
    if request.method == 'GET':
        if company_details['company_info']:
            company_details['company_info'] = \
                HTMLParser.HTMLParser().unescape(
                    company_details['company_info'])
        company_form.company_info.data = company_details['company_info']
        company_form.company_size.data = company_details['company_size']
        company_form.company_revenue.data = company_details['company_revenue']
        company_form.company_years.data = \
            company_details['years_of_incorporation']

        if company_details['bca']:
            for bca in company_details['bca']:
                company_form.bca.data = bca
        else:
            company_form.bca.data = company_details['bca']

        if company_details['iso']:
            for iso in company_details['iso']:
                company_form.iso.data = iso
        else:
            company_form.iso.data = company_details['iso']

        company_form.bizsafe.data = company_details['bizsafe']
        return render_template('users/company_details.html',
                               company_form=company_form,
                               message_count=message_count,
                               transaction_count=transaction_count,
                               user=user, company_details=company_details,
                               company_industries=company_industries)
    elif request.method == 'POST':
        if company_form.is_submitted():
            sanitized_inputs = helpers.sanitize(request.form)
            name = sanitized_inputs['name']
            company_info = sanitized_inputs['company_info']
            office_number = sanitized_inputs['office_number']
            website = sanitized_inputs['website']
            facebook = sanitized_inputs['facebook']
            linkedin = sanitized_inputs['linkedin']
            unit_number = sanitized_inputs['unit_number']
            block_street = sanitized_inputs['block_street']
            postal_code = sanitized_inputs['postal_code']
            company_size = company_form.company_size.data
            company_revenue = company_form.company_revenue.data
            years_of_incorporation = company_form.company_years.data
            bizsafe = company_form.bizsafe.data
            image = request.files['image_url']

            company_industry = request.form.get('industrys')

            iso_arr = request.form.getlist('iso')
            iso = []
            for iso_val in iso_arr:
                iso_dict = {
                    'title': iso_val
                }
                iso.append(iso_dict)

            bca_arr = request.form.getlist('bca')
            bca = []
            for bca_val in bca_arr:
                bca_dict = {
                    'title': bca_val
                }
                bca.append(bca_dict)

            if image.filename is None:
                image_url = ''
            else:
                image_url = helpers.upload(image)

            update_company = services.update_company(
                company_id, name, company_info, office_number,
                website, facebook, linkedin, unit_number, block_street,
                postal_code, company_industry, company_size,
                company_revenue, years_of_incorporation,
                iso, bizsafe, bca, image_url)

            if update_company.status_code == 202:
                flash('Company successfully updated.;success', 'profile')
                return redirect(url_for('.user_company_page',
                                        company_id=company_id))
            else:
                flash('Error in updating profile.;danger',
                      'profile')
                return render_template('users/company_details.html',
                                       company_form=company_form,
                                       message_count=message_count,
                                       transaction_count=transaction_count,
                                       company_details=company_details,
                                       company_industries=company_industries)
        else:
            flash('Please fill up the required fields.;danger', 'profile')
            return render_template('users/company_details.html',
                                   company_form=company_form,
                                   user=user, company_details=company_details,
                                   message_count=message_count,
                                   transaction_count=transaction_count,
                                   company_industries=company_industries)


# View Company Page by Users
@UserBP.route('/company-view/<int:company_id>', methods=['GET'])
@login_required
def user_company_view(company_id):
    uid = current_user.id
    user = services.get_profile(uid)
    company_details = services.get_company(company_id)
    company_form = CompanyProfileForm()
    company_industries = services.get_industry()
    # company_form.company_industry.choices = [(i['id'], i['industry_name'])
    #                                          for i in company_industries]
    basic_auth = session['user_basic']
    count_auth = services.get_count_auth(basic_auth)
    message_count = count_auth['message_count']
    transaction_count = count_auth['pending_transaction_count']
    if request.method == 'GET':
        company_details['name'] = \
            HTMLParser.HTMLParser().unescape(company_details['name'])
        company_form.company_info.data = company_details['company_info']
        company_form.company_size.data = company_details['company_size']
        company_form.company_revenue.data = company_details['company_revenue']
        company_form.company_years.data = \
            company_details['years_of_incorporation']

        if company_details['bca']:
            for bca in company_details['bca']:
                company_form.bca.data = bca
        else:
            company_form.bca.data = company_details['bca']

        if company_details['iso']:
            for iso in company_details['iso']:
                company_form.iso.data = iso
        else:
            company_form.iso.data = company_details['iso']

        company_form.bizsafe.data = company_details['bizsafe']
        return render_template('users/company_view.html',
                               company_form=company_form,
                               message_count=message_count,
                               transaction_count=transaction_count,
                               user=user, company_details=company_details,
                               company_industries=company_industries)


# My Resource Page
@UserBP.route('/<int:user_id>/resources', methods=['GET'])
@login_required
def user_resources_page(user_id):
    user = services.get_profile(user_id)
    sorting = ''
    sort = request.args.get('sort')
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')

    if current_user.id != user_id:
        return render_template('error_pages/401.html')

    page = request.args.get('page')
    if page is None:
        page = 1
    else:
        page = int(page)

    if sort:
        sorting = sort
        if min_price or max_price:
            resources = services.get_resources(user_id,
                                               sort=sort,
                                               min_price=min_price,
                                               max_price=max_price)
        else:
            resources = services.get_resources(user_id, sort=sort)

    else:
        resources = services.get_resources(user_id)

    count = len(resources)
    pagination = Pagination(page, PER_PAGE, count)
    resources = pagination.paginate(resources)

    basic_auth = session['user_basic']
    count_auth = services.get_count_auth(basic_auth)
    message_count = count_auth['message_count']
    transaction_count = count_auth['pending_transaction_count']
    return render_template('users/my_resources.html',
                           user=user,
                           resources=resources,
                           sorting=sorting,
                           min_price=min_price,
                           max_price=max_price,
                           page=page,
                           pagination=pagination,
                           message_count=message_count,
                           transaction_count=transaction_count)


# My Wishlist Page
@UserBP.route('/<int:user_id>/wishlist', methods=['GET'])
@login_required
def user_wishlist_page(user_id):
    user = services.get_profile(user_id)
    wishlist_form = WishlistForm()
    page = request.args.get('page')
    if page is None:
        page = 1
    else:
        page = int(page)

    wishlists = services.get_user_wishlists(user_id)

    count = len(wishlists)
    pagination = Pagination(page, PER_PAGE, count)
    wishlists = pagination.paginate(wishlists)

    basic_auth = session['user_basic']
    count_auth = services.get_count_auth(basic_auth)
    message_count = count_auth['message_count']
    transaction_count = count_auth['pending_transaction_count']

    if current_user.id != user_id:
        return render_template('error_pages/401.html')
    return render_template('users/my_wishlist.html',
                           user=user,
                           wishlists=wishlists,
                           page=page,
                           pagination=pagination,
                           message_count=message_count,
                           transaction_count=transaction_count,
                           wishlist_form=wishlist_form)


# My Wishlist Page
@UserBP.route('/<int:user_id>/archived-wishlist', methods=['GET'])
@login_required
def archive_wishlist_page(user_id):
    user = services.get_profile(user_id)
    wishlist_form = WishlistForm()
    page = request.args.get('page')
    if page is None:
        page = 1
    else:
        page = int(page)

    wishlists = services.get_archive_wishlists(user_id)

    count = len(wishlists)
    pagination = Pagination(page, PER_PAGE, count)
    wishlists = pagination.paginate(wishlists)

    basic_auth = session['user_basic']
    count_auth = services.get_count_auth(basic_auth)
    message_count = count_auth['message_count']
    transaction_count = count_auth['pending_transaction_count']
    if current_user.id != user_id:
        return render_template('error_pages/401.html')
    return render_template('users/archived_wishlist.html',
                           user=user,
                           wishlists=wishlists,
                           page=page,
                           pagination=pagination,
                           message_count=message_count,
                           transaction_count=transaction_count,
                           wishlist_form=wishlist_form)


# My Archived Resource Page
@UserBP.route('/<int:user_id>/resources-archived', methods=['GET'])
def archive_resources_page(user_id):
    user = services.get_profile(user_id)
    sorting = ''
    sort = request.args.get('sort')
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')
    if current_user.id != user_id:
        return render_template('error_pages/401.html')
    page = request.args.get('page')
    if page is None:
        page = 1
    else:
        page = int(page)

    if sort:
        sorting = sort
        if min_price or max_price:
            resources = services.get_archived_resources(user_id,
                                                        sort=sort,
                                                        min_price=min_price,
                                                        max_price=max_price)
        else:
            resources = services.get_archived_resources(user_id, sort=sort)

    else:
        resources = services.get_archived_resources(user_id)

    count = len(resources)
    pagination = Pagination(page, PER_PAGE, count)
    resources = pagination.paginate(resources)

    basic_auth = session['user_basic']
    count_auth = services.get_count_auth(basic_auth)
    message_count = count_auth['message_count']
    transaction_count = count_auth['pending_transaction_count']
    return render_template('users/archived_resources.html',
                           user=user,
                           resources=resources,
                           sorting=sorting,
                           min_price=min_price,
                           max_price=max_price,
                           page=page,
                           pagination=pagination,
                           message_count=message_count,
                           transaction_count=transaction_count)


# Edit Profile Page
@UserBP.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def user_edit_profile():
    user_form = UserProfileForm()
    uid = current_user.id
    user = services.get_profile(uid)
    basic_auth = session['user_basic']
    count_auth = services.get_count_auth(basic_auth)
    message_count = count_auth['message_count']
    transaction_count = count_auth['pending_transaction_count']
    print user
    if request.method == 'GET':
        if user['description']:
            user['description'] = HTMLParser.HTMLParser().\
                unescape(user['description'])
        user_form.description.data = user['description']
        user_form.subscribe_email.data = user['is_subscribed']
        user_form.subscribe_newsletter.data = user['subscribed']
        return render_template('users/edit_profile.html',
                               user_form=user_form,
                               message_count=message_count, user=user,
                               transaction_count=transaction_count)
    elif request.method == 'POST':
        if user_form.is_submitted():

            sanitized_inputs = helpers.sanitize(request.form)
            # email = sanitized_inputs['email']
            first_name = sanitized_inputs['first_name']
            last_name = sanitized_inputs['last_name']
            description = sanitized_inputs['description']
            designation = sanitized_inputs['designation']
            # birth_date = sanitized_inputs['birth_date']
            mobile_number = sanitized_inputs['mobile_number']
            landline_number = sanitized_inputs['landline_number']
            image = request.files['image_url']

            # description = HTMLParser.HTMLParser().unescape(description)
            # encode_description = description.encode('utf-8')
            # print description

            is_subscribed = user_form.subscribe_email.data
            subscribed = user_form.subscribe_newsletter.data

            if image.filename is None:
                image_url = ''
            else:
                image_url = helpers.upload(image)

            update_profile = services.update_profile(
                current_user.id, first_name, last_name,
                designation, description,
                mobile_number, landline_number, is_subscribed,
                subscribed, image_url)
            # print update_profile

            if update_profile.status_code == 202:
                flash('Profile successfully updated.;success', 'profile')
                return redirect(url_for('.user_edit_profile',
                                        encode='utf-8'))
            else:
                flash('Error in updating profile.;danger', 'profile')
                return render_template(
                    'users/edit_profile.html',
                    user_form=user_form, message_count=message_count,
                    transaction_count=transaction_count, user=user)
        else:
            flash('Please fill up the required fields.;danger', 'profile')
            return render_template(
                'users/edit_profile.html',
                user_form=user_form, user=user,
                message_count=message_count,
                transaction_count=transaction_count)


# Change Password Page
@UserBP.route('/profile/change_password', methods=['GET', 'POST'])
@login_required
def user_change_password():
    change_password_form = ChangePasswordForm()
    basic_auth = session['user_basic']
    count_auth = services.get_count_auth(basic_auth)
    message_count = count_auth['message_count']
    transaction_count = count_auth['pending_transaction_count']
    if request.method == 'GET':
        return render_template('users/change_password.html',
                               change_password_form=change_password_form,
                               message_count=message_count,
                               transaction_count=transaction_count)
    elif request.method == 'POST':
        if change_password_form.validate_on_submit():
            sanitized_inputs = helpers.sanitize(request.form)
            old_password = sanitized_inputs['old_password']
            new_password = sanitized_inputs['new_password']
            confirm_password = sanitized_inputs['confirm_password']
            change_password = services.change_password(
                current_user.id, old_password, new_password,
                confirm_password,
                current_user.email)
            if change_password.status_code == 202:
                flash('Password successfully changed.;success', 'password')
                return redirect(url_for('.user_change_password'))
            else:
                flash('Error in changing password.;danger', 'password')
                return redirect(url_for('.user_change_password'))
        else:
            flash('Please fill up the required fields.;danger', 'password')
            return render_template(
                'users/change_password.html',
                change_password_form=change_password_form,
                message_count=message_count,
                transaction_count=transaction_count)


# View Favorite Resources
@UserBP.route('/bookmarks', methods=['GET', 'POST'])
@login_required
def view_bookmarks_page():
    session['selected_category'] = None
    session['selected_subcategory'] = None

    page = request.args.get('page')
    if page is None:
        page = 1
    else:
        page = int(page)

    favorites = [ favorite for favorite in services.get_favorites(current_user.id) if favorite.get('status') != "ARCHIVED" ]
    count = len(favorites)
    pagination = Pagination(page, PER_PAGE, count)
    favorites = pagination.paginate(favorites)

    wishlists = services.get_wishlists(mode='unarchived')

    basic_auth = session['user_basic']
    count_auth = services.get_count_auth(basic_auth)
    message_count = count_auth['message_count']
    transaction_count = count_auth['pending_transaction_count']

    return render_template('users/favorites.html',
                           favorites=favorites,
                           page=page,
                           pagination=pagination,
                           message_count=message_count,
                           transaction_count=transaction_count,
                           wishlists=wishlists)


# Forgot password
@UserBP.route('/password/forgot', methods=['GET', 'POST'])
def forgot_password():
    forgot_password_form = ForgotPasswordForm()
    if request.method == 'GET':
        return render_template('users/forgot_password.html',
                               forgot_password_form=forgot_password_form)
    elif request.method == 'POST':
        if forgot_password_form.validate_on_submit():
            sanitized_inputs = helpers.sanitize(request.form)
            email = sanitized_inputs['email']
            forgot_password = services.forgot_password(email)
            if forgot_password.status_code == 200:
                flash(forgot_password.text, 'success')
            else:
                flash(forgot_password.text, 'danger')
            return redirect(url_for('.forgot_password'))
        else:
            return render_template('users/forgot_password.html',
                                   forgot_password_form=forgot_password_form)


# @UserBP.route('/resend-email-verification', methods=['POST'])
# def resend_email():
#     sanitized_inputs = helpers.sanitize(request.form)
#     email = sanitized_inputs['email']
#     print email
#     resend_email = services.resend_email(email)
#     print resend_email
#     print resend_email.status_code
#     if resend_email.status_code == 202:
#         flash(resend_email.text, 'success')
#     else:
#         flash(resend_email.text, 'danger')
#     return redirect(url_for('.login_page'))

# Resend Email Verifcation
@UserBP.route('/resend-email-verification', methods=['GET', 'POST'])
def resend_email():
    resend_email_form = ResendEmailForm()
    if request.method == 'GET':
        return render_template('users/resend_email.html',
                               resend_email_form=resend_email_form)
    elif request.method == 'POST':
        if resend_email_form.validate_on_submit():
            sanitized_inputs = helpers.sanitize(request.form)
            email = sanitized_inputs['email']
            print email
            resend_email = services.resend_email(email)
            print resend_email
            print resend_email.status_code
            if resend_email.status_code == 202:
                flash(resend_email.text, 'success')
            else:
                flash(resend_email.text, 'danger')
            # return redirect(url_for('.resend_email'))
        # else:
        #     return render_template('users/resend_email.html',
        #                 resend_email_form=resend_email_form)
        return redirect(url_for('.login_page'))


@UserBP.route('/password/reset/<string:token>', methods=['GET', 'POST'])
def reset_password(token=None):
    reset_password_form = ResetPasswordForm()
    if request.method == 'GET':
        return render_template('users/reset_password.html',
                               reset_password_form=reset_password_form)
    elif request.method == 'POST':
        email = request.args.get('email')
        if reset_password_form.validate_on_submit():
            sanitized_inputs = helpers.sanitize(request.form)
            password = sanitized_inputs['password']
            confirm_password = sanitized_inputs['confirm_password']
            reset_password = services.reset_password(email, token,
                                                     password,
                                                     confirm_password)
            if reset_password.status_code == 202:
                flash(reset_password.text, 'success')
            else:
                flash(reset_password.text, 'danger')
            return redirect(url_for('.login_page'))
        else:
            return render_template('users/reset_password.html',
                                   reset_password_form=reset_password_form)


@UserBP.route('/activate', methods=['GET'])
def activate_account():
    if request.method == 'GET':
        code = request.args.get('code')
        aid = request.args.get('aid')
        activate = services.activate(code, aid)
        if activate.status_code == 200:
            flash(activate.text, 'success')
        elif activate.status_code == 409:
            flash(activate.text, 'info')
        else:
            flash(activate.text, 'danger')
        return redirect(url_for('.login_page'))


@UserBP.route('/inbox/messages/new', methods=['GET', 'POST'])
@login_required
def new_message():
    message_form = MessageForm()
    resource_id = request.args.get('rid')
    uid = current_user.id
    messages = services.get_user_messages(uid, mode='unarchived')
    basic_auth = session['user_basic']
    count_auth = services.get_count_auth(basic_auth)
    message_count = count_auth['message_count']
    transaction_count = count_auth['pending_transaction_count']
    resource = resource_services.get_resource(resource_id)
    if request.method == 'GET':
        if messages is not None:
            print messages
            message_id = 0

            for message in messages:
                if message['resource']['id'] == int(resource_id):
                    message_id = message['id']

            if message_id > 0:
                return redirect(url_for('.message_thread',
                                        message_id=message_id))
            else:
                return render_template('users/new_chat_message.html',
                                       message_form=message_form,
                                       resource=resource,
                                       messages=messages,
                                       message_count=message_count,
                                       transaction_count=transaction_count)
        else:
            return render_template('users/new_chat_message.html',
                                   message_form=message_form,
                                   resource=resource,
                                   messages=messages,
                                   transaction_count=transaction_count,
                                   message_count=message_count)

    elif request.method == 'POST':
        json_data = request.get_json()
        message = json_data['message']
        resource_id = json_data['resource_id']
        new_msg = {
            'resource_id': resource_id,
            'message': message
        }

        send_new_msg = services.send_new_message(current_user.id, new_msg)
        json_result = send_new_msg.json()

        if send_new_msg.status_code == 202:
            return jsonify(json_result)
        return render_template('users/new_chat_message.html',
                               message_form=message_form,
                               resource=resource,
                               messages=messages,
                               transaction_count=transaction_count,
                               message_count=message_count)

    else:
        return render_template('users/new_chat_message.html',
                               message_form=message_form,
                               resource=resource,
                               messages=messages,
                               transaction_count=transaction_count,
                               message_count=message_count)


@UserBP.route('/inbox', methods=['GET'])
@login_required
def view_message_list():
    uid = current_user.id
    messages = services.get_user_messages(uid, mode='unarchived')

    page = request.args.get('page')
    if page is None:
        page = 1
    else:
        page = int(page)
    count = len(messages)
    pagination = Pagination(page, PAGES, count)
    messages = pagination.paginate(messages)

    basic_auth = session['user_basic']
    count_auth = services.get_count_auth(basic_auth)
    message_count = count_auth['message_count']
    transaction_count = count_auth['pending_transaction_count']

    return render_template('users/chat_message_list.html',
                           messages=messages, count=count,
                           pagination=pagination, page=page,
                           message_count=message_count,
                           transaction_count=transaction_count)


@UserBP.route('/inbox/messages/<int:message_id>', methods=['GET', 'POST'])
@login_required
def message_thread(message_id):
    uid = current_user.id
    messages = services.get_user_messages(uid, mode='unarchived')
    basic_auth = session['user_basic']
    count_auth = services.get_count_auth(basic_auth)
    transaction_count = count_auth['pending_transaction_count']

    message_form = MessageForm()
    if request.method == 'GET':
        msg_thread = services.get_user_message(current_user.id, message_id)
        message_count = count_auth['message_count']
        return render_template('users/chat_message.html',
                               msg_thread=msg_thread, messages=messages,
                               msg_id=message_id, message_form=message_form,
                               transaction_count=transaction_count,
                               message_count=message_count)

    elif request.method == 'POST':

        json_data = request.get_json()
        message = json_data['message']
        resource_id = json_data['resource_id']
        message_reply = {
            'resource_id': resource_id,
            'message': message
        }

        send_reply = services.send_reply_message(current_user.id, message_id,
                                                 message_reply)
        json_result = send_reply.json()
        print send_reply
        print json_result
        if send_reply.status_code == 202:
            return jsonify(json_result)
        return redirect(url_for('.message_thread', message_id=message_id))
    else:
        return render_template('users/chat_message.html',
                               message_form=message_form,
                               messages=messages,
                               transaction_count=transaction_count,
                               message_count=message_count)


@UserBP.route('/inbox/messages/<int:message_id>/archive', methods=['POST'])
@login_required
def archive_message_thread(message_id):
    uid = current_user.id
    message_form = MessageForm()
    messages = services.get_user_messages(uid, mode='all')
    basic_auth = session['user_basic']
    count_auth = services.get_count_auth(basic_auth)
    transaction_count = count_auth['pending_transaction_count']
    message_count = count_auth['message_count']

    if request.method == 'POST':
        if message_form.validate():
            archived_thread = services.archive_threads(uid,
                                                       message_id)
            if archived_thread.status_code == 202:
                # flash('Message successfully archived.', 'success')
                return redirect(url_for('.archived_message_list'))
            else:
                # flash(archived_thread.text, 'danger')
                return redirect(url_for('.view_message_list'))
        else:
            return render_template('users/chat_message_list.html',
                                   messages=messages,
                                   message_count=message_count,
                                   transaction_count=transaction_count)


@UserBP.route('/archived-inbox', methods=['GET'])
@login_required
def archived_message_list():
    uid = current_user.id
    messages = services.get_user_messages(uid, mode='archived')
    basic_auth = session['user_basic']
    count_auth = services.get_count_auth(basic_auth)
    transaction_count = count_auth['pending_transaction_count']
    message_count = count_auth['message_count']

    return render_template('users/archived_chat_message.html',
                           messages=messages,
                           message_count=message_count,
                           transaction_count=transaction_count)


@UserBP.route('/archived-inbox/<int:message_id>', methods=['GET'])
@login_required
def archived_message(message_id):
    uid = current_user.id
    messages = services.get_user_messages(uid, mode='archived')
    basic_auth = session['user_basic']
    count_auth = services.get_count_auth(basic_auth)
    transaction_count = count_auth['pending_transaction_count']

    message_form = MessageForm()
    if request.method == 'GET':
        msg_thread = services.get_user_message(current_user.id, message_id)
        message_count = count_auth['message_count']

        return render_template('users/archived_message.html',
                               msg_thread=msg_thread, messages=messages,
                               msg_id=message_id, message_form=message_form,
                               transaction_count=transaction_count,
                               message_count=message_count)


# AJAX call for refreshing Captcha
@UserBP.route('/users/__captcha', methods=['GET'])
def refresh_captcha():
    if request.method == 'GET':
        captcha_string = helpers.generate_random_chars(4)
        session['captcha_string'] = captcha_string
        captcha = services.generate_captcha(captcha_string)
        return jsonify({'message': captcha})


# Unsubscribe Notification Page
@UserBP.route('/unsubscribe/notifications',
              methods=['GET'])
@login_required
def unsubscribe_notification():
    if request.method == 'GET':
        unsubscribe = services.unsubsribe_email(type_id=0)
        print unsubscribe
        print 'hello'
        if unsubscribe.status_code == 200:
            return render_template("company/unsubscribe.html")
        else:
            return render_template("error_pages/404.html")


# Unsubscribe Notification Page
@UserBP.route('/unsubscribe/newsletters',
              methods=['GET'])
@login_required
def unsubscribe_newsletter():
    if request.method == 'GET':
        unsubscribe = services.unsubsribe_newsletter(type_id=1)
        if unsubscribe.status_code == 200:
            return render_template("company/unsubscribe.html")
        else:
            return render_template("error_pages/404.html")
