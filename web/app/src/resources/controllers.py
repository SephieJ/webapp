# -*- coding: utf-8 -*-

import re
import random
from flask import (Blueprint, render_template, request, redirect, url_for,
                   jsonify, flash, session)
from flask_login import login_required, current_user
from app.src.resources.forms import AddResourceForm, WishlistForm
from app.src.utils import helpers
import services, pprint
import dateutil.parser
from app.src.users import services as user_services
from app.src.users.transactions.forms import AddTransactionForm
from app.src.categories import services as category_services
from app.src.utils.pagination import Pagination
from app.src.utils.constants import PER_PAGE, PAGES
import HTMLParser
import ConfigParser
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pprint
import datetime as dt

ResourceBP = Blueprint('ResourceBP', __name__)


# View Resources Info
@ResourceBP.route('/<slug>',
                  methods=['GET', 'POST'])
def resource_page(slug):
    transaction_form = AddTransactionForm()
    resource_form = AddResourceForm()
    resource_id = slug.split("_")[-1]
    config = ConfigParser.RawConfigParser()
    config.read('env.cfg')
    fb_app_id = config.get('FacebookKey', 'FB_APP_ID')
    if not current_user.is_authenticated:
        session['selected_category'] = None
        session['selected_subcategory'] = None
    if request.method == 'GET':
        # s = time.time()
        other_resources = services.get_paginated_resources()
        count = 5
        if len(other_resources) < count:
            count = len(other_resources)
            other_resources = random.sample(other_resources, count)

        resource = services.get_resource(resource_id)

        # e = time.time()
        # print (e - s)
        is_favorite = False
        if current_user.is_authenticated:
            # s = time.time()
            user_favorites = user_services.get_favorites(current_user.id)
            for favorite in user_favorites:
                if favorite['id'] == resource_id:
                    is_favorite = True
                    break
            basic_auth = session['user_basic']
            count_auth = user_services.get_count_auth(basic_auth)
            message_count = count_auth['message_count']
            transaction_count = count_auth['pending_transaction_count']

            wishlists = user_services.get_wishlists(mode='unarchived')

            if request.args.get('rent_now'):
                return render_template('resources/rent-now.html',
                                       resource=resource,
                                       is_favorite=is_favorite,
                                       transaction_form=transaction_form,
                                       other_resources=other_resources,
                                       message_count=message_count,
                                       transaction_count=transaction_count,
                                       wishlists=wishlists,
                                       resource_form=resource_form,
                                       fb_app_id=fb_app_id)
            else:
                return render_template('resources/show.html',
                                       resource=resource,
                                       is_favorite=is_favorite,
                                       transaction_form=transaction_form,
                                       other_resources=other_resources,
                                       message_count=message_count,
                                       transaction_count=transaction_count,
                                       wishlists=wishlists,
                                       resource_form=resource_form,
                                       fb_app_id=fb_app_id)
        else:
            return render_template('resources/show.html',
                                   resource=resource,
                                   is_favorite=is_favorite,
                                   transaction_form=transaction_form,
                                   other_resources=other_resources,
                                   fb_app_id=fb_app_id)
    elif request.method == 'POST':
        if transaction_form.validate_on_submit():
            sanitize_inputs = helpers.sanitize(request.form)
            booking_date = sanitize_inputs['booking_date'].split(' - ')
            start_date = dateutil.parser.parse(booking_date[0]).isoformat()
            end_date = dateutil.parser.parse(booking_date[1]).isoformat()
            params = {
                'resource_id': resource_id,
                'proposal': sanitize_inputs['proposal'],
                'quantity': sanitize_inputs['quantity'],
                'booking_start_date': start_date,
                'booking_end_date': end_date
            }
            submit_transaction = user_services.submit_transaction(
                current_user.id, params)
            if submit_transaction.status_code == 201:
                flash('Booking has been submitted.', 'success')
            else:
                flash('Error in transaction booking.', 'danger')

            return redirect(url_for('.resource_page',
                                    slug=slug))
        else:
            return redirect(url_for('.resource_page',
                                    slug=slug))


