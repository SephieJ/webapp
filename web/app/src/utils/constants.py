# -*- coding: utf-8 -*-
import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('env.cfg')

# Pagination
PER_PAGE = 15
PAGES = 10

API_BASE_URL = config.get('URL', 'API_BASE_URL')
WEB_BASE_URL = config.get('URL', 'WEB_BASE_URL')
PROFANITY_URL = config.get('URL', 'PROFANITY_URL')
CHAT_SUPPORT_URL = config.get('URL', 'CHAT_SUPPORT_URL')
# ONE MAP
ONE_MAP_URL = "https://developers.onemap.sg/commonapi"
# STAGINGAPI_BASE_URL = config.get('URL', 'STAGINGAPI_BASE_URL')

IMAGE_UPLOAD_DIR = WEB_BASE_URL + '/static/uploads/'
AUDIO_CAPTCHA_DIR = config.get('Captcha', 'AUDIO_PATH')

# Categories
CATEGORY_ALL = API_BASE_URL + '/categories'
CATEGORY_ONE = API_BASE_URL + '/categories/{category_id}'

# Sub-Categories
SUBCATEGORIES_ALL = API_BASE_URL + '/categories/{category_id}/subcategories'
SUBCATEGORIES_ONE = API_BASE_URL + '/categories/{category_id}' \
    '/subcategories/{subcategory_id}'

# Users
USERS_ONE = API_BASE_URL + '/users/{user_id}'
USER_LOGIN = API_BASE_URL + '/users/login'
USER_REGISTER = API_BASE_URL + '/users/register'
USER_ACTIVATE = API_BASE_URL + '/activate'
USER_PASSWORD = API_BASE_URL + '/users/{user_id}/password'
USER_FORGOT_PASSWORD = API_BASE_URL + '/users/password/forgot/web'
USER_RESEND_EMAIL = API_BASE_URL + '/users/resend/email'
USER_RESET_PASSWORD = API_BASE_URL + '/users/password/reset/web'
USER_RESOURCE_ALL = API_BASE_URL + '/users/{user_id}/resources'
USER_RESOURCE_ONE = API_BASE_URL + '/users/{user_id}/resources/{resource_id}'
USER_RESOURCE_RESTORE = API_BASE_URL + '/users/{user_id}' \
    '/resources/{resource_id}/restore'
USER_WISHLIST_ALL = API_BASE_URL + '/users/{user_id}/wishlists'
USER_WISHLIST_ONE = API_BASE_URL + 'users/{user_id}/wishlists/{wishlist_id}'
USER_FAVORITE = API_BASE_URL + '/users/{user_id}/resources/favorites'
USER_TRANSACTIONS = API_BASE_URL + '/users/{user_id}/transactions'
USER_TRANSACTION_DETAIL = API_BASE_URL + '/users/{user_id}' \
    '/transactions/{transaction_id}'
USER_TRANSACTIONS_SELLING = API_BASE_URL + '/users/{user_id}' \
    '/transactions/selling'
USER_TRANSACTIONS_BUYING = API_BASE_URL + '/users/{user_id}' \
    '/transactions/buying'
USER_TRANSACTION_RATE = API_BASE_URL + '/users/{user_id}' \
    '/transactions/{transaction_id}/rate'
USER_TRANSACTION_ACCEPT = API_BASE_URL + '/users/{user_id}' \
    '/transactions/{transaction_id}'
USER_TRANSACTION_REJECT = API_BASE_URL + '/users/{user_id}' \
    '/transactions/{transaction_id}/reject'
USER_TRANSACTION_COMPLETE = API_BASE_URL + '/users/{user_id}' \
    '/transactions/{transaction_id}/complete'
USER_MESSAGES = API_BASE_URL + '/users/{user_id}/messages'
USER_MESSAGE_THREAD = API_BASE_URL + '/users/{user_id}/messages/{message_id}'
USER_MESSAGE_REPLY = API_BASE_URL + '/users/{user_id}' \
    '/messages/{message_id}/reply'
USER_UNSUBSCRIBE_EMAIL = API_BASE_URL + '/users/unsubscribe?type={type_id}'
USER_UNSUBSCRIBE_NEWSLETTER = API_BASE_URL + \
    '/users/unsubscribe?type={type_id}'

# FAQS
FAQ_ALL = API_BASE_URL + '/faqs'
FAQ_ONE = API_BASE_URL + '/faqs/{faq_id}'
FAQ_QUESTION_ALL = API_BASE_URL + '/faqs/{faq_id}/questions'
FAQ_QUESTION_ONE = API_BASE_URL + '/faqs/{faq_id}/questions/{question_id}'

