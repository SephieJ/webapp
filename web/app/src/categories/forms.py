# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import FileField
from wtforms.validators import InputRequired
from wtforms.validators import Optional
from app.src.utils.helpers import profane_words


class AddCategoryForm(FlaskForm):
    name = StringField(validators=[
        InputRequired("Category Name is required"), profane_words()])
    description = StringField(validators=[
        InputRequired("Category Description is required"), profane_words()])


class AddSubCategoryForm(FlaskForm):
    name = StringField(validators=[
        InputRequired("Sub-Category Name is required"), profane_words()])
    description = StringField(validators=[
        InputRequired("Sub-Category Description is required"), profane_words()])
    image_url = FileField(validators=[Optional()])
