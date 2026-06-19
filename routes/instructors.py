from flask import Blueprint, request, jsonify
from extensions import db
from models import Instructor, Department

instructor=Blueprint('instructor', __name__)

# create new instructor

@instructor.route('/instructors', methods=['POST'])
def create_instructor():
    data=request.get_json()
    errors={}
    
    name=data.get('name').strip()
    email=data.get('email').strip()
    department_id=data.get('department_id')
    
    if not name:
        errors['name']='Required.'
    if not email:
        errors['email']='Required.'
    if not department_id:
        errors['department_id']='Required.'
    if errors:
        return jsonify({'errors':errors}), 400
    
    if not db.session.get(Department, department_id):
        return jsonify({'error':f"Department '{department_id}' not found."}), 404
       
    
    if Instructor.query.filter_by(email=email).first():
        return jsonify({'error':f"Email '{email}' is already in use."}), 409
    
    instructor=Instructor(name=name, email=email, department_id=department_id)
    
    db.session.add(instructor)
    db.session.commit()
    
    return jsonify(instructor.to_dict()), 201

# get list in instructors

@instructor.route('/instructors', methods=['GET'])
def list_instructor():
    page=request.args.get('page',1,type=int)
    per_page=request.args.get('per_page',20,type=int)
    per_page=min(per_page,100)
    
    pagination=Instructor.query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        "instructors":[ i.to_dict() for i in pagination.items],
        "total":pagination.total,
        'page':pagination.page,
        'pages':pagination.pages,
        'per_page':pagination.per_page
    }), 200
    
# get instructor by their id
    
@instructor.route('/instructors/<int:instructor_id>', methods=['GET'])
def get_instructor(instructor_id):
    instructor=db.session.get(Instructor, instructor_id)
    
    if not instructor:
        return jsonify({'error':f'Instructor {instructor_id} not found.'}), 404
    
    return jsonify(instructor.to_dict()), 200

# update instructor

@instructor.route('/instructors/<int:instructor_id>', methods=['PUT'])
def update_instructor(instructor_id):
    instructor=db.session.get(Instructor, instructor_id)
    
    if not instructor:
        return jsonify({'error':f'Instructor {instructor_id} not found.'}), 404
    
    data=request.get_json()
    
    if 'name' in data:
        instructor.name=data['name'].strip() or instructor.name
    
    if 'email' in data:
        new_email=data['email']
        
        if new_email != instructor.email and Instructor.query.filter_by(email=new_email).first():
             return jsonify({"error": f"Email '{new_email}' is already in use."}), 409
        
        instructor.email=new_email
        
    if 'department_id' in data:
        if not db.session.get(Department, data['department_id']):
            return jsonify({"error": f"Department {data['department_id']} not found."}), 404
        
        instructor.department_id=data['department_id']
    
    db.session.commit()
    
    return jsonify(instructor.to_dict()), 200

# delete instructor by their id

@instructor.route('/instructors/<int:instructor_id>', methods=['DELETE'])
def delete_instructor(instructor_id):
    instructor=db.session.get(Instructor, instructor_id)
    
    if not instructor:
        return jsonify({'error':f'Instructor {instructor_id} not found.'}), 404
    
    if instructor.courses:
        return jsonify({'error':"Cann't delete an instructor that still has courses."}), 409
    
    db.session.delete(instructor)
    db.session.commit()
    
    return jsonify(instructor.to_dict()), 200


# List courses taught by instructor  ONE <---> MANY: instructor to courses

@instructor.route('/instructors/<int:instructor_id>/courses',methods=['GET'])
def list_instructor_courses(instructor_id):
    instructor=db.session.get(Instructor, instructor_id)
    
    if not instructor:
        return jsonify({'error':f'Instructor {instructor_id} not found.'}), 404
    
    return jsonify({'courses':[c.to_dict() for c in instructor.courses]}), 200


    

        
    