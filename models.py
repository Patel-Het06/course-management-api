from datetime import date, datetime
from extensions import db


class Student(db.Model):
    __tablename__='students'
    
    id=db.Column(db.Integer, primary_key=True)
    first_name=db.Column(db.String(100),nullable=False)
    last_name=db.Column(db.String(100),nullable=False)
    email=db.Column(db.String(300),nullable=False, unique=True)
    enrollment_date=db.Column(db.Date,nullable=False, default=date.today)
    
    #one-one 
    profile=db.relationship('StudentProfile', backref='student', uselist=False, cascade='all, delete-orphan' )
    
    #many--many
    courses=db.relationship('Enrollment', backref='student', cascade='all, delete-orphan')
    
    def to_dict(self):
        return{
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "enrollment_date": self.enrollment_date.isoformat() if self.enrollment_date else None,
            'profile':self.profile.to_dict() if self.profile else None,
            'courses':[e.course.to_dict() for e in self.courses]
        }
        
class StudentProfile(db.Model):
    __tablename__='studentprofiles'
    
    id=db.Column(db.Integer, primary_key=True)
    student_id=db.Column(db.Integer,db.ForeignKey('students.id'),unique=True,nullable=False)
    date_of_birth=db.Column(db.Date, nullable=True)
    phone=db.Column(db.String(15),nullable=True)
    address=db.Column(db.String(500),nullable=True)
    bio=db.Column(db.Text,nullable=True)
    
    
    def to_dict(self):
        return{
            'id':self.id,
            'student_id':self.student_id,
            'date_of_birth':self.date_of_birth.isoformat() if self.date_of_birth else None,
            'phone':self.phone,
            'address':self.address,
            'bio':self.bio
        }
        
class Department(db.Model):
    __tablename__='departments'
    
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(200),nullable=False)
    code=db.Column(db.String(20),nullable=False, unique=True)
    
    #one--many 
    instructors=db.relationship('Instructor', backref='department', cascade='all, delete-orphan')
    
    #many--many
    courses=db.relationship('Course', backref='department')
    
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
    department_id=db.Column(db.Integer, db.ForeignKey('departments.id'),nullable=False)
    
    courses=db.relationship('Course', backref='instructor')
        
    def to_dict(self):
        return{
            'id':self.id,
            'name':self.name,
            'email':self.email,
            'department_id':self.department_id,
            'department': self.department.to_dict() if self.department else None
        }       

class Course(db.Model):
    __tablename__='courses'
    
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    code=db.Column(db.String(20),nullable=False, unique=True)
    credits=db.Column(db.Integer,nullable=False)
    department_id=db.Column(db.Integer, db.ForeignKey('departments.id'),nullable=False)
    instructor_id=db.Column(db.Integer, db.ForeignKey('instructors.id'), nullable=False)
    
    
    enrollments=db.relationship('Enrollment', backref='course', cascade='all, delete-orphan')
    
    def to_dict(self):
        return{
            'id':self.id,
            'title':self.title,
            'code':self.code,
            'credits':self.credits,
            'department_id':self.department_id,
            'instructor_id':self.instructor_id,
            'department': self.department.to_dict() if self.department else None,
            'instructor': self.instructor.to_dict() if self.instructor else None
        }
               
class Enrollment(db.Model):
    __tablename__='enrollments'
    
    id=db.Column(db.Integer, primary_key=True)
    student_id=db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    course_id=db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    grade=db.Column(db.String(10),nullable=True)
    enrolled_at=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    __table_args__=(db.UniqueConstraint('student_id','course_id', name='uq_student_course'),)

    
    def to_dict(self):
        return{
            'id':self.id,
            'student_id':self.student_id,
            'course_id':self.course_id,
            'grade':self.grade,
            'enrolled_at':self.enrolled_at.isoformat() if self.enrolled_at else None
        }