# Add Resources
@ResourceBP.route('/share', methods=['GET', 'POST'])
@login_required
def add_resources_page():
    sPage = 'share'
    resource_form = AddResourceForm()
    basic_auth = session['user_basic']
    count_auth = user_services.get_count_auth(basic_auth)
    message_count = count_auth['message_count']
    transaction_count = count_auth['pending_transaction_count']
    this_user = user_services.get_profile(current_user.id).get('company').get('address')
    if this_user is not None:
        current_user_company = {
            str(key): str(value)
            for key, value in this_user.items()
        }
    else:
        current_user_company = {}
    if request.method == 'GET':
        return render_template('resources/add.html',
                               resource_form=resource_form,
                               message_count=message_count,
                               transaction_count=transaction_count,
                               current_user_company=current_user_company,
                               sPage=sPage)
    elif request.method == 'POST':
        if resource_form.validate_on_submit():
            keywords = [str(keyword)
                        for keyword in request.form.getlist('keywords[]')]
            sanitize_inputs = helpers.sanitize(request.form)
            item_name = sanitize_inputs['name']
            description = sanitize_inputs['description']
            quantity = sanitize_inputs['quantity']
            price = sanitize_inputs['price']
            unit_number = sanitize_inputs['unit_number']
            street = sanitize_inputs['street']
            zipcode = sanitize_inputs['zipcode']
            city = sanitize_inputs['city']
            state = sanitize_inputs['state']

            item_name = HTMLParser.HTMLParser().unescape(item_name)
            description = HTMLParser.HTMLParser().unescape(description)

            image_arr = request.form.getlist('inputImage_url[]')
            filtered_image_arr = filter(None, image_arr)

            image_json_array = []
            for img in filtered_image_arr:
                image = img.split(',')
                image_dict = {
                    'image': image[0],
                    'image_full': image[1]
                }
                image_json_array.append(image_dict)

            suggest_checkbox = resource_form.suggest_checkbox.data
            selected_categories = []
            if suggest_checkbox:
                parent = resource_form.parent_category.data
                subcategories = resource_form.subcategory.data
                subcategories_array = subcategories.split(',')

                for item in subcategories_array:
                    is_string = re.search('[a-zA-Z]', parent)
                    if is_string:
                        category = {
                            'main_category_name': parent,
                            'subcategory_name': item
                        }
                    else:
                        category = {
                            'main_category_id': int(parent),
                            'subcategory_name': item
                        }
                    selected_categories.append(category)
            else:
                categories = request.form.getlist('categories')
                for item in categories:
                    category_id = 0
                    category_list = category_services.get_categories()
                    for category in category_list:
                        for subcategory in category['subcategories']:
                            if subcategory['id'] == int(item):
                                category_id = category['id']
                                break
                    category = {
                        'main_category_id': category_id,
                        'subcategory_id': int(item)
                    }
                    selected_categories.append(category)

            unit = resource_form.unit.data
            booking_holiday = resource_form.booking_holiday.data
            resource_availability = resource_form.availability.data
            retain_availability = resource_form.retain.data

            if booking_holiday == 'Yes':
                booking_holiday = True
            else:
                booking_holiday = False

            if resource_availability == 'No':
                resource_avail_from = sanitize_inputs['avail_from']
                resource_avail_to = sanitize_inputs['avail_to']
                date_avail_from = \
                    dateutil.parser.parse(resource_avail_from).isoformat()
                date_avail_to = \
                    dateutil.parser.parse(resource_avail_to).isoformat()

                monday = resource_form.monday.data
                tuesday = resource_form.tuesday.data
                wednesday = resource_form.wednesday.data
                thursday = resource_form.thursday.data
                friday = resource_form.friday.data
                saturday = resource_form.saturday.data
                sunday = resource_form.sunday.data
            else:
                date_avail_from = dateutil.parser.parse(datetime.today().strftime("%Y-%m-%dT%H:%M:%S")).isoformat()
                date_avail_to = dateutil.parser.parse((datetime.today() + relativedelta(years=1)).strftime("%Y-%m-%dT%H:%M:%S")).isoformat()
                monday = True
                tuesday = True
                wednesday = True
                thursday = True
                friday = True
                saturday = False
                sunday = False

            avail_mins_from = 60
            avail_mins_to = 0
            sched_time_from = []
            sched_time_to = []
            dates = []

            if retain_availability == 'No':
                avail_mins_from = sanitize_inputs['avail_mins_from']
                avail_mins_to = sanitize_inputs['avail_mins_to']

                if avail_mins_to == '':
                    avail_mins_to = 0

                sched_from_arr = request.form.getlist('sched_time_from')
                dates_list_from = [
                    datetime.strptime(time_from, '%I:%M %p').now().isoformat()
                    for time_from in sched_from_arr
                ]
                for time_from_val in dates_list_from:
                    time_from_dict = ('from', time_from_val)
                    sched_time_from.append(time_from_dict)

                sched_to_arr = request.form.getlist('sched_time_to')
                dates_list_to = [
                    datetime.strptime(time_to, '%I:%M %p').now().isoformat()
                    for time_to in sched_to_arr
                ]
                for time_to_val in dates_list_to:
                    time_to_dict = ('to', time_to_val)
                    sched_time_to.append(time_to_dict)

                zip_dates = zip(sched_time_from, sched_time_to)

                for set_dates in zip_dates:
                    dict_dates = dict(set_dates)
                    dates.append(dict_dates)

            else:
                avail_mins_from
                avail_mins_to
                sched_time_from
                sched_time_to
                dates = [
                    { "from": "1970-01-01T09:00:00", "to": "1970-01-01T10:00:00" },
                    { "from": "1970-01-01T10:00:00", "to": "1970-01-01T11:00:00" },
                    { "from": "1970-01-01T11:00:00", "to": "1970-01-01T12:00:00" },
                    { "from": "1970-01-01T12:00:00", "to": "1970-01-01T13:00:00" },
                    { "from": "1970-01-01T13:00:00", "to": "1970-01-01T14:00:00" },
                    { "from": "1970-01-01T14:00:00", "to": "1970-01-01T15:00:00" },
                    { "from": "1970-01-01T15:00:00", "to": "1970-01-01T16:00:00" },
                    { "from": "1970-01-01T16:00:00", "to": "1970-01-01T17:00:00" },
                    { "from": "1970-01-01T17:00:00", "to": "1970-01-01T18:00:00" }
                ]

            resource = {
                'name': item_name,
                'description': description,
                'price': price,
                'quantity': quantity,
                'image_url': image_json_array[0]['image'],
                'categories': selected_categories,
                'location': [
                    {
                        'unit_number': unit_number,
                        'street': street,
                        'zipcode': zipcode,
                        'city': city,
                        'state': state,
                        'longitude': '',
                        'latitude': ''
                    }
                ],
                'resource_rate': unit,
                'availability': {
                    'available_date_from': date_avail_from,
                    'available_date_to': date_avail_to,
                    'schedules': dates,
                    'duration': avail_mins_from,
                    'gap': avail_mins_to,
                    'is_available_on_holidays': booking_holiday,
                    'days_available': {
                        'monday': monday,
                        'tuesday': tuesday,
                        'wednesday': wednesday,
                        'thursday': thursday,
                        'friday': friday,
                        'saturday': saturday,
                        'sunday': sunday
                    },
                    'resource_availability': resource_availability,
                    'retain_availability': retain_availability
                },
                'images': image_json_array,
                'keywords': keywords
            }

            pprint.pprint(resource)
            # return jsonify(resource)
            add_resource = services.add_resource(current_user.id,
                                                 resource)
            if add_resource.status_code == 201:
                flash(add_resource.text, 'success')
                return redirect(url_for('.add_resources_page', sPage=sPage))
            else:
                flash(add_resource.text, 'danger')
                return render_template('resources/add.html',
                                       resource_form=resource_form,
                                       message_count=message_count,
                                       transaction_count=transaction_count,
                                       current_user_company=current_user_company,
                                       sPage=sPage)
        else:
            flash(resource_form.errors, 'danger')
            return render_template('resources/add.html',
                                   resource_form=resource_form,
                                   message_count=message_count,
                                   transaction_count=transaction_count,
                                   current_user_company=current_user_company,
                                   sPage=sPage)


