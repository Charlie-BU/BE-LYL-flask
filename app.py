from flask import Flask, request, redirect, url_for, session, g, render_template, jsonify
from sqlalchemy.testing.pickleable import User

from exts import db, mail
import config, datetime
from models import *
from bluePrints.user import bp as user_bp
from bluePrints.application import bp as application_bp
from flask_migrate import Migrate
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
# 加载配置
app.config.from_object(config)
# 注册蓝图
app.register_blueprint(user_bp)
app.register_blueprint(application_bp)
# 绑定数据库
db.init_app(app)
migrate = Migrate(app, db)
# 添加数据库表
# with app.app_context():
#     db.create_all()
# 发送邮件初始化
mail.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')


# 请求前检查是否有用户登录
@app.before_request
def my_before_request():
    user_id = session.get("user_id")
    if user_id:
        user = User.query.get(user_id)
        setattr(g, "user", user)
    else:
        setattr(g, "user", None)


@app.context_processor
def my_context_processor():
    return {"user": g.user}


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
else:
    application = app
