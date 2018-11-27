# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, session
import services
from app.src.resources import services as resource_services
from app.src.utils.pagination import Pagination
from app.src.utils.constants import PER_PAGE
from app.src.users import services as user_services
from app.src.users import services as user_service
# from app.src.users.transactions import services as transaction_services

from flask_login import current_user

CategoryBP = Blueprint('CategoryBP', __name__)


# Category page with sub categories
@CategoryBP.route('/categories/<int:category_id>', methods=['GET'])
# @CategoryBP.route(
#     '/categories/<int:category_id>/subcategories/<int:subcategory_id>',
#     methods=['GET'])
def view_category_page(category_id):
    if request.method == 'GET':
        session['selected_category'] = None
        session['selected_subcategory'] = None
        active_subcategory = None
        sorting = ''
        subcategory_id = request.args.get('subcategory')
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
            if subcategory_id:
                active_subcategory = services.get_subcategory(category_id,
                                                              subcategory_id)
                if min_price or max_price:
                    resources = resource_services.get_subcategory_resources(
                        subcategory_id, sort=sort,
                        min_price=min_price, max_price=max_price)
                else:
                    resources = resource_services.get_subcategory_resources(
                        subcategory_id, sort=sort)
            else:
                if min_price or max_price:
                    resources = resource_services.get_category_resources(
                        category_id, sort=sort,
                        min_price=min_price, max_price=max_price)
                else:
                    resources = resource_services.get_category_resources(
                        category_id, sort=sort)
        else:
            if subcategory_id:
                active_subcategory = services.get_subcategory(category_id,
                                                              subcategory_id)
                resources = resource_services.get_subcategory_resources(
                    subcategory_id)
            else:
                resources = resource_services.get_category_resources(
                    category_id=category_id)

        parent_category = services.get_category(category_id)
        subcategories = services.get_subcategories(category_id)
        count = len(resources)
        pagination = Pagination(page, PER_PAGE, count)
        resources = pagination.paginate(resources)
        session['selected_category'] = parent_category
        if active_subcategory:
            session['selected_subcategory'] = active_subcategory
        if current_user.is_authenticated:
            wishlists = user_services.get_wishlists(mode='unarchived')

            basic_auth = session['user_basic']
            count_auth = user_service.get_count_auth(basic_auth)
            message_count = count_auth['message_count']
            transaction_count = count_auth['pending_transaction_count']
            return render_template('categories/index.html',
                                   parent_category=parent_category,
                                   subcategories=subcategories,
                                   resources=resources,
                                   active_subcategory=active_subcategory,
                                   sorting=sorting,
                                   min_price=min_price,
                                   max_price=max_price,
                                   count=count,
                                   page=page,
                                   pagination=pagination,
                                   message_count=message_count,
                                   transaction_count=transaction_count,
                                   wishlists=wishlists)
        else:
            return render_template('categories/index.html',
                                   parent_category=parent_category,
                                   subcategories=subcategories,
                                   resources=resources,
                                   active_subcategory=active_subcategory,
                                   sorting=sorting,
                                   min_price=min_price,
                                   max_price=max_price,
                                   count=count,
                                   page=page,
                                   pagination=pagination)