# Edit Resource
@ResourceBP.route('/resources/<slug>/edit', methods=['GET', 'POST'])
@login_required
def edit_resources_page(slug):
    resource_form = AddResourceForm()
    resource_id = slug.split("_")[-1]
    resource = services.get_resource(resource_id)
    basic_auth = session['user_basic']
    count_auth = user_services.get_count_auth(basic_auth)
    message_count = count_auth['message_count']
    transaction_count = count_auth['pending_transaction_count']
    resource['keywords'] = [
        str(keyword) for keyword in resource.get('keywords')] if \
        resource.get('keywords') is not None else []
    this_user = user_services.get_profile(current_user.id).get('company').get('address')
    if this_user is not None:
        current_user_company = {
            str(key): str(value)
            for key, value in this_user.items()
        }
    else:
        current_user_company = {}
    if resource['owner_id'] != current_user.id:
        return render_template('error_pages/401.html')
    # input1 = 'Yes'
    # input2 = 'No'
    # input3 = 'No'
    if request.method == 'GET':
        if resource['has_update']:
            flash('There is still pending verification for this resource',
                  'danger')
            return redirect(url_for('.resource_page',
                                    slug=slug))
            # return render_template('error_pages/pending-resource.html',
            #                        resource=resource)
        HTMLParser.HTMLParser().unescape(resource['description'])
        HTMLParser.HTMLParser().unescape(resource['resource_name'])
        resource_form.description.data = resource['description']
        resource_form.unit.data = resource['rate']
        # resource_form.availability.data = input2
        # resource_form.retain.data = input3
        # resource_form.availability.form = False
        # print resource
        return render_template('resources/edit.html',
                               resource_form=resource_form,
                               resource=resource,
                               message_count=message_count,
                               current_user_company=current_user_company,
                               transaction_count=transaction_count,)
                            #    input1=input1, input2=input2, input3=input3)
    elif request.method == 'POST':
        if resource_form.validate_on_submit():
            keywords = [str(keyword)
                        for keyword in request.form.getlist('keywords[]')]
            sanitize_inputs = helpers.sanitize(request.form)
            item_name = sanitize_inputs['name']
            description = sanitize_inputs['description']
            quantity = sanitize_inputs['quantity']
            price = sanitize_inputs['price']
            unit_number = sanitize_inputs['unit_number']
            street = sanitize_inputs['street']
            zipcode = sanitize_inputs['zipcode']
            city = sanitize_inputs['city']
            state = sanitize_inputs['state']

            # item_name = HTMLParser.HTMLParser().unescape(item_name)
            # description = HTMLParser.HTMLParser().unescape(description)

            image_arr = request.form.getlist('inputImage_url[]')
            filtered_image_arr = filter(None, image_arr)

            image_json_array = []
            for img in filtered_image_arr:
                image = img.split(',')
                image_dict = {
                    'image': image[0],
                    'image_full': image[1]
                }
                image_json_array.append(image_dict)

            suggest_checkbox = resource_form.suggest_checkbox.data
            selected_categories = []
            if suggest_checkbox:
                parent = resource_form.parent_category.data
                subcategories = resource_form.subcategory.data
                subcategories_array = subcategories.split(',')

                for item in subcategories_array:
                    is_string = re.search('[a-zA-Z]', parent)
                    if is_string:
                        category = {
                            'main_category_name': parent,
                            'subcategory_name': item
                        }
                    else:
                        category = {
                            'main_category_id': int(parent),
                            'subcategory_name': item
                        }
                    selected_categories.append(category)
            else:
                categories = request.form.getlist('categories')
                for item in categories:
                    category_id = 0
                    category_list = category_services.get_categories()
                    for category in category_list:
                        for subcategory in category['subcategories']:
                            if subcategory['id'] == int(item):
                                category_id = category['id']
                                break
                    category = {
                        'main_category_id': category_id,
                        'subcategory_id': int(item)
                    }
                    selected_categories.append(category)

            unit = resource_form.unit.data
            booking_holiday = resource_form.booking_holiday.data
            resource_availability = resource_form.availability.data
            retain_availability = resource_form.retain.data

            if booking_holiday == 'Yes':
                booking_holiday = True
            else:
                booking_holiday = False

            if resource_availability == 'No':
                resource_avail_from = sanitize_inputs['avail_from']
                resource_avail_to = sanitize_inputs['avail_to']
                date_avail_from = \
                    dateutil.parser.parse(resource_avail_from).isoformat()
                date_avail_to = \
                    dateutil.parser.parse(resource_avail_to).isoformat()

                monday = resource_form.monday.data
                tuesday = resource_form.tuesday.data
                wednesday = resource_form.wednesday.data
                thursday = resource_form.thursday.data
                friday = resource_form.friday.data
                saturday = resource_form.saturday.data
                sunday = resource_form.sunday.data
            else:
                date_avail_from = dateutil.parser.parse(datetime.today().strftime("%Y-%m-%dT%H:%M:%S")).isoformat()
                date_avail_to = dateutil.parser.parse((datetime.today() + relativedelta(years=1)).strftime("%Y-%m-%dT%H:%M:%S")).isoformat()
                monday = True
                tuesday = True
                wednesday = True
                thursday = True
                friday = True
                saturday = False
                sunday = False

            avail_mins_from = 60
            avail_mins_to = 0
            sched_time_from = []
            sched_time_to = []
            dates = []

            if retain_availability == 'No':
                avail_mins_from = sanitize_inputs['avail_mins_from']
                avail_mins_to = sanitize_inputs['avail_mins_to']

                if avail_mins_to == '':
                    avail_mins_to = 0

                sched_from_arr = request.form.getlist('sched_time_from')
                dates_list_from = [
                    datetime.strptime(time_from, '%I:%M %p').isoformat()
                    for time_from in sched_from_arr
                ]
                for time_from_val in dates_list_from:
                    time_from_dict = ('from', time_from_val)
                    sched_time_from.append(time_from_dict)

                sched_to_arr = request.form.getlist('sched_time_to')
                dates_list_to = [
                    datetime.strptime(time_to, '%I:%M %p').isoformat()
                    for time_to in sched_to_arr
                ]
                for time_to_val in dates_list_to:
                    time_to_dict = ('to', time_to_val)
                    sched_time_to.append(time_to_dict)

                zip_dates = zip(sched_time_from, sched_time_to)

                for set_dates in zip_dates:
                    dict_dates = dict(set_dates)
                    dates.append(dict_dates)

            else:
                avail_mins_from
                avail_mins_to
                sched_time_from
                sched_time_to
                dates = [
                    { "from": "1970-01-01T09:00:00", "to": "1970-01-01T10:00:00" },
                    { "from": "1970-01-01T10:00:00", "to": "1970-01-01T11:00:00" },
                    { "from": "1970-01-01T11:00:00", "to": "1970-01-01T12:00:00" },
                    { "from": "1970-01-01T12:00:00", "to": "1970-01-01T13:00:00" },
                    { "from": "1970-01-01T13:00:00", "to": "1970-01-01T14:00:00" },
                    { "from": "1970-01-01T14:00:00", "to": "1970-01-01T15:00:00" },
                    { "from": "1970-01-01T15:00:00", "to": "1970-01-01T16:00:00" },
                    { "from": "1970-01-01T16:00:00", "to": "1970-01-01T17:00:00" },
                    { "from": "1970-01-01T17:00:00", "to": "1970-01-01T18:00:00" }
                ]

            resource = {
                'name': item_name,
                'description': description,
                'price': price,
                'quantity': quantity,
                'image_url': image_json_array[0]['image'],
                'categories': selected_categories,
                'location': [
                    {
                        'unit_number': unit_number,
                        'street': street,
                        'zipcode': zipcode,
                        'city': city,
                        'state': state,
                        'longitude': '',
                        'latitude': ''
                    }
                ],
                'resource_rate': unit,
                'availability': {
                    'available_date_from': date_avail_from,
                    'available_date_to': date_avail_to,
                    'schedules': dates,
                    'duration': avail_mins_from,
                    'gap': avail_mins_to,
                    'is_available_on_holidays': booking_holiday,
                    'days_available': {
                        'monday': monday,
                        'tuesday': tuesday,
                        'wednesday': wednesday,
                        'thursday': thursday,
                        'friday': friday,
                        'saturday': saturday,
                        'sunday': sunday
                    },
                    'resource_availability': resource_availability,
                    'retain_availability': retain_availability
                },
                'images': image_json_array,
                'keywords': keywords
            }

            pprint.pprint(resource)
            # return jsonify(resource)
            edit_resource = services.edit_resource(resource_id,
                                                   current_user.id,
                                                   resource)
            # if edit_resource.status_code == 202:
            if edit_resource.status_code in [202, 200]:
                # flash('Your resource is updated and will reviewed first \
                #       by the Admin to accept the changes.',
                #       'success')
                notice = 'Your updates have been saved and will be reviewed by the administrator'
                flash(notice + ' for approval before the changes are reflected.', 'success')
                return redirect(url_for('.resource_page',
                                        slug=slug))
            else:
                flash(edit_resource.text, 'danger')
                return redirect(url_for('.edit_resources_page',
                                        slug=slug))
        else:
            flash(resource_form.errors, 'danger')
            return render_template('resources/edit.html',
                                   resource_form=resource_form,
                                   resource=resource,
                                   message_count=message_count,
                                   current_user_company=current_user_company,
                                   transaction_count=transaction_count)


