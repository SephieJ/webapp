# -*- coding: utf-8 -*-

import dateutil.parser
from sqlalchemy import (Boolean, Column, Integer, String, Date, DateTime,
                        Unicode)
from app.src.utils.database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=False)
    account_id = Column(String(255), nullable=False)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=True)
    email = Column(String(255), nullable=False)
    birth_date = Column(Date, nullable=True)
    description = Column(Unicode(2, collation='utf8mb4'),
                         nullable=True)
    designation = Column(String(255), nullable=True)
    landline_number = Column(String(255), nullable=True)
    mobile_number = Column(String(255), nullable=True)
    image_url = Column(String(255), nullable=True)
    status = Column(String(255), nullable=True)
    is_subscribed = Column(Boolean(), nullable=True)
    created_date = Column(DateTime, nullable=False)
    updated_date = Column(DateTime, nullable=True)
    deleted_date = Column(DateTime, nullable=True)

    # Company
    co_name = Column(String(255), nullable=True)
    co_info = Column(Unicode(2, collation='utf8mb4'),
                     nullable=True)
    co_business_reg_number = Column(String(255), nullable=True)
    co_office_number = Column(String(255), nullable=True)
    co_mobile_number = Column(String(255), nullable=True)

    def __init__(self, data):
        self.id = data['id']
        self.account_id = data['account_id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.description = data['description']
        self.designation = data['designation']
        self.landline_number = data['landline_number']
        self.mobile_number = data['mobile_number']
        self.image_url = data['image_url']
        self.status = data['status']
        self.is_subscribed = data['is_subscribed']

        # Company
        if data['company'] is not None:
            self.co_name = data['company']['name']
            self.co_info = data['company']['company_info']
            self.co_business_reg_number = data['company']['business_reg_number']
            self.co_office_number = data['company']['office_number']
            self.co_mobile_number = data['company']['mobile_number']

        if data['birth_date'] is not None:
            if isinstance(data['birth_date'], (str, unicode)):
                self.birth_date = dateutil.parser.parse(data['birth_date'])
            else:
                self.birth_date = data['birth_date']
        else:
            self.birth_date = None

        if data['created_date'] is not None:
            if isinstance(data['created_date'], (str, unicode)):
                self.created_date = dateutil.parser.parse(data['created_date'])
            else:
                self.created_date = data['created_date']
        else:
            self.created_date = None

        if data['updated_date'] is not None:
            if isinstance(data['updated_date'], (str, unicode)):
                self.updated_date = dateutil.parser.parse(data['updated_date'])
            else:
                self.updated_date = data['updated_date']
        else:
            self.updated_date = None

        if data['deleted_date'] is not None:
            if isinstance(data['deleted_date'], (str, unicode)):
                self.deleted_date = dateutil.parser.parse(data['deleted_date'])
            else:
                self.deleted_date = data['deleted_date']
        else:
            self.deleted_date = None

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'account_id': self.account_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'birth_date': self.birth_date,
            'description': self.description,
            'designation': self.designation,
            'landline_number': self.landline_number,
            'mobile_number': self.mobile_number,
            'image_url': self.image_url,
            'status': self.status,
            'is_subscribed': self.is_subscribed,
            'created_date': self.created_date,
            'updated_date': self.updated_date,
            'deleted_date': self.deleted_date,
            'co_name': self.co_name,
            'co_info': self.co_info,
            'co_business_reg_number': self.co_business_reg_number,
            'co_office_number': self.co_office_number,
            'co_mobile_number': self.co_mobile_number,
        }
