from flask import request, jsonify, Blueprint
from extensions import db
from models import Student, StudentProfile
from datetime import datetime

student=Blueprint('student', __name__)


@student.route('/students', methods=['POST'])
def create_student():
    data=request.get_json()
    errors={}
    
    first_name=data.get('first_name',"").strip()
    last_name=data.get('last_name',"").strip()
    email=data.get('email',"").strip()
    
    if not first_name:
        errors['first_name']='Required.'
    if not last_name:
        errors['last_name']='Required.'
    if not email:
        errors['email']='Required.'
    if errors:
        return jsonify({'errors':errors}),400
    
    if Student.query.filter_by(email=email).first():
        return jsonify({'error':f"Email '{email}' is already in use."})
    
    student=Student(first_name=first_name, last_name=last_name, email=email)
    
    db.session.add(student)
    db.session.commit()
    
    return jsonify(student.to_dict()), 201

@student.route('/students', methods=['GET'])
def list_students():
    page=request.args.get('page', 1, type=int)
    per_page=request.args.get('per_page', 20, type=int)
    per_page=min(per_page, 100)
    
    pagination=Student.query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'student':[student.to_dict() for student in pagination.items],
        'total':pagination.total,
        'page':pagination.page,
        'pages':pagination.pages,
        'per_page':pagination.per_page
    }), 200

@student.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    student=db.session.get(Student, student_id)
    
    if not student:
        return jsonify({'error':'Student not found'}), 404
    
    return jsonify(student.to_dict()), 200


@student.route('/students/<int:student_id>', methods=['PUT'])
def update_studet(student_id):
    student=db.session.get(Student, student_id)
    
    if not student:
        return jsonify({'error':'Stundet not found'}), 404
    
    data=request.get_json()
    
    if 'fisrt_name' in data:
        student.first_name=data['first_name'].strip() or student.first_name 
    
    if 'last_name' in data:
        student.last_name=data['last_name'].strip() or student.last_name
    
    if 'email' in data:
        new_email=data['email'].strip()
        
        if new_email != student.email and Student.query.filter_by(email=new_email).first():
            return jsonify({'error':f"Email '{new_email}' is already in use."})
        
        student.email=new_email
    
    db.session.commit()
    return jsonify(student.to_dict()), 200   

@student.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    student=db.session.get(Student, student_id)
    
    if not student:
        return jsonify({'error':'Student not found'}),404
    
    db.session.delete(student)
    db.session.commit()
    return jsonify({'message':'Student deleted successfully!!'}), 200

@student.route('/students/<int:student_id>/profile', methods=['POST'])
def create_profile(student_id):
    student=db.session.get(Student, student_id)
    
    if not student:
        return jsonify({'error':'Student not found'}),404
    
    profile=student.profile
    
    if profile:
        return jsonify({'error':'this student already has profile'}), 409
    
    data=request.get_json()
    
    profile=StudentProfile(
        student_id=student_id,
        date_of_birth=data.get['date_of_birth'],
        phone=data.get['phone'],
        address=data.get['address'],
        bio=data.get['bio']
    )
    db.session.add(profile)
    db.session.commit()
    return jsonify(profile.to_dict()), 201
    
    
@student.route('/students/<int:student_id>/profile', methods=['GET'])
def get_profile(student_id):
    student=db.session.get(Student, student_id)
    
    if not student:
        return jsonify({'error':'Student not found'}),404
    
    profile=student.profile
    
    if not profile:
        return jsonify({'error':'No profile found for this student'}), 404
    
    return jsonify(profile.to_dict()), 200
            
@student.route('/students/<int:student_id>/profile', methods=['PUT'])
def update_profile(student_id):
    student=db.session.get(Student, student_id)
    
    if not student:
        return jsonify({'error':'Student not found'}),404
    
    
    if not student.profile:
        return jsonify({'error':'No profile found for this student'}), 404
    
    data=request.get_json()
    profile=student.profile
    
    if 'date_of_birth' in data:
        try:
            profile.date_of_birth = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error':'date_of_birth must be in YYYY-MM-DD format'}), 400
        
    if "phone" in data:
        profile.phone=data['phone'].strip() or profile.phone
    
    if "address" in data:
        profile.address=data['address'].strip() or profile.address
        
    if "bio" in data:
        profile.bio=data['bio'].strip() or profile.bio
        
    db.session.commit()
    return jsonify(profile.to_dict()), 200