# Provide Wishlist
@ResourceBP.route('/provide-wishlist/<slug>', methods=['GET', 'POST'])
@login_required
def provide_wishlist_page(slug):
    sPage = 'provide-wishlist/' + slug
    wishlist_id = slug.split("_")[-1]
    wishlist = services.get_wishlist_item(wishlist_id,
                                          mode='unarchived')
    resource_form = AddResourceForm()
    basic_auth = session['user_basic']
    count_auth = user_services.get_count_auth(basic_auth)
    message_count = count_auth['message_count']
    transaction_count = count_auth['pending_transaction_count']

    if request.method == 'GET':
        resource_form.name.data = wishlist['name']
        resource_form.description.data = wishlist['description']
        return render_template('resources/add_wishlist.html',
                               resource_form=resource_form,
                               message_count=message_count,
                               transaction_count=transaction_count,
                               sPage=sPage, wishlist=wishlist)
    elif request.method == 'POST':
        if resource_form.validate_on_submit():
            sanitize_inputs = helpers.sanitize(request.form)
            item_name = sanitize_inputs['name']
            description = sanitize_inputs['description']
            quantity = sanitize_inputs['quantity']
            price = sanitize_inputs['price']
            rates = resource_form.rates.data
            street = sanitize_inputs['street']
            city = sanitize_inputs['city']
            state = sanitize_inputs['state']
            zipcode = sanitize_inputs['zipcode']

            item_name = HTMLParser.HTMLParser().unescape(item_name)
            description = HTMLParser.HTMLParser().unescape(description)
            print item_name
            print description

            image_arr = request.form.getlist('inputImage_url[]')
            filtered_image_arr = filter(None, image_arr)

            image_json_array = []
            for img in filtered_image_arr:
                image = img.split(',')
                image_dict = {
                    'image': image[0],
                    'image_full': image[1]
                }
                image_json_array.append(image_dict)

            suggest_checkbox = resource_form.suggest_checkbox.data
            selected_categories = []
            if suggest_checkbox:
                parent = resource_form.parent_category.data
                subcategories = resource_form.subcategory.data
                subcategories_array = subcategories.split(',')

                for item in subcategories_array:
                    is_string = re.search('[a-zA-Z]', parent)
                    if is_string:
                        category = {
                            'main_category_name': parent,
                            'subcategory_name': item
                        }
                    else:
                        category = {
                            'main_category_id': int(parent),
                            'subcategory_name': item
                        }
                    selected_categories.append(category)
            else:
                categories = request.form.getlist('categories')
                for item in categories:
                    category_id = 0
                    category_list = category_services.get_categories()
                    for category in category_list:
                        for subcategory in category['subcategories']:
                            if subcategory['id'] == int(item):
                                category_id = category['id']
                                break
                    category = {
                        'main_category_id': category_id,
                        'subcategory_id': int(item)
                    }
                    selected_categories.append(category)
            resource = {
                'name': item_name,
                'description': description,
                'price': price,
                'quantity': quantity,
                'resource_rate': rates,
                'image_url': image_json_array[0]['image'],
                'categories': selected_categories,
                'location': [
                    {
                        'street': street,
                        'city': city,
                        'state': state,
                        'zipcode': zipcode,
                        'longitude': '',
                        'latitude': ''
                    }
                ],
                'images': image_json_array
            }

            add_resource = services.add_resource(current_user.id,
                                                 resource)
            if add_resource.status_code == 201:
                flash(add_resource.text, 'success')
                return redirect(url_for('.provide_wishlist_page', sPage=sPage))
            else:
                flash(add_resource.text, 'danger')
                return render_template('resources/add_wishlist.html',
                                       resource_form=resource_form,
                                       message_count=message_count,
                                       transaction_count=transaction_count,
                                       sPage=sPage)
        else:
            return render_template('resources/add_wishlist.html',
                                   resource_form=resource_form,
                                   message_count=message_count,
                                   transaction_count=transaction_count,
                                   sPage=sPage)


