# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import TextAreaField
from wtforms import HiddenField
from wtforms.validators import InputRequired, Optional
from app.src.utils.helpers import profane_words


class SupportForm(FlaskForm):
    subject = StringField(validators=[
        InputRequired("Subject of the issue is required."),
        profane_words()])
    message = TextAreaField(validators=[
        InputRequired("A detailed description is required."),
        profane_words()])


class SupportMessageForm(FlaskForm):
    message = TextAreaField(validators=[Optional()])
    support_id = HiddenField(validators=[Optional()])

class SupportChatForm(FlaskForm):
    message = StringField(validators=[Optional()])
    reference_code = HiddenField(validators=[Optional()])
