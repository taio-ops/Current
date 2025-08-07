from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()  # Initialize without app

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/testdb'

    app.secret_key = 'SOME KEY'

    db.init_app(app)
    migrate.init_app(app, db)  # Set up here

    login_manager = LoginManager()
    login_manager.init_app(app)

    from dbapplication.models import User
    
    @login_manager.user_loader
    def load_user(uid):
        return User.query.get(uid)
    
    bcrypt = Bcrypt(app)
   
    from dbapplication.routes import register_routes
    register_routes(app, db, bcrypt)

    return app