# Delete Resources
@ResourceBP.route('/myresources/<int:resource_id>/delete',
                  methods=['GET', 'POST'])
@login_required
def delete_resources_page(resource_id):
    if request.method == 'GET':
        delete_resource = services.delete_resource(current_user.id,
                                                   resource_id)
        if delete_resource.status_code == 202:
            flash('Successfully removed.', 'success')
        else:
            flash(delete_resource.text, 'danger')
        return redirect(url_for('.resource_category_page'))


# Archived Resources List
@ResourceBP.route('/myresources/archived', methods=['GET'])
@login_required
def archived_resources_page():
    if request.method == 'GET':
        resources = services.get_resources(mode='archived')
        return render_template('resources/restore.html', resources=resources)


# Restore Resources
@ResourceBP.route('/myresources/<int:resource_id>/restore',
                  methods=['GET', 'POST'])
@login_required
def restore_resources_page(resource_id):
    if request.method == 'GET':
        restore_resource = services.restore_resource(current_user.id,
                                                     resource_id)
        if restore_resource.status_code == 202:
            flash('Successfully restored.', 'success')
        else:
            flash(restore_resource.text, 'danger')
        return redirect(url_for('.resource_category_page'))


# Search for Resources
@ResourceBP.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
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
            resources = services.get_search_results(
                query=query, sort=sort,
                min_price=min_price,
                max_price=max_price)
        else:
            resources = services.get_search_results(
                query=query, sort=sort)

    else:
        resources = services.get_search_results(query=query)
    count = len(resources)
    pagination = Pagination(page, PER_PAGE, count)
    resources = pagination.paginate(resources)

    if current_user.is_authenticated:
        wishlists = user_services.get_wishlists(mode='unarchived')
        basic_auth = session['user_basic']
        count_auth = user_services.get_count_auth(basic_auth)
        message_count = count_auth['message_count']
        transaction_count = count_auth['pending_transaction_count']
        return render_template('resources/search.html',
                               resources=resources,
                               query=query,
                               sorting=sorting,
                               min_price=min_price,
                               max_price=max_price,
                               page=page,
                               pagination=pagination,
                               message_count=message_count,
                               transaction_count=transaction_count,
                               wishlists=wishlists)
    else:
        return render_template('resources/search.html',
                               resources=resources,
                               query=query,
                               sorting=sorting,
                               min_price=min_price,
                               max_price=max_price,
                               page=page,
                               pagination=pagination)


