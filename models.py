from datetime import date, datetime
from extentions import db


class Student(db.Model):
    __tablename__='students'
    
    id=db.Column(db.Integer, primary_key=True)
    first_name=db.Column(db.String(100),nullable=False)
    last_name=db.Column(db.String(100),nullable=False)
    email=db.Column(db.String(300),nullable=False, unique=True)
    enrollment_date=db.Column(db.Date,nullable=False, default=date.today)
    
   
    
    def to_dict(self, include_profile=False):
        data = {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "enrollment_date": self.enrollment_date.isoformat() if self.enrollment_date else None,
        }
            
        return data
        
class StudentProfile(db.Model):
    __tablename__='studentprofiles'
    
    id=db.Column(db.Integer, primary_key=True)
    date_of_birth=db.Column(db.Date, nullable=False)
    phone=db.Column(db.String(15),nullable=False)
    address=db.Column(db.String(500),nullable=True)
    bio=db.Column(db.Text,nullable=True)
    
    
    def to_dict(self):
        return{
            'id':self.id,
            'date_of_birth':self.date_of_birth.isoformate() if self.date_of_birth else None,
            'phone':self.phone,
            'address':self.address,
            'bio':self.bio
        }
        
class Department(db.Model):
    __tablename__='departments'
    
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(200),nullable=False)
    code=db.Column(db.String(20),nullable=False, unique=True)
    
    
    def to_dict(self):
        return{
            'id':self.id,
            'name':self.name,
            'code':self.code
        }
        
class Instructor(db.Model):
    __tablename__='instructors'
    
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    email=db.Column(db.String(300),nullable=False, unique=True)
        
    def to_dict(self):
        data={
            'id':self.id,
            'name':self.name,
            'email':self.email,
        }
            
        return data

class Course(db.Model):
    __tablename__='courses'
    
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    code=db.Column(db.String(20),nullable=False, unique=True)
    credits=db.Column(db.Integer,nullable=False)
    
    def to_dict(self):
        data={
            'id':self.id,
            'title':self.title,
            'code':self.code,
            'credits':self.credits
        }
        
        return data
    
class Enrollment(db.Model):
    __tablename__='enrollments'
    
    id=db.Column(db.Integer, primary_key=True)
    grade=db.Column(db.String(10),nullable=True)
    enrolled_at=db.Column(db.Datetime, nullable=False, default=datetime.utcnow)
    
    def to_dict(self):
        data={
            'id':self.id,
            'grade':self.grade,
            'enrolled_at':self.enrolled_at.isoformate() +'Z'if self.enrolled_at else None
        }

        return data