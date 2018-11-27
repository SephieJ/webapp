# -*- coding: utf-8 -*-

import dateutil.parser
from app.src.utils import api_manager
from app.src.utils import constants
from io import BytesIO
import pprint, base64, re


def image_link_validation(image):
    invalid_status_codes = [403, 404, 500]
    first_check = api_manager.get_request_no_auth(image.get('image_full'))
    if first_check.status_code not in invalid_status_codes:
        return image
    temp_link = image.get('image_full').replace('.png', '.jpeg')
    second_check = api_manager.get_request_no_auth(temp_link)
    if second_check.status_code not in invalid_status_codes:
        return { 'image_full': temp_link, 'image': image.get('image') }
    return { 'image_full': image.get('image'), 'image': image.get('image') }


def get_resource(resource_id):
    url = constants.RESOURCE_NEW_ONE.format(resourceId=resource_id)
    req = api_manager.get_request_no_auth(url)
    resource = None
    if req.status_code == 200:
        try:
            resource = req.json()
            resource['price'] = ('%.2f' % resource['price'])
            valid_images_link = [
                { 
                    'image_full': image.get('image').replace('.png', '_full.png') if image.get('image').startswith('https') \
                        else "https://s3-ap-southeast-1.amazonaws.com/resourcestoshare/resources/static/uploads/{}_full.png".format(image.get('image')),
                    'image': image.get('image') if image.get('image').startswith('https') else \
                        "https://s3-ap-southeast-1.amazonaws.com/resourcestoshare/resources/static/uploads/{}.png".format(image.get('image')),
                }
                for image in resource.get('images')
            ]
            resource['images'] = [ image_link_validation(image) for image in valid_images_link ]
        except ValueError:
            resource = {}
    return resource


def get_resources(min_price=None, max_price=None, sort=None,
                  mode='unarchived'):
    params = {}
    params['mode'] = mode
    if min_price:
        params['min_price'] = min_price
    if max_price:
        params['max_price'] = max_price
    if sort:
        params['sort'] = sort
    url = constants.RESOURCE_ALL
    req = api_manager.get_request_no_auth(url, params)
    resources = []
    if req.status_code == 200:
        try:
            resources = req.json()
            for resource in resources:
                resource['created_date'] = dateutil.parser.parse(
                    resource['created_date'])
                resource['price'] = ('%.2f' % resource['price'])
        except ValueError:
            resources = []
    return resources


def get_paginated_resources(min_price=None, max_price=None, sort=None,
                            mode='unarchived', offset=0):
    params = {}
    params['mode'] = mode
    if min_price:
        params['min_price'] = min_price
    if max_price:
        params['max_price'] = max_price
    if sort:
        params['sort'] = sort
    url = constants.RESOURCE_NEW + '?offset=' + str(offset) + '&limit=15'
    req = api_manager.get_request_no_auth(url, params)
    resources = []
    if req.status_code == 200:
        try:
            resources = req.json()
            for resource in resources:
                # resource['created_date'] = dateutil.parser.parse(
                #     resource['created_date'])
                resource['price'] = ('%.2f' % resource['price'])
        except ValueError:
            resources = []
    return resources


def get_category_resources(category_id, min_price=None, max_price=None,
                           sort=None, mode='unarchived'):
    params = {'id': category_id}
    params['mode'] = mode
    if min_price:
        params['min_price'] = min_price
    if max_price:
        params['max_price'] = max_price
    if sort:
        params['sort'] = sort
    req = api_manager.get_request_no_auth(constants.RESOURCE_CATEGORIES,
                                          params)
    resources = []
    if req.status_code == 200:
        try:
            resources = req.json()
            for resource in resources:
                resource['created_date'] = dateutil.parser.parse(
                    resource['created_date'])
                resource['price'] = ('%.2f' % resource['price'])
        except ValueError:
            resources = []
    return resources


def get_subcategory_resources(subcategory_id, min_price=None, max_price=None,
                              sort=None, mode='unarchived'):
    params = {'id': subcategory_id}
    params['mode'] = mode
    if min_price:
        params['min_price'] = min_price
    if max_price:
        params['max_price'] = max_price
    if sort:
        params['sort'] = sort
    req = api_manager.get_request_no_auth(constants.RESOURCE_SUBCATEGORIES,
                                          params)
    resources = []
    if req.status_code == 200:
        try:
            resources = req.json()
            for resource in resources:
                resource['created_date'] = dateutil.parser.parse(
                    resource['created_date'])
                resource['price'] = ('%.2f' % resource['price'])
        except ValueError:
            resources = []
    return resources


