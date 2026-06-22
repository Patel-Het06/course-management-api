from flask import Blueprint, request, jsonify
from extensions import db
from models import Course, Department, Instructor

course=Blueprint('course', __name__)

# create new course

@course.route('/courses', methods=['POST'])
def create_corse():
    data=request.get_json()
    errors={}
    
    title=data.get('title',"").strip()
    code=data.get('code',"").strip().upper()
    credits=data.get('credits')
    department_id=data.get('department_id')
    instructor_id=data.get('instructor_id')
    
    if not title:
        errors['title']='Required.'
    if not code:
        errors['code']='Required.'
    if credits is None:
        errors['credits']='Required.'
    elif not isinstance(data['credits'], int) or credits<1:
        errors['credits']='Must be positive integer.'
    if not department_id:
         errors['department_id']='Required.'
    if not instructor_id:
        errors['instructor_id']='Required.'
    if errors:
        return jsonify({'errors':errors}), 400
    
    if not db.session.get(Department, department_id):
        return jsonify({'error':f'Department {department_id} not found!'}), 404
    if not db.session.get(Instructor, instructor_id):
        return jsonify({'error':f'Instructor {instructor_id} not found!'}), 404
    
    if Course.query.filter_by(code=code).first():
        return jsonify({"error":f"Course code '{code}' already in use."}), 409
    
    course=Course(title=title, code=code, credits=credits, department_id=department_id, instructor_id=instructor_id)
    
    db.session.add(course)
    db.session.commit()
    
    return jsonify(course.to_dict()), 201

# list courses and use dpartment_id 

@course.route('/courses', methods=['GET'])
def list_courses_department():
    department_id=request.args.get("department_id", type=int)
    
    query=Course.query
    
    if department_id:
        department=db.session.get(Department, department_id)
        
        if not department:
            return jsonify({'error': f'Department {department_id} not found'}), 404

        query=query.filter_by(department_id=department_id)
        
    return jsonify({'Courses':[c.to_dict() for c in query.all()]}), 200

# get courses by their id

@course.route('/courses/<int:course_id>', methods=['GET'])
def get_course(course_id):
    course=db.session.get(Course, course_id)
    
    if not course:
        return jsonify({'error':'Course not found!'}), 404
    
    return jsonify(course.to_dict()), 200

# update course 

@course.route('/courses/<int:course_id>', methods=['PUT'])
def update_course(course_id):
    course=db.session.get(Course, course_id)
    
    if not course:
        return jsonify({'error':'Course not found!'}), 404
    
    data=request.get_json()
    
    if 'title' in data:
        course.title=data['title'].strip() or course.title
        
    if 'code' in data:
        new_code=data['code'].strip().upper()
        
        if new_code != course.code and Course.query.filter_by(code=new_code).first():
            return jsonify({'error': f"Course code '{new_code}' already exists."}), 409
        
        course.code=new_code
        
    if 'credits' in data:
        if not isinstance(data['credits'], int) or data['credits'] < 1:
            return jsonify({'error':'Credits must be positive integer.'}), 400  
        course.credits=data['credits']
        
    if 'department_id' in data:
        if not db.session.get(Department, data['department_id']):
            return jsonify({'error':f"Department {data['department_id']} not found"}), 404
        
        course.department_id=data['department_id']
    
    if 'instructor_id' in data:
        if not db.session.get(Instructor, data['instructor_id']):
            return jsonify({'error':f"Instructoe {data['instructor_id']} not found"}), 404
        
        course.instructor_id=data['instructor_id']
    
    db.session.commit()
    
    return jsonify(course.to_dict()), 200

# delete course by their id

@course.route('/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    course=db.session.get(Course, course_id)
    
    if not course:
        return jsonify({'error':'Course not found!'}), 404
    
    db.session.delete(course)
    db.session.commit()
    
    return jsonify(course.to_dict()), 200