# General Search
@ResourceBP.route('/search-all', methods=['GET'])
@login_required
def search_all():
    query = request.args.get('query')
    sorting = ''
    # sort = request.args.get('sort')
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')
    items = services.get_all_search_results(query=query)
    # print items
    if bool(items):
        result_resources = items['resources']
        result_users = items['accounts']
        result_companies = items['companies']
    else:
        result_resources = []
        result_users = []
        result_companies = []

    page_resources = request.args.get('page1')
    if page_resources is None:
        page_resources = 1
    else:
        page_resources = int(page_resources)

    print 'pagination'
    # page2 = request.args.get('page2')
    # if page2 is None:
    #     page2 = 1
    # else:
    #     page2 = int(page2)

    # page3 = request.args.get('page3')
    # if page3 is None:
    #     page3 = 1
    # else:
    #     page3 = int(page3)

    # if sort:
    #     sorting = sort
    #     if min_price or max_price:
    #         items['resources'] = services.get_all_search_results(
    #             query=query, sort=sort,
    #             min_price=min_price,
    #             max_price=max_price)
    #     else:
    #         items['resources'] = services.get_all_search_results(
    #             query=query, sort=sort)

    # else:
    #     items = services.get_all_search_results(query=query)
    # print items['companies']
    # count1 = len(items['accounts'])
    # count2 = len(items['companies'])
    count_resources = len(result_resources)
    # print count1
    # pagination1 = Pagination(page1, PAGES, count1)
    # pagination2 = Pagination(page2, PAGES, count2)
    pagination_resources = Pagination(page_resources, PAGES, count_resources)
    print 'helo'
    print page_resources
    # item_list = []
    # item_list = items['accounts'] + items['companies'] + items['resources']
    # print item_list
    # item_list = pagination.paginate(item_list)
    # item_account = pagination1.paginate(items['accounts'])
    # item_company = pagination2.paginate(items['companies'])
    chunk_resources = pagination_resources.paginate(result_resources)

    if current_user.is_authenticated:
        wishlists = user_services.get_wishlists(mode='unarchived')
        basic_auth = session['user_basic']
        count_auth = user_services.get_count_auth(basic_auth)
        message_count = count_auth['message_count']
        transaction_count = count_auth['pending_transaction_count']
        return render_template('resources/search_all.html',
                               query=query,
                               sorting=sorting,
                               min_price=min_price,
                               max_price=max_price,
                               page_resources=page_resources,
                               pagination_resources=pagination_resources,
                               message_count=message_count,
                               transaction_count=transaction_count,
                               wishlists=wishlists,
                               result_resources=result_resources,
                               result_users=result_users,
                               result_companies=result_companies,
                               chunk_resources=chunk_resources)


# Add Wishlist
@ResourceBP.route('/wishlist', methods=['GET', 'POST'])
@login_required
def add_wishlist_page():
    uid = current_user.id
    sPage = 'wishlists'
    wishlist_form = WishlistForm()
    wishlists = user_services.get_wishlists(mode='unarchived')
    basic_auth = session['user_basic']
    count_auth = user_services.get_count_auth(basic_auth)
    message_count = count_auth['message_count']
    transaction_count = count_auth['pending_transaction_count']
    if request.method == 'GET':
        return render_template('resources/wishlist.html',
                               wishlist_form=wishlist_form,
                               message_count=message_count,
                               transaction_count=transaction_count,
                               wishlists=wishlists,
                               sPage=sPage)
    elif request.method == 'POST':
        if wishlist_form.validate_on_submit():
            sanitize_inputs = helpers.sanitize(request.form)
            item_name = sanitize_inputs['name']
            description = sanitize_inputs['description']

            item_name = HTMLParser.HTMLParser().unescape(item_name)
            description = HTMLParser.HTMLParser().unescape(description)

            suggest_checkbox = wishlist_form.suggest_checkbox.data
            selected_categories = []
            if suggest_checkbox:
                parent = wishlist_form.parent_category.data
                subcategories = wishlist_form.subcategory.data
                subcategories_array = subcategories.split(',')

                for item in subcategories_array:
                    is_string = re.search('[a-zA-Z]', parent)
                    if is_string:
                        category = {
                            'main_category_name': parent,
                            'subcategory_name': item
                        }
                    else:
                        category = {
                            'main_category_id': int(parent),
                            'subcategory_name': item
                        }
                    selected_categories.append(category)
            else:
                categories = request.form.getlist('categories')
                for item in categories:
                    category_id = 0
                    category_list = category_services.get_categories()
                    for category in category_list:
                        for subcategory in category['subcategories']:
                            if subcategory['id'] == int(item):
                                category_id = category['id']
                                break
                    category = {
                        'main_category_id': category_id,
                        'subcategory_id': int(item)
                    }
                    selected_categories.append(category)

            wishlist = {
                'name': item_name,
                'description': description,
                'categories': selected_categories,
            }
            add_wishlist = services.add_wishlist(uid, wishlist)
            if add_wishlist.status_code == 201:
                flash(add_wishlist.text, 'success')
                return redirect(url_for('.add_wishlist_page', sPage=sPage))
            else:
                flash(add_wishlist.text, 'danger')
                return render_template('resources/wishlist.html',
                                       wishlist_form=wishlist_form,
                                       message_count=message_count,
                                       transaction_count=transaction_count,
                                       wishlists=wishlists,
                                       sPage=sPage)
        else:
            return render_template('resources/wishlist.html',
                                   wishlist_form=wishlist_form,
                                   message_count=message_count,
                                   transaction_count=transaction_count,
                                   wishlists=wishlists,
                                   sPage=sPage)


