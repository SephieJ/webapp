# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import TextAreaField
from wtforms import FileField
from wtforms import IntegerField
from wtforms import DecimalField
from wtforms import SelectField
from wtforms import BooleanField
from wtforms import RadioField
from wtforms import DateField
from wtforms.validators import InputRequired, Optional, Length
from app.src.utils.helpers import profane_words


class AddResourceForm(FlaskForm):
    name = StringField(validators=[
        InputRequired('Item name is required.'),
        profane_words()])
    description = TextAreaField(validators=[
        InputRequired('Short description is required.'),
        profane_words()])
    quantity = IntegerField(validators=[
        InputRequired('Quantity is required.')])
    price = DecimalField(validators=[
        InputRequired('Product price is required.')])
    # rates = RadioField(choices=[
    #     ('QTY', 'Per Quantity'),
    #     ('HOUR', 'Per Hour'),
    #     ('DAY', 'Per Day'),
    #     ('WEEK', 'Per Week'),
    #     ('MONTH', 'Per Month')],
    #     default='QTY', validators=[InputRequired()])
    unit = SelectField(validators=[
        InputRequired('Unit of Measurement is required.')],
        choices=[('QTY', 'Per Quantity'),
                 ('HOUR', 'Per Hour'),
                 ('DAY', 'Per Day'),
                 ('WEEK', 'Per Week'),
                 ('MONTH', 'Per Month')])
    booking_holiday = RadioField(choices=[
        ('Yes', 'Yes'),
        ('No', 'No')],
        default='No', validators=[InputRequired()])
    availability = RadioField(choices=[
        ('Yes', 'Yes'),
        ('No', 'No')],
        default='Yes', validators=[InputRequired()])
    retain = RadioField(choices=[
        ('Yes', 'Yes'),
        ('No', 'No')],
        default='Yes', validators=[InputRequired()])

    # Date Availability
    avail_from = DateField(format='%d-%m-%Y', validators=[
        Optional()])
    avail_to = DateField(format='%d-%m-%Y', validators=[
        Optional()])

    # Booking Days
    monday = BooleanField('Mon',
                          validators=[Optional()],
                          default='checked')
    tuesday = BooleanField('Tue',
                           validators=[Optional()],
                           default='checked')
    wednesday = BooleanField('Wed',
                             validators=[Optional()],
                             default='checked')
    thursday = BooleanField('Thu',
                            validators=[Optional()],
                            default='checked')
    friday = BooleanField('Fri',
                          validators=[Optional()],
                          default='checked')
    saturday = BooleanField('Sat',
                            validators=[Optional()])
    sunday = BooleanField('Sun',
                          validators=[Optional()])
    select_all = BooleanField('All',
                              validators=[Optional()])

    # Availability in Minutes
    avail_mins_from = StringField('minutes', validators=[
                                  Optional(),
                                  Length(min=1, max=4)],
                                  default=60)
    avail_mins_to = StringField('minutes', validators=[
                                Optional(),
                                Length(min=1, max=4)])

    # Scheduling Time
    sched_time_from = StringField(validators=[Optional()])
    sched_time_to = StringField(validators=[Optional()])

    suggest_checkbox = BooleanField('Suggest Category',
                                    validators=[Optional()])
    parent_category = StringField(validators=[Optional()])
    subcategory = StringField(validators=[Optional()])
    image_url = FileField(validators=[Optional()])
    unit_number = StringField(validators=[Optional()])
    street = StringField(validators=[Optional()])
    zipcode = StringField(validators=[Optional()])
    city = StringField(validators=[Optional()])
    state = StringField(validators=[Optional()])


class WishlistForm(FlaskForm):
    suggest_checkbox = BooleanField('Suggest Category',
                                    validators=[Optional()])
    parent_category = StringField(validators=[Optional()])
    name = StringField(validators=[
        InputRequired('Item name is required.'),
        profane_words()])
    subcategory = StringField(validators=[Optional()])
    description = TextAreaField(validators=[
        InputRequired('Short description is required.'),
        profane_words()])
