# -*- coding: utf-8 -*-

import bleach
import os
import string
import random
import requests
from flask import flash, current_app as app
from werkzeug.utils import secure_filename
from app.src.utils import constants
from wtforms.validators import ValidationError


def special_chars():
    message = 'Special characters are not allowed.'

    def _special_chars(form, field):
        invalidChars = string.punctuation
        word = field.data
        if any(char in invalidChars for char in word):
            raise ValidationError(message)

    return _special_chars


def sg_mobile_number():
    message = 'Wrong format for mobile number.'

    def _sg_mobile_number(form, field):
        mobile_number = field.data
        if not mobile_number.startswith(('8', '9')):
            raise ValidationError(message)

    return _sg_mobile_number


def sg_office_number():
    message = 'Wrong format for office number.'

    def _sg_office_number(form, field):
        office_number = field.data
        if not office_number.startswith(('6')):
            raise ValidationError(message)

    return _sg_office_number


def profane_words():
    message = 'Profane words are not acceptable.'

    def _profane_words(form, field):
        profane = field.data
        profanity_url = constants.PROFANITY_URL
        profanity_check = requests.post(
            profanity_url, data={"words": profane})
        profanity_obj = profanity_check.json()
        if profanity_obj["status"] == "invalid":
            profane = profanity_obj["message"]
            raise ValidationError(message)
    return _profane_words


def sanitize(inputs):
    sanitized = {}
    for item in inputs:
        # Check if the data is inn/float since bleach convert numeric to string
        if isinstance(inputs[item], (int, float, long)) is True:
            sanitized[item] = inputs[item]
        else:
            sanitized[item] = bleach.clean(inputs[item]).strip()
    return sanitized


def flash_errors(form):
    # Flashes form errors
    for field, errors in form.errors.items():
        for error in errors:
            flash(error)


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


def upload(image):
    if image and allowed_file(image.filename):
        # Make the filename safe, remove unsupported characters
        image_name = secure_filename(image.filename)
        # Move the file from the temporal folder to the upload folder we set up
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_name))
        return constants.IMAGE_UPLOAD_DIR + image_name


def generate_random_chars(char_count):
    char_set = string.ascii_uppercase
    random_string = ''.join(random.sample(char_set * char_count, char_count))
    return random_string
