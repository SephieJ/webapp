# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import TextAreaField
from wtforms.validators import InputRequired, Email
from app.src.utils.helpers import profane_words


class ContactForm(FlaskForm):
    name = StringField(validators=[
        InputRequired('Full Name is required.'),
        profane_words()])
    email = StringField(validators=[
        InputRequired('Email Address is required.'),
        Email('Please enter a valid email address.'),
        profane_words()])
    message = TextAreaField(validators=[
        InputRequired('Message is required'),
        profane_words()])
