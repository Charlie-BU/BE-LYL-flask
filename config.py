test = False
# 数据库配置
USERNAME = "Charlie"
PASSWORD = "liyilian666"
HOSTNAME = "101.132.24.99"
PORT = 3306
DATABASE = "liyilian-test" if test else "liyilian"
DB_URI = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4'
SQLALCHEMY_DATABASE_URI = DB_URI

SECRET_KEY = "qwfsdgkdfhkbld"

# 邮箱配置
MAIL_SERVER = ""  # 邮件服务器地址
MAIL_USE_SSL = True
MAIL_PORT = 465  # 邮件服务器端口
MAIL_USERNAME = ""  # 发件邮箱
MAIL_PASSWORD = ""  # 授权码
MAIL_DEFAULT_SENDER = ""


# 小程序配置
APPID = "wx89661193f664f803"
APPSECRET = ""

# 微信支付配置
MCH_ID = ''                                   # 商户号
NOTIFY_URL = ''     # 通知地址
MERCHANT_KEY = ''       # 商户KEY
# TRADE_TYPE = 'JSAPI'                                    # 交易类型
