import os

basedir=os.path.abspath(os.path.dirname(__file__))

class Config():
    SECRET_KEY='mykey'
    SQLALCHEMY_DATABASE_URI='sqlite:///'+ os.path.join(basedir, 'course_management.db')
    SQLALCHEMY_TACK_MODIFICATIONS= False
    JSON_SORT_KEYS = False  
    