# Resources
RESOURCE_ALL = API_BASE_URL + '/resources'
RESOURCE_NEW = API_BASE_URL + '/new/resources'
RESOURCE_ONE = API_BASE_URL + '/resources/{resource_id}'
RESOURCE_NEW_ONE = API_BASE_URL + '/new/resources/{resourceId}'
RESOURCE_CATEGORIES = API_BASE_URL + '/resources/category'
RESOURCE_SUBCATEGORIES = API_BASE_URL + '/resources/subcategory'
RESOURCE_FAVORITE = API_BASE_URL + '/resources/{resource_id}/favorites'
RESOURCE_SEARCH = API_BASE_URL + '/resources/search'

# Company
COMPANY_REGISTER = API_BASE_URL + '/companies/register'
COMPANY_ONE = API_BASE_URL + '/companies/{company_id}'
COMPANY_INDUSTRY = API_BASE_URL + '/companies/industry'
COMPANY_MEMBERS = API_BASE_URL + '/companies/{company_id}/members'

# Resource image upload
# IMAGE_UPLOAD = API_BASE_URL + '/upload/images' # old api upload images
IMAGE_UPLOAD = API_BASE_URL + '/upload/images/multipart'

# Raise Support Request
RAISE_SUPPORT = API_BASE_URL + '/users/{user_id}/support/requests'
TICKET_ALL = API_BASE_URL + '/users/{user_id}/support/requests'

# Wishlist
WISHLIST_ALL = API_BASE_URL + '/users/{user_id}/wishlists'
WISHLIST_ONE = API_BASE_URL + '/users/{user_id}/wishlists/{wishlist_id}'
WISHLIST_RESTORE = API_BASE_URL + \
    '/users/{user_id}/wishlists/{wishlist_id}/restore'
WISHLIST = API_BASE_URL + '/wishlists'
WISHLIST_NEW = API_BASE_URL + '/new/wishlists'
WISHLIST_ITEM = API_BASE_URL + '/wishlists/{wishlist_id}'

# Chat Support
CLIENT_SUPPORT_REQUEST = CHAT_SUPPORT_URL + \
    '/client/supportrequests/{user_id}'
CLIENT_SUPPORT_REQUEST_CREATE = CHAT_SUPPORT_URL + \
    '/client/supportrequests/create'
CLIENT_SUPPORT_REQUEST_PROFILE = CHAT_SUPPORT_URL + \
    '/client/supportrequests/' \
    '{reference_code}/profile'
CLIENT_SUPPORT_CONVERSATION = CHAT_SUPPORT_URL + \
    '/client/supportrequests/conversation'

# Agreement Selling
SELLER_RESOURCE_AGREEMENT = CHAT_SUPPORT_URL + \
    '/resources/agreement'

GET_RESOURCE_AGREEMENT = CHAT_SUPPORT_URL + \
    '/resources/agreement/{reference_code}'

BUYER_RESOURCE_AGREEMENT_ACCEPT = CHAT_SUPPORT_URL + \
    '/resources/agreement/accept'

# General Search
SEARCH_ALL = API_BASE_URL + '/search'

# Contact Us
CONTACT_US = API_BASE_URL + '/support/mail'

# Count Execution
COUNT_EXEC = API_BASE_URL + '/pagemeta'

# Keywords
KEYWORDS = API_BASE_URL + '/keyword'

###############################################################################

# STAGING API

# Categories
# CATEGORY_ALL = STAGINGAPI_BASE_URL + '/categories'
# CATEGORY_ONE = STAGINGAPI_BASE_URL + '/categories/{category_id}'

# # Sub-Categories
# SUBCATEGORIES_ALL = STAGINGAPI_BASE_URL + '/categories/{category_id}' \
#     '/subcategories'
# SUBCATEGORIES_ONE = STAGINGAPI_BASE_URL + '/categories/{category_id}' \
#     '/subcategories/{subcategory_id}'

