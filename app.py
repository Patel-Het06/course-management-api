from flask import Flask
from config import Config
from extensions import db
from routes import student

def create_app(config_class=Config):
    app=Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    
    app.register_blueprint(student)
    
    
    with app.app_context():
        db.create_all()
        
    return app

if __name__=='__main__':
    app=create_app()
    app.run(debug=True)