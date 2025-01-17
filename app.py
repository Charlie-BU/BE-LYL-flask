from flask import Flask, render_template
from flask_migrate import Migrate
from flask_cors import CORS
from flask_apscheduler import APScheduler
from pytz import timezone

from exts import mail
import config
from models import *
from schedule_tasks import *
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

# 配置APScheduler
app.config['SCHEDULER_API_ENABLED'] = True  # 启用任务管理 API
scheduler = APScheduler()
# APScheduler初始化
scheduler.init_app(app)

# 添加每日0:00执行任务
scheduler.add_job(
    id='update_active_score',
    func=update_active_score,
    trigger='cron',
    hour=0,
    minute=0,
    timezone=timezone('Asia/Shanghai')
)
scheduler.add_job(
    id='update_all_users_star',
    func=update_all_users_star,
    trigger='cron',
    hour=0,
    minute=10,
    timezone=timezone('Asia/Shanghai')
)
scheduler.add_job(
    id='delete_outdated_items',
    func=delete_outdated_items,
    trigger='cron',
    hour=1,
    minute=0,
    timezone=timezone('Asia/Shanghai')
)
# 启动定时任务调度器
scheduler.start()


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