def get_search_results(query=None, min_price=None, max_price=None, sort=None,
                       category_id=None, subcategory_id=None,
                       mode='unarchived'):
    params = {}
    params['mode'] = mode
    if query:
        params['query'] = query
    if min_price:
        params['min_price'] = min_price
    if max_price:
        params['max_price'] = max_price
    if sort:
        params['sort'] = sort
    if category_id:
        params['category_id'] = category_id
    if subcategory_id:
        params['subcategory_id'] = subcategory_id
    req = api_manager.get_request_no_auth(constants.RESOURCE_SEARCH, params)
    resources = []
    if req.status_code == 200:
        try:
            resources = req.json()
            for resource in resources:
                resource['created_date'] = dateutil.parser.parse(
                    resource['created_date'])
                resource['price'] = ('%.2f' % resource['price'])
        except ValueError:
            resources = []
    return resources


def get_all_search_results(query=None, mode='unarchived'):
    import pprint
    params = {}
    params['mode'] = mode
    if query:
        params['query'] = query
    req = api_manager.get_request(constants.SEARCH_ALL, params)
    items = []
    if req.status_code == 200:
        # try:
        #     items = req.json()
        #     pprint.pprint(items)
        #     for company in items['companies']:
        #         print 'company'
        #     for resource in items['resources']:
        #         resource['price'] = ('%.2f' % resource['price'])
        #     for user in items['accounts']:
        #         print 'user'
        # except ValueError:
        #     items = []
        if bool(req.json()):
            try:
                items = req.json()
                pprint.pprint(items)
                for company in items['companies']:
                    print 'company'
                for resource in items['resources']:
                    resource['price'] = ('%.2f' % resource['price'])
                for user in items['accounts']:
                    print 'user'
            except ValueError:
                items = []
        else:
            items = []

    return items


def add_resource(user_id, resource):
    url = constants.USER_RESOURCE_ALL.format(user_id=user_id)
    req = api_manager.post_request(url, resource)
    return req


def edit_resource(resource_id, user_id, resource):
    url = constants.USER_RESOURCE_ONE.format(user_id=user_id,
                                             resource_id=resource_id)
    req = api_manager.put_request(url, resource)
    return req


def delete_resource(user_id, resource_id):
    url = constants.USER_RESOURCE_ONE.format(user_id=user_id,
                                             resource_id=resource_id)
    req = api_manager.delete_request(url)
    return req


def restore_resource(user_id, resource_id):
    url = constants.USER_RESOURCE_RESTORE.format(user_id=user_id,
                                                 resource_id=resource_id)
    req = api_manager.post_request(url)
    return req


def upload_image(image_base64, image_base64_full):
    params = {
        'image': image_base64,
        'image_full': image_base64_full
    }
    req = api_manager.post_request(constants.IMAGE_UPLOAD, params)
    return req


def upload_image_multipart(image_base64, image_base64_full):
    image_base64 = re.sub('^data:image/.+;base64,', '', image_base64)
    image_cropped = BytesIO(base64.b64decode(image_base64))
    image_base64_full = re.sub('^data:image/.+;base64,', '', image_base64_full)
    image_full = BytesIO(base64.b64decode(image_base64_full))
    params = {
        'image': image_cropped,
        'image_full': image_full
    }
    req = api_manager.post_request(constants.IMAGE_UPLOAD, files=params)
    return req


def add_wishlist(user_id, wishlist):
    url = constants.WISHLIST_ALL.format(user_id=user_id)
    req = api_manager.post_request(url, wishlist)
    return req


def edit_wishlist(user_id, wishlist_id, wishlist):
    url = constants.WISHLIST_ONE.format(user_id=user_id,
                                        wishlist_id=wishlist_id)
    req = api_manager.put_request(url, wishlist)
    return req


def delete_wishlist(user_id, wishlist_id):
    url = constants.WISHLIST_ONE.format(user_id=user_id,
                                        wishlist_id=wishlist_id)
    req = api_manager.delete_request(url)
    return req


def restore_wishlist(user_id, wishlist_id):
    url = constants.WISHLIST_RESTORE.format(user_id=user_id,
                                            wishlist_id=wishlist_id)
    req = api_manager.post_request(url)
    return req


def get_wishlist_item(wishlist_id, mode='unarchived'):
    params = {'mode': mode}
    url = constants.WISHLIST_ITEM.format(wishlist_id=wishlist_id)
    req = api_manager.get_request(url, params)
    wishlist = None
    if req.status_code == 200:
        try:
            wishlist = req.json()
            wishlist['created_date'] = dateutil.parser.parse(
                wishlist['created_date'])
        except ValueError:
            wishlist = {}
    return wishlist


def check_profanity(word):
    data = dict(words=word)
    url = constants.PROFANITY_URL
    profanity_obj = api_manager.post_request_profanity(url, data)
    return profanity_obj