# Edit Wishlist
@ResourceBP.route('/wishlist/<slug>/edit', methods=['GET', 'POST'])
@login_required
def edit_wishlist_page(slug):
    wishlist_form = WishlistForm()
    uid = current_user.id
    wishlist_id = int(slug.split("_")[-1])

    wishlists = user_services.get_wishlists(mode='unarchived')
    wishlist = services.get_wishlist_item(wishlist_id,
                                          mode='unarchived')
    basic_auth = session['user_basic']
    count_auth = user_services.get_count_auth(basic_auth)
    message_count = count_auth['message_count']
    transaction_count = count_auth['pending_transaction_count']
    if request.method == 'GET':
        if uid == wishlist['account']['id']:
            wishlist_form.name.data = wishlist['name']
            wishlist_form.description.data = wishlist['description']
            return render_template('resources/edit_wishlist.html',
                                   wishlist_form=wishlist_form,
                                   message_count=message_count,
                                   transaction_count=transaction_count,
                                   wishlists=wishlists, wishlist=wishlist)
        else:
            return render_template('error_pages/401.html')
    elif request.method == 'POST':
        if uid == wishlist['account']['id']:
            if wishlist_form.validate_on_submit():
                sanitize_inputs = helpers.sanitize(request.form)
                item_name = sanitize_inputs['name']
                description = sanitize_inputs['description']

                item_name = HTMLParser.HTMLParser().unescape(item_name)
                description = HTMLParser.HTMLParser().unescape(description)

                suggest_checkbox = wishlist_form.suggest_checkbox.data
                selected_categories = []
                if suggest_checkbox:
                    parent = wishlist_form.parent_category.data
                    subcategories = wishlist_form.subcategory.data
                    subcategories_array = subcategories.split(',')

                    for item in subcategories_array:
                        is_string = re.search('[a-zA-Z]', parent)
                        if is_string:
                            category = {
                                'main_category_name': parent,
                                'subcategory_name': item
                            }
                        else:
                            category = {
                                'main_category_id': int(parent),
                                'subcategory_name': item
                            }
                        selected_categories.append(category)
                else:
                    categories = request.form.getlist('categories')
                    for item in categories:
                        category_id = 0
                        category_list = category_services.get_categories()
                        for category in category_list:
                            for subcategory in category['subcategories']:
                                if subcategory['id'] == int(item):
                                    category_id = category['id']
                                    break
                        category = {
                            'main_category_id': category_id,
                            'subcategory_id': int(item)
                        }
                        selected_categories.append(category)

                wishlist = {
                    'name': item_name,
                    'description': description,
                    'categories': selected_categories,
                }
                print wishlist_id
                print wishlist
                edit_wishlist = services.edit_wishlist(uid,
                                                       wishlist_id,
                                                       wishlist)
                print edit_wishlist
                notice = 'Your updates have been saved ' \
                    'and will be reviewed by the administrator ' \
                    'for approval before the changes are reflected.'
                if edit_wishlist.status_code == 202:
                    flash(notice, 'success')
                    return redirect(url_for('.edit_wishlist_page', slug=slug))
                else:
                    flash(edit_wishlist.text, 'danger')
                    return render_template('resources/edit_wishlist.html',
                                           wishlist_form=wishlist_form,
                                           message_count=message_count,
                                           transaction_count=transaction_count,
                                           wishlists=wishlists,
                                           wishlist=wishlist)
            else:
                return render_template('resources/edit_wishlist.html',
                                       wishlist_form=wishlist_form,
                                       message_count=message_count,
                                       transaction_count=transaction_count,
                                       wishlists=wishlists, wishlist=wishlist)
        else:
            return render_template('error_pages/401.html')


# View Wishlist
@ResourceBP.route('/wishlist/<slug>', methods=['GET'])
@login_required
def view_wishlist_page(slug):
    wishlist_form = WishlistForm()
    wishlist_id = slug.split("_")[-1]
    wishlist = services.get_wishlist_item(wishlist_id,
                                          mode='unarchived')
    print wishlist_id
    wishlists = user_services.get_wishlists(mode='unarchived')
    basic_auth = session['user_basic']
    count_auth = user_services.get_count_auth(basic_auth)
    message_count = count_auth['message_count']
    transaction_count = count_auth['pending_transaction_count']
    if request.method == 'GET':
        return render_template('resources/show_wishlist.html',
                               wishlist_form=wishlist_form,
                               message_count=message_count,
                               transaction_count=transaction_count,
                               wishlist=wishlist,
                               wishlists=wishlists)


# AJAX Call add Resources to Favorites
@ResourceBP.route('/resources/<int:resource_id>/bookmarks', methods=['GET'])
def add_favorites_page(resource_id):
    if request.method == 'GET':
        result = user_services.mark_favorite(current_user.id, resource_id)
        return jsonify({'message': result})


# Archive Resource
@ResourceBP.route('/users/<int:user_id>/resources/<slug>',
                  methods=['POST'])
@login_required
def archive_resource(user_id, slug):
    resource_form = AddResourceForm()
    transaction_form = AddTransactionForm()

    other_resources = services.get_resources()
    count = 5
    if len(other_resources) < count:
        count = len(other_resources)
        other_resources = random.sample(other_resources, count)
    resource_id = slug.split("_")[-1]
    resource = services.get_resource(resource_id)
    is_favorite = False

    user_favorites = user_services.get_favorites(current_user.id)
    for favorite in user_favorites:
        if favorite['id'] == resource['resource_id']:
            is_favorite = True
            break
    uid = current_user.id

    wishlists = user_services.get_wishlists(mode='unarchived')
    basic_auth = session['user_basic']
    count_auth = user_services.get_count_auth(basic_auth)
    message_count = count_auth['message_count']
    transaction_count = count_auth['pending_transaction_count']

    if request.method == 'POST':
        archive_resource = services.delete_resource(uid, resource_id)
        if archive_resource.status_code == 202:
            return redirect(url_for('UserBP.archive_resources_page',
                                    user_id=uid))
        else:
            flash('Error in deleting resource.', 'danger')
            return redirect(url_for('.resource_page',
                                    slug=slug))
    else:
        return render_template('resources/show.html',
                               resource=resource,
                               is_favorite=is_favorite,
                               transaction_form=transaction_form,
                               other_resources=other_resources,
                               message_count=message_count,
                               transaction_count=transaction_count,
                               wishlists=wishlists,
                               resource_form=resource_form)


