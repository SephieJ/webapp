# -*- coding: utf-8 -*-

from sqlalchemy.exc import InvalidRequestError
from models import User
from app.src.utils.database import SessionDB


def get(user_id):
    db_session = SessionDB
    try:
        db_session.rollback()
        results = db_session.query(User).filter(User.id == user_id).first()
        db_session.close()
    except InvalidRequestError:
        db_session.rollback()
        db_session.close()
    return results


def add(user):
    db_session = SessionDB()
    db_session.add(user)
    db_session.commit()
    db_session.close()
    return True


def update(user):
    db_session = SessionDB()
    updated_user = (
        db_session.query(User)
        .filter(User.id == user.id)
        .filter(User.deleted_date.is_(None))
        .first()
        # .execute('SET NAMES utf8mb4')
        # .execute("SET CHARACTER SET utf8mb4")
        # .execute("SET character_set_connection=utf8mb4")
    )
    updated_user.account_id = user.account_id
    updated_user.first_name = user.first_name
    updated_user.last_name = user.last_name
    updated_user.email = user.email
    updated_user.birth_date = user.birth_date
    updated_user.description = user.description
    updated_user.designation = user.designation
    updated_user.landline_number = user.landline_number
    updated_user.mobile_number = user.mobile_number
    updated_user.image_url = user.image_url
    updated_user.status = user.status
    updated_user.is_subscribed = user.is_subscribed
    db_session.commit()
    db_session.close()
    return True
