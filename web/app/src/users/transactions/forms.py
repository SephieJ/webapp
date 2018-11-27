# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import IntegerField
from wtforms import TextAreaField
from wtforms import HiddenField
from wtforms.validators import InputRequired, Optional
from app.src.utils.helpers import profane_words


class AddTransactionForm(FlaskForm):
    quantity = IntegerField('qty',
                            validators=[InputRequired(
                                "Quantity is required.")])
    proposal = TextAreaField('proposal', validators=[Optional(), profane_words()])
    booking_date = StringField('booking_date',
                               validators=[InputRequired(
                                   "Booking date is required.")])


class RateTransactionForm(FlaskForm):
    message = StringField(validators=[InputRequired("Message is required."), profane_words()])
    rate = HiddenField(validators=[InputRequired("Rate is required.")])


class TransactionForm(FlaskForm):
    name = StringField()
    agreement_html = StringField()
    price = IntegerField()

class AgreementForm(FlaskForm):
    booking_reference_code = StringField()
    agreement_html = TextAreaField()
