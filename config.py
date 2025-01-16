test = True
# 数据库配置
USERNAME = "Charlie"
PASSWORD = "liyilian666"
HOSTNAME = "101.132.24.99" if test else "localhost"
PORT = 3306
# DATABASE = "liyilian-test" if test else "liyilian"
DATABASE = "liyilian"
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
APPSECRET = "69fd5a49894dc45b242f48a2ea3afc4f"

# 微信支付配置
MCH_ID = ''                                   # 商户号
NOTIFY_URL = ''     # 通知地址
MERCHANT_KEY = ''       # 商户KEY
# TRADE_TYPE = 'JSAPI'                                    # 交易类型


# 阿里云OSS配置
OSS_ACCESS_KEY_ID = 'LTAI5tRmNY2Aa1MZb1PK49Hg'
OSS_ACCESS_KEY_SECRET = 'd4GH1DVJKhEX4ZXY5lEVNEFP31sn3z'
OSS_BUCKET_NAME = 'liyilian'
OSS_ENDPOINT = 'oss-cn-hangzhou.aliyuncs.com'       # 不能带liyilian.*
