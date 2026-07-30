from flask_sqlalchemy import SQLAlchemy
database = SQLAlchemy()
def init_database(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Acervo.db"

    
    with app.app_context():
        database.init_app(app)  
        database.create_all() 
