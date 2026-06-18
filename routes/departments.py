from flask import request, jsonify, Blueprint
from extensions import db
from models import Department, Course

department=Blueprint('department', __name__)

# create new department

@department.route('/department', methods=['POST'])
def create_department():
    data=request.get_json()
    errors={}
    
    name=data.get('name',"").strip()
    code=data.get('code',"").strip()
    
    if not name:
        errors['name']='Required.'
    if not code:
        errors['code']='Required.'
    if errors:
        return jsonify({'errors':errors}), 400
    
    if Department.query.filter_by(code=code).first():
        return jsonify({'error':f"Derpartment code '{code}' is already in use."}), 409
    
    department=Department(name=name, code=code)
    
    db.session.add(department)
    db.session.commit()
    
    return jsonify(department.to_dict()), 201

# list of department

@department.route('/department', methods=['GET'])
def list_department():
    departments=Department.query.all()
    
    return jsonify([d.to_dict() for d in departments]), 200

# get department by id

@department.route('/department/<int:department_id>', methods=['GET'])
def get_department(department_id):
    department=db.session.get(Department, department_id)
    
    if not department:
        return jsonify({'error':'Department not found'}), 404
    
    return jsonify(department.to_dict()), 200

# update department by id

@department.route('/department/<int:department_id>', methods=['PUT'])
def update_department(department_id):
    department=db.session.get(Department, department_id)
    
    if not department:
        return jsonify({'error':'Department not found'}), 404
    
    data=request.get_json()
    
    if 'name' in data:
        department.name=data['name'].strip() or department.name
    
    if 'code' in data:
        new_code=data['code'].strip()
        
        if new_code != department.code and Department.query.filter_by(code=new_code).first():
            return jsonify({'error':f"Department code '{new_code}' is already in use."}), 409   
        
        department.code=new_code
        
    db.session.commit()
    return jsonify(department.to_dict()), 200

# delete department by id

@department.route('/department/<int:department_id>', methods=['DELETE'])
def delete_department(department_id):
    department=db.session.get(Department, department_id)
    
    if not department:
        return jsonify({'error':'Department not found'}), 404
    
    db.session.delete(department)
    db.session.commit()
    
    return jsonify({'message':f'{department.name} department successfully deleted.'}), 200

#  list courses by department id 

@department.route('/department/<int:department_id>/courses', methods=['GET'])
def list_courses(department_id):
    department=db.session.get(Department, department_id)
    
    if not department:
        return jsonify({'error':'Department not found'}), 404
    
    return jsonify([c.to_dict() for c in department.courses]), 200