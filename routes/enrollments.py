from flask import Blueprint, request, jsonify
from extensions import db
from models import Enrollment, Student, Course

enrollment=Blueprint('enrollment', __name__)

# enrolled student into course

@enrollment.route('/enrollments', methods=['POST'])
def create_enrollment():
    data=request.get_json()
    errors={}
    
    student_id=data.get('student_id')
    course_id=data.get('course_id')
    
    if not student_id:
        errors['student_id']='Required.'
    if not course_id:
        errors['course_id']='Required.'
    if errors:
        return jsonify({'errors':errors}), 400
    
    if not db.session.get(Student, student_id):
        return jsonify({'error':f'Student {student_id} not found'}), 404
    if not db.session.get(Course, course_id):
        return jsonify({'error':f'Course {course_id} not found'}), 404
    
    if Enrollment.query.filter_by(student_id=student_id, course_id=course_id).first():
        return jsonify({"error":"Student already enrolled in this course."}), 409
    
    enrollment=Enrollment(student_id=student_id, course_id=course_id)
    
    db.session.add(enrollment)
    db.session.commit()
    
    return jsonify(enrollment.to_dict()), 201

# list of enrollments 

@enrollment.route('/enrollments', methods=['GET'])
def list_enrollment():
    enrollments=Enrollment.query.all()
    
    return jsonify({"enrollments":[e.to_dict() for e in enrollments]}), 200

# get of enrollment by their id

@enrollment.route('/enrollments/<int:enrollment_id>', methods=['GET'])
def get_enrollment(enrollment_id):
    enrollment=db.session.get(Enrollment, enrollment_id)
    
    if not enrollment:
        return jsonify({"error":"Enrollment not found."}), 404
    
    return jsonify(enrollment.to_dict()), 200

# update grade of course by enrollment_id

@enrollment.route('/enrollments/<int:enrollment_id>', methods=['PUT'])
def update_enrollment(enrollment_id):
    enrollment=db.session.get(Enrollment, enrollment_id)
    
    if not enrollment:
        return jsonify({"error":"Enrollment not found."}), 404
    
    data=request.get_json()
    
    if "grade" in data:
        enrollment.grade=data['grade']
        
    db.session.commit()
    
    return jsonify(enrollment.to_dict()), 200

# delete enrollment

@enrollment.route('/enrollments/<int:enrollment_id>', methods=['DELETE'])
def delete_enrollment(enrollment_id):
    enrollment=db.session.get(Enrollment, enrollment_id)
    
    if not enrollment:
        return jsonify({"error":"Enrollment not found."}), 404
    
    db.session.delete(enrollment)
    db.session.commit()
    
    return jsonify({"message": "Enrollment removed."}), 200

# List courses a student is enrolled in	   many <--> many

@enrollment.route('/students/<int:student_id>/courses', methods=['GET'])
def list_student_course(student_id):
    student=db.session.get(Student, student_id)
    
    if not student:
        return jsonify({'error':'Student not found.'}), 404
    
    courses=[
        {**e.course.to_dict(), 'grade':e.grade, 'enrolled_at':e.enrolled_at.isoformat()}
        for e in student.courses
    ]
    
    return jsonify({'courses':courses}), 200

#  List students enrolled in a course	  many <--> many

@enrollment.route('/courses/<int:course_id>/students', methods=['GET'])
def list_course_student(course_id):
    course=db.session.get(Course, course_id)
    
    if not course:
        return jsonify({'error':'Course not found.'}), 404
    
    students=[
        {**e.student.to_dict(), "grade":e.grade, "enrolled_at":e.enrolled_at.isoformat()}
        for e in course.enrollments
    ]
    
    return jsonify({'students':students}), 200

    
    




    
    
    
    