# Restore Resource
@ResourceBP.route('/users/<int:user_id>/resources/<slug>/restore',
                  methods=['POST'])
@login_required
def restore_resource(user_id, slug):
    resource_form = AddResourceForm()
    transaction_form = AddTransactionForm()
    resource_id = slug.split("_")[-1]
    other_resources = services.get_resources()
    count = 5
    if len(other_resources) < count:
        count = len(other_resources)
        other_resources = random.sample(other_resources, count)
    resource = services.get_resource(resource_id)
    is_favorite = False

    user_favorites = user_services.get_favorites(current_user.id)
    for favorite in user_favorites:
        if favorite['id'] == resource['resource_id']:
            is_favorite = True
            break
    uid = current_user.id
    wishlists = user_services.get_wishlists(mode='unarchived')
    basic_auth = session['user_basic']
    count_auth = user_services.get_count_auth(basic_auth)
    message_count = count_auth['message_count']
    transaction_count = count_auth['pending_transaction_count']

    if request.method == 'POST':
        archive_resource = services.restore_resource(uid, resource_id)
        if archive_resource.status_code == 202:
            return redirect(url_for('UserBP.user_resources_page',
                                    user_id=uid))
        else:
            flash('Error in restoring resource.', 'danger')
            return redirect(url_for('.resource_page',
                                    resource_id=resource_id))
    else:
        return render_template('resources/show.html',
                               resource=resource,
                               is_favorite=is_favorite,
                               transaction_form=transaction_form,
                               other_resources=other_resources,
                               message_count=message_count,
                               transaction_count=transaction_count,
                               wishlists=wishlists,
                               resource_form=resource_form)


# Archive Wishlist
@ResourceBP.route('/users/<int:user_id>/wishlist/<slug>/archive',
                  methods=['POST'])
@login_required
def archive_wishlist_page(user_id, slug):
    wishlist_form = WishlistForm()

    wishlist_id = slug.split("_")[-1]
    wishlist = services.get_wishlist_item(wishlist_id,
                                          mode='unarchived')

    uid = current_user.id
    wishlists = user_services.get_wishlists(mode='unarchived')

    basic_auth = session['user_basic']
    count_auth = user_services.get_count_auth(basic_auth)
    message_count = count_auth['message_count']
    transaction_count = count_auth['pending_transaction_count']

    if request.method == 'POST':
        archive_wishlist = services.delete_wishlist(uid, wishlist_id)
        if archive_wishlist.status_code == 202:
            return redirect(url_for('UserBP.archive_wishlist_page',
                                    user_id=uid))
        else:
            flash('Error in deleting resource.', 'danger')
            return redirect(url_for('.view_wishlist_page',
                                    slug=slug))
    else:
        return render_template('resources/show_wishlist.html',
                               wishlist_form=wishlist_form,
                               message_count=message_count,
                               transaction_count=transaction_count,
                               wishlist=wishlist,
                               wishlists=wishlists)


# Restore Wishlist
@ResourceBP.route('/users/<int:user_id>/wishlist/<slug>/restore',
                  methods=['POST'])
@login_required
def restore_wishlist_page(user_id, slug):
    wishlist_form = WishlistForm()

    wishlist_id = slug.split("_")[-1]
    wishlist = services.get_wishlist_item(wishlist_id,
                                          mode='unarchived')

    uid = current_user.id
    wishlists = user_services.get_wishlists(mode='unarchived')
    basic_auth = session['user_basic']
    count_auth = user_services.get_count_auth(basic_auth)
    message_count = count_auth['message_count']
    transaction_count = count_auth['pending_transaction_count']
    if request.method == 'POST':
        restore_wishlist = services.restore_wishlist(uid, wishlist_id)
        if restore_wishlist.status_code == 202:
            return redirect(url_for('UserBP.user_wishlist_page',
                                    user_id=uid))
        else:
            flash('Error in restoring resource.', 'danger')
            return redirect(url_for('.view_wishlist_page',
                                    slug=slug))
    else:
        return render_template('resources/show_wishlist.html',
                               wishlist_form=wishlist_form,
                               message_count=message_count,
                               transaction_count=transaction_count,
                               wishlist=wishlist,
                               wishlists=wishlists)


@ResourceBP.route('/resources/upload/images', methods=['POST'])
def upload_image():
    json_data = request.get_json()
    image_base64 = json_data['image']
    image_base64_full = json_data['image_full']

    # CSS purposes of image upload spinner
    style_pic_id = json_data['pic_id']
    style_pic_wrap = json_data['pic_wrap']

    result = services.upload_image_multipart(image_base64, image_base64_full)
    json_result = result.json()
    json_result.update({"pic_id": style_pic_id, "pic_wrap": style_pic_wrap})
    return jsonify(json_result)


@ResourceBP.route('/keywords/check_profanity', methods=['POST'])
def check_profane_keyword():
    result = services.check_profanity(request.form.get('keyword'))
    json_result = result.json()
    return jsonify(json_result)