# # Users
# USERS_ONE = STAGINGAPI_BASE_URL + '/users/{user_id}'
# USER_LOGIN = STAGINGAPI_BASE_URL + '/users/login'
# USER_REGISTER = STAGINGAPI_BASE_URL + '/users/register'
# USER_ACTIVATE = STAGINGAPI_BASE_URL + '/activate'
# USER_PASSWORD = STAGINGAPI_BASE_URL + '/users/{user_id}/password'
# USER_FORGOT_PASSWORD = STAGINGAPI_BASE_URL + '/users/password/forgot/web'
# USER_RESET_PASSWORD = STAGINGAPI_BASE_URL + '/users/password/reset/web'
# USER_RESOURCE_ALL = STAGINGAPI_BASE_URL + '/users/{user_id}/resources'
# USER_RESOURCE_ONE = STAGINGAPI_BASE_URL + '/users/{user_id}' \
#     '/resources/{resource_id}'
# USER_RESOURCE_RESTORE = STAGINGAPI_BASE_URL + '/users/{user_id}' \
#     '/resources/{resource_id}/restore'
# USER_FAVORITE = STAGINGAPI_BASE_URL + '/users/{user_id}/resources/favorites'
# USER_TRANSACTIONS = STAGINGAPI_BASE_URL + '/users/{user_id}/transactions'
# USER_TRANSACTION_DETAIL = STAGINGAPI_BASE_URL + '/users/{user_id}' \
#     '/transactions/{transaction_id}'
# USER_TRANSACTIONS_SELLING = STAGINGAPI_BASE_URL + '/users/{user_id}' \
#     '/transactions/selling'
# USER_TRANSACTIONS_BUYING = STAGINGAPI_BASE_URL + '/users/{user_id}' \
#     '/transactions/buying'
# USER_TRANSACTION_RATE = STAGINGAPI_BASE_URL + '/users/{user_id}' \
#     '/transactions/{transaction_id}/rate'
# USER_TRANSACTION_ACCEPT = STAGINGAPI_BASE_URL + '/users/{user_id}' \
#     '/transactions/{transaction_id}'
# USER_TRANSACTION_REJECT = STAGINGAPI_BASE_URL + '/users/{user_id}' \
#     '/transactions/{transaction_id}/reject'
# USER_TRANSACTION_COMPLETE = STAGINGAPI_BASE_URL + '/users/{user_id}' \
#     '/transactions/{transaction_id}/complete'
# USER_MESSAGES = STAGINGAPI_BASE_URL + '/users/{user_id}/messages'
# USER_MESSAGE_THREAD = STAGINGAPI_BASE_URL + '/users/{user_id}/' \
#     'messages/{message_id}'
# USER_MESSAGE_REPLY = STAGINGAPI_BASE_URL + '/users/{user_id}' \
#     '/messages/{message_id}/reply'

# # FAQS
# FAQ_ALL = STAGINGAPI_BASE_URL + '/faqs'
# FAQ_ONE = STAGINGAPI_BASE_URL + '/faqs/{faq_id}'
# FAQ_QUESTION_ALL = STAGINGAPI_BASE_URL + '/faqs/{faq_id}/questions'
# FAQ_QUESTION_ONE = STAGINGAPI_BASE_URL + '/faqs/{faq_id}' \
#     '/questions/{question_id}'

# # Resources
# RESOURCE_ALL = STAGINGAPI_BASE_URL + '/resources'
# RESOURCE_ONE = STAGINGAPI_BASE_URL + '/resources/{resource_id}'
# RESOURCE_CATEGORIES = STAGINGAPI_BASE_URL + '/resources/category'
# RESOURCE_SUBCATEGORIES = STAGINGAPI_BASE_URL + '/resources/subcategory'
# RESOURCE_FAVORITE = STAGINGAPI_BASE_URL + \
#      '/resources/{resource_id}/favorites'
# RESOURCE_SEARCH = STAGINGAPI_BASE_URL + '/resources/search'

# # Company
# COMPANY_REGISTER = STAGINGAPI_BASE_URL + '/companies/register'

# # Resource image upload

# IMAGE_UPLOAD = STAGINGAPI_BASE_URL + '/upload/images'

# # Raise Support Request
# RAISE_SUPPORT = STAGINGAPI_BASE_URL + '/users/{user_id}/support/requests'
# TICKET_ALL = STAGINGAPI_BASE_URL + '/users/{user_id}/support/requests'

# # Wishlist
# WISHLIST_ALL = STAGINGAPI_BASE_URL + '/users/{user_id}/wishlists'
# WISHLIST_ONE = STAGINGAPI_BASE_URL + \
#       '/users/{user_id}/wishlists/{wishlist_id}'
# WISHLIST = API_BASE_URL + '/wishlists'
# WISHLIST_ITEM = API_BASE_URL + '/wishlists/{wishlist_id}'
