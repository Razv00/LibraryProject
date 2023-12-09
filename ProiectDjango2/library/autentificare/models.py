from django.db import models

from .Database.OracleDB import OracleDB

# Create your models here.
from . import db


class CustomUser():
    def __init__(self, _id=None, name=None, password=None):
        self._id = _id
        self.name = name
        self.password = password

    @classmethod
    def create(cls, name, password, ):
        new_user = cls(name=name, password=password)
        new_user.insertIntoDb()
        return new_user

    def insertIntoDb(self):
        db.insertUserWithModel(name=self.name,
                               password=self.password,
                               )

    @staticmethod
    def getByName(name):
        user_data = db.users.getUserDataByName(name)
        if user_data:
            user = CustomUser(_id=user_data[0], name=user_data[1], password=user_data[3])
            return user
        else:
            return None

    def loadUserDataByName(self):
        user_data = db.users.getUserDataByName(self.name)
        if user_data is not None:
            self.name = user_data['name']
            self.password = user_data['password']

    @staticmethod
    def get(user_id):
        if user_id == 'None':
            return None

        user_data = db.getUserDataById(user_id)
        if user_data:
            user = CustomUser(_id=user_data[0], name=user_data[1], password=user_data[2])
            return user
        else:
            return None
