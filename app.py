from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from routes import *
from models import User, Post

@app.cli.command("init-db")
def init_db():
    db.create_all()
    
    # 创建管理员用户
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(username='admin')
        admin.set_password('password')
        db.session.add(admin)
        db.session.commit()
        print("管理员用户已创建。")
    
    print("数据库表已创建。")

if __name__ == '__main__':
    app.run(debug=True)

