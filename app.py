from flask import Flask, g, render_template
from flask_migrate import Migrate
from flask_cors import CORS
from flask_apscheduler import APScheduler
from pytz import timezone

from exts import mail
import config
from models import *
from schedule_task import *
from bluePrints.user import bp as user_bp
from bluePrints.application import bp as application_bp

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
# 发送邮件初始化
mail.init_app(app)


# # 配置 APScheduler
# class Config:
#     SCHEDULER_API_ENABLED = True


# app.config.from_object(Config)
# # 定时任务初始化
# scheduler = APScheduler()
# scheduler.init_app(app)
# # 添加每日0:00执行任务
# scheduler.add_job(
#     id='update_login_state',  # 任务 ID
#     func=update_login_state,  # 任务函数
#     trigger='cron',  # 使用 cron 表达式
#     hour=12,  # 每天的 0 点
#     minute=52,  # 0 分
#     timezone=timezone('Asia/Shanghai')
# )
# # 启动定时任务调度器
# scheduler.start()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/test')
def test():
    return "success"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
else:
    application = app
