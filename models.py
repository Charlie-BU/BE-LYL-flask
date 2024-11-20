# coding: utf-8
from datetime import datetime
from exts import db


class TpAccountLog(db.Model):
    __tablename__ = 'tp_account_log'

    log_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    gid = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    money = db.Column(db.Numeric(15, 4), server_default=db.FetchedValue())
    type = db.Column(db.Integer, server_default=db.FetchedValue())
    add_time = db.Column(db.Integer, nullable=False)
    desc = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    order_sn = db.Column(db.String(50))
    order_id = db.Column(db.Integer)
    pick_order_id = db.Column(db.Integer)
    wid = db.Column(db.Integer, server_default=db.FetchedValue())
    is_ywy = db.Column(db.Integer, server_default=db.FetchedValue())


class TpAd(db.Model):
    __tablename__ = 'tp_ad'

    ad_id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    ad_name = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    ad_type = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    ad_link = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    image = db.Column(db.Text, nullable=False)
    video = db.Column(db.Text)
    click_count = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    open = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    sort = db.Column(db.Integer, server_default=db.FetchedValue())
    target = db.Column(db.Integer, server_default=db.FetchedValue())
    add_time = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())


class TpAdmin(db.Model):
    __tablename__ = 'tp_admin'

    admin_id = db.Column(db.SmallInteger, primary_key=True)
    user_name = db.Column(db.String(60), nullable=False, index=True, server_default=db.FetchedValue())
    email = db.Column(db.String(60), server_default=db.FetchedValue())
    password = db.Column(db.String(32), nullable=False, server_default=db.FetchedValue())
    ec_salt = db.Column(db.String(10))
    add_time = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    last_login = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    last_ip = db.Column(db.String(15), nullable=False, server_default=db.FetchedValue())
    nav_list = db.Column(db.Text)
    role_id = db.Column(db.SmallInteger, server_default=db.FetchedValue())


class TpAdminLog(db.Model):
    __tablename__ = 'tp_admin_log'

    log_id = db.Column(db.BigInteger, primary_key=True)
    admin_id = db.Column(db.Integer)
    log_info = db.Column(db.String(255))
    log_ip = db.Column(db.String(30))
    log_url = db.Column(db.String(50))
    log_time = db.Column(db.Integer)


class TpAdminRole(db.Model):
    __tablename__ = 'tp_admin_role'

    role_id = db.Column(db.SmallInteger, primary_key=True)
    role_name = db.Column(db.String(30))
    act_list = db.Column(db.Text)
    role_desc = db.Column(db.String(255))


class TpConfig(db.Model):
    __tablename__ = 'tp_config'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    value = db.Column(db.String(512))
    inc_type = db.Column(db.String(64))
    desc = db.Column(db.String(50))


class TpContract(db.Model):
    __tablename__ = 'tp_contract'

    id = db.Column(db.Integer, primary_key=True)
    order_sn = db.Column(db.String(255, 'utf8mb4_bin'))
    name = db.Column(db.String(255, 'utf8mb4_bin'))
    user_idj = db.Column(db.Integer, server_default=db.FetchedValue())
    user_idjtype = db.Column(db.Integer, server_default=db.FetchedValue())
    user_idy = db.Column(db.Integer, server_default=db.FetchedValue())
    user_idytype = db.Column(db.Integer, server_default=db.FetchedValue())
    user_idb = db.Column(db.String(255, 'utf8mb4_bin'), server_default=db.FetchedValue())
    add_time = db.Column(db.Integer)
    update_time = db.Column(db.Integer)
    src = db.Column(db.Text(collation='utf8mb4_bin'))
    pay_countpt = db.Column(db.Integer, server_default=db.FetchedValue())
    pay_pricept = db.Column(db.Numeric(10, 2), server_default=db.FetchedValue())
    pay_countyf = db.Column(db.Integer, server_default=db.FetchedValue())
    pay_priceyf = db.Column(db.Numeric(10, 2), server_default=db.FetchedValue())


class TpEssay(db.Model):
    __tablename__ = 'tp_essay'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False, server_default=db.FetchedValue())
    cat_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    description = db.Column(db.Text)
    image = db.Column(db.String(255), server_default=db.FetchedValue())
    video = db.Column(db.Text)
    content = db.Column(db.Text, nullable=False)
    sort = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    open = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    add_time = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    update_time = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    click = db.Column(db.Integer, server_default=db.FetchedValue())


class TpGoodsSearch(db.Model):
    __tablename__ = 'tp_goods_search'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    type = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    key_word = db.Column(db.String(255), index=True)


class TpGzhUser(db.Model):
    __tablename__ = 'tp_gzh_user'

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, server_default=db.FetchedValue())
    avatar = db.Column(db.String(255))
    province = db.Column(db.String(100))
    city = db.Column(db.String(100))
    nick_name = db.Column(db.String(100))
    gender = db.Column(db.String(10))
    openid = db.Column(db.String(255))
    unionid = db.Column(db.String(255))
    subscribe = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    subscribe_scene = db.Column(db.String(255),
                                info='返回用户关注的渠道来源，ADD_SCENE_SEARCH 公众号搜索，ADD_SCENE_ACCOUNT_MIGRATION 公众号迁移，ADD_SCENE_PROFILE_CARD 名片分享，ADD_SCENE_QR_CODE 扫描二维码，ADD_SCENE_PROFILE_LINK 图文页内名称点击，ADD_SCENE_PROFILE_ITEM 图文页右上角菜单，ADD_SCENE_PAID 支付后关注，ADD_SCENE_WECHAT_ADVERTISEMENT 微信广告，ADD_SCENE_REPRINT 他人转载 ,ADD_SCENE_LIVESTREAM 视频号直播，ADD_SCENE_CHANNELS 视频号 , ADD_SCENE_OTHERS 其他')
    subscribe_time = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    remark = db.Column(db.String(255))
    add_time = db.Column(db.Integer, nullable=False)
    update_time = db.Column(db.Integer)


class TpInvoice(db.Model):
    __tablename__ = 'tp_invoice'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255, 'utf8mb4_bin'))
    number = db.Column(db.String(255, 'utf8mb4_bin'))
    address = db.Column(db.String(255, 'utf8mb4_bin'))
    user_id = db.Column(db.Integer)
    pay_id = db.Column(db.String(255, 'utf8mb4_bin'))
    add_time = db.Column(db.Integer)
    update_time = db.Column(db.Integer)
    status = db.Column(db.Integer, server_default=db.FetchedValue())
    phone = db.Column(db.String(255, 'utf8mb4_bin'))
    email = db.Column(db.String(255, 'utf8mb4_bin'))
    price = db.Column(db.Numeric(10, 2))
    reason = db.Column(db.String(255, 'utf8mb4_bin'))
    kp_status = db.Column(db.Integer, server_default=db.FetchedValue())
    contract_id = db.Column(db.Integer, server_default=db.FetchedValue())
    numberprice = db.Column(db.Numeric(10, 2), server_default=db.FetchedValue())


class TpItem(db.Model):
    __tablename__ = 'tp_items'

    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.Integer, server_default=db.FetchedValue())
    type = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    title = db.Column(db.String(255))
    birthday = db.Column(db.String(255))
    property = db.Column(db.Text)
    citys = db.Column(db.Text)
    salary = db.Column(db.String(255))
    sex = db.Column(db.Integer, server_default=db.FetchedValue())
    salary_unit = db.Column(db.String(100))
    tags = db.Column(db.Text)
    post = db.Column(db.Text)
    talents = db.Column(db.Text)
    hz_start_time = db.Column(db.String(255))
    hz_end_time = db.Column(db.String(255))
    strength = db.Column(db.Text)
    experience = db.Column(db.Text)
    remark = db.Column(db.Text)
    status = db.Column(db.Integer, server_default=db.FetchedValue())
    refresh_time = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    reason = db.Column(db.String(255))
    check_time = db.Column(db.Integer, server_default=db.FetchedValue())
    refuse_time = db.Column(db.Integer, server_default=db.FetchedValue())
    add_time = db.Column(db.Integer, nullable=False)
    update_time = db.Column(db.Integer)


class TpItemsChat(db.Model):
    __tablename__ = 'tp_items_chat'

    id = db.Column(db.BigInteger, primary_key=True)
    item_id = db.Column(db.BigInteger, nullable=False, server_default=db.FetchedValue())
    type = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    user_id = db.Column(db.Integer, server_default=db.FetchedValue())
    to_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    add_time = db.Column(db.Integer, nullable=False)
    update_time = db.Column(db.Integer)


class TpItemsCollect(db.Model):
    __tablename__ = 'tp_items_collect'

    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.Integer, server_default=db.FetchedValue())
    item_id = db.Column(db.BigInteger, nullable=False, server_default=db.FetchedValue())
    type = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    add_time = db.Column(db.Integer, nullable=False)
    update_time = db.Column(db.Integer)


class TpItemsRefresh(db.Model):
    __tablename__ = 'tp_items_refresh'

    id = db.Column(db.BigInteger, primary_key=True)
    item_id = db.Column(db.BigInteger, nullable=False, server_default=db.FetchedValue())
    user_id = db.Column(db.Integer, server_default=db.FetchedValue())
    add_time = db.Column(db.Integer, nullable=False)
    update_time = db.Column(db.Integer)


class TpPay(db.Model):
    __tablename__ = 'tp_pay'

    id = db.Column(db.Integer, primary_key=True)
    contract_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    touser_id = db.Column(db.Integer)
    money = db.Column(db.Numeric(10, 2))
    img = db.Column(db.String(255, 'utf8mb4_bin'))
    add_time = db.Column(db.Integer)
    kp_status = db.Column(db.Integer, server_default=db.FetchedValue())
    status = db.Column(db.Integer, server_default=db.FetchedValue())


class TpPlugin(db.Model):
    __tablename__ = 'tp_plugin'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(13))
    name = db.Column(db.String(55))
    version = db.Column(db.String(255))
    author = db.Column(db.String(30))
    config = db.Column(db.Text)
    config_value = db.Column(db.Text)
    desc = db.Column(db.String(255))
    status = db.Column(db.Integer, server_default=db.FetchedValue())
    type = db.Column(db.String(50), info='插件类型 payment支付 login 登陆 shipping物流')
    icon = db.Column(db.String(255))
    bank_code = db.Column(db.Text)
    scene = db.Column(db.Integer, server_default=db.FetchedValue(), info='使用场景 0PC+手机 1手机 2PC 3APP 4小程序')


class TpProtocol(db.Model):
    __tablename__ = 'tp_protocol'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False, server_default=db.FetchedValue())
    type = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    content = db.Column(db.Text, nullable=False)
    image = db.Column(db.Text, nullable=False)
    gs_name = db.Column(db.Text, nullable=False)
    cl_time = db.Column(db.Text, nullable=False)
    gs_gm = db.Column(db.Text, nullable=False)
    zy_yw = db.Column(db.Text, nullable=False)
    address = db.Column(db.Text)
    latitude = db.Column(db.String(100))
    longitude = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    add_time = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    update_time = db.Column(db.Integer)


class TpRegion(db.Model):
    __tablename__ = 'tp_region'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    level = db.Column(db.Integer, server_default=db.FetchedValue(), info='地区等级 分省市县区')
    parent_id = db.Column(db.Integer)


class TpSmsLog(db.Model):
    __tablename__ = 'tp_sms_log'

    id = db.Column(db.Integer, primary_key=True)
    mobile = db.Column(db.String(11), server_default=db.FetchedValue())
    code = db.Column(db.String(10), server_default=db.FetchedValue())
    scene = db.Column(db.Integer, server_default=db.FetchedValue(), info='发送场景1:修改银行卡信息 2:注册 3:找回密码 4:修改密码 5提现 6转赠 7修改交易密码')
    is_use = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    add_time = db.Column(db.Integer, server_default=db.FetchedValue())


class TpSystemMenu(db.Model):
    __tablename__ = 'tp_system_menu'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    group = db.Column(db.String(20))
    right = db.Column(db.Text)
    open = db.Column(db.Integer, server_default=db.FetchedValue())


class TpTag(db.Model):
    __tablename__ = 'tp_tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    type = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    pid = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    level = db.Column(db.Integer, server_default=db.FetchedValue())
    sort = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    is_show = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    is_hot = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    add_time = db.Column(db.Integer, nullable=False)
    update_time = db.Column(db.Integer)


class TpThirdUser(db.Model):
    __tablename__ = 'tp_third_user'

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, server_default=db.FetchedValue())
    type = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    avatar = db.Column(db.String(255))
    province = db.Column(db.String(100))
    city = db.Column(db.String(100))
    nick_name = db.Column(db.String(100))
    gender = db.Column(db.String(10))
    user_id = db.Column(db.String(100))
    openid = db.Column(db.String(255))
    xcx_openid = db.Column(db.String(255))
    unionid = db.Column(db.String(255))
    add_time = db.Column(db.Integer, nullable=False)
    update_time = db.Column(db.Integer)
    sessionKey = db.Column(db.String(255))


class TpUserAddress(db.Model):
    __tablename__ = 'tp_user_address'

    address_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    consignee = db.Column(db.String(60), nullable=False, server_default=db.FetchedValue())
    province = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    city = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    district = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    address = db.Column(db.String(120), nullable=False, server_default=db.FetchedValue())
    mobile = db.Column(db.String(60), nullable=False, server_default=db.FetchedValue())
    is_default = db.Column(db.Integer, server_default=db.FetchedValue())


class TpUserSign(db.Model):
    __tablename__ = 'tp_user_sign'

    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.Integer)
    day = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    money = db.Column(db.Numeric(10, 2), nullable=False, server_default=db.FetchedValue())
    extra_money = db.Column(db.Numeric(10, 2), nullable=False, server_default=db.FetchedValue())
    add_time = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())


class TpUser(db.Model):
    __tablename__ = 'tp_users'
    user_id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(32), nullable=False, server_default=db.FetchedValue())
    paypwd = db.Column(db.String(32))
    head_pic = db.Column(db.String(255))
    nickname = db.Column(db.String(50))
    mobile = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue())
    level = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    realname = db.Column(db.String(100))
    firm_name = db.Column(db.String(255))
    kf_name = db.Column(db.String(255))
    idcard = db.Column(db.String(100))
    person_cert = db.Column(db.String(255))
    person_cert1 = db.Column(db.String(255))
    zhifubao = db.Column(db.String(255))
    bank_name = db.Column(db.String(255))
    bank_card = db.Column(db.String(255))
    bank_zh = db.Column(db.String(255))
    weixin = db.Column(db.String(255))
    balance = db.Column(db.Numeric(15, 4), nullable=False, server_default=db.FetchedValue())
    reg_time = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    reid = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    jt_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    rekey = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    zt_num = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    td_num = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    lj_sign = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    sign_money = db.Column(db.Numeric(15, 2), nullable=False, server_default=db.FetchedValue())
    is_sign = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    last_login = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    last_ip = db.Column(db.String(15), nullable=False, server_default=db.FetchedValue())
    is_lock = db.Column(db.Integer, server_default=db.FetchedValue())
    is_kf = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    is_online = db.Column(db.Integer, server_default=db.FetchedValue())
    openid = db.Column(db.String(255))
    user_token = db.Column(db.String(50), nullable=False)
    kf_img = db.Column(db.String(255), nullable=False)
    kf_show = db.Column(db.Integer, nullable=False)


class TpVoucher(db.Model):
    __tablename__ = 'tp_voucher'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    img = db.Column(db.String(255, 'utf8mb4_bin'))
    status = db.Column(db.String(255, 'utf8mb4_bin'), server_default=db.FetchedValue())
    order_sn = db.Column(db.String(255, 'utf8mb4_bin'))
    mobile = db.Column(db.String(255, 'utf8mb4_bin'))
    add_time = db.Column(db.Integer)
    update_time = db.Column(db.Integer)
    contract_id = db.Column(db.Integer, server_default=db.FetchedValue())
    kf_wx = db.Column(db.String(255, 'utf8mb4_bin'))


class TpWxMenu(db.Model):
    __tablename__ = 'tp_wx_menu'

    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.Integer, server_default=db.FetchedValue())
    name = db.Column(db.String(50), nullable=False, server_default=db.FetchedValue())
    sort = db.Column(db.Integer, server_default=db.FetchedValue())
    type = db.Column(db.String(20), server_default=db.FetchedValue(), info='0 view 1 click')
    value = db.Column(db.String(255))
    token = db.Column(db.String(50), nullable=False, server_default=db.FetchedValue())
    pid = db.Column(db.Integer, server_default=db.FetchedValue())


class TpWxUser(db.Model):
    __tablename__ = 'tp_wx_user'
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, nullable=False, index=True)
    wxname = db.Column(db.String(60), nullable=False, server_default=db.FetchedValue())
    aeskey = db.Column(db.String(256), nullable=False, server_default=db.FetchedValue())
    encode = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    appid = db.Column(db.String(50), nullable=False, server_default=db.FetchedValue())
    appsecret = db.Column(db.String(50), nullable=False, server_default=db.FetchedValue())
    wxid = db.Column(db.String(64), nullable=False, server_default=db.FetchedValue())
    weixin = db.Column(db.String(64), nullable=False)
    headerpic = db.Column(db.String(255), nullable=False)
    token = db.Column(db.String(255), nullable=False)
    w_token = db.Column(db.String(150), nullable=False, server_default=db.FetchedValue())
    add_time = db.Column(db.Integer, nullable=False)
    update_time = db.Column(db.Integer, nullable=False)
    tplcontentid = db.Column(db.String(2), nullable=False, server_default=db.FetchedValue())
    share_ticket = db.Column(db.String(150), nullable=False, server_default=db.FetchedValue())
    share_dated = db.Column(db.String(15), nullable=False)
    authorizer_access_token = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    authorizer_refresh_token = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    authorizer_expires = db.Column(db.String(10), nullable=False)
    type = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    web_access_token = db.Column(db.String(200), server_default=db.FetchedValue(), info=' 网页授权token')
    web_refresh_token = db.Column(db.String(200), server_default=db.FetchedValue())
    web_expires = db.Column(db.Integer, nullable=False)
    qr = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    menu_config = db.Column(db.Text)
    wait_access = db.Column(db.Integer, server_default=db.FetchedValue())


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    poster_id = db.Column(db.Integer, db.ForeignKey('tp_users.user_id'))
    poster = db.relationship('TpUser', backref="posts")
    likes = db.Column(db.Integer, nullable=True)
    stars = db.Column(db.Integer, nullable=True)
    time = db.Column(db.DateTime, default=datetime.now)
    def to_json(self):
        data = {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "poster_id": self.poster_id,
            "poster_realname": self.poster.realname if self.poster else None,
            "poster_nickname": self.poster.nickname if self.poster else None,
            "poster_pic": self.poster.head_pic if self.poster else None,
            "likes": self.likes,
            "stars": self.stars,
            "time": self.time,
            "comment_length": len(self.comments) if self.comments else 0,
        }
        if self.images:
            image_data = self.images[0]
            if image_data:
                post_image = {
                    "length": image_data.length,
                    "image1": image_data.image1,
                    "image2": image_data.image2,
                    "image3": image_data.image3,
                    "image4": image_data.image4,
                    "image5": image_data.image5,
                    "image6": image_data.image6,
                    "image7": image_data.image7,
                    "image8": image_data.image8,
                    "image9": image_data.image9,
                }
                data["post_image"] = post_image
        return data


class Post_image(db.Model):
    __tablename__ = 'post_image'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    post = db.relationship('Post', backref="images")
    image1 = db.Column(db.Text, nullable=True)
    image2 = db.Column(db.Text, nullable=True)
    image3 = db.Column(db.Text, nullable=True)
    image4 = db.Column(db.Text, nullable=True)
    image5 = db.Column(db.Text, nullable=True)
    image6 = db.Column(db.Text, nullable=True)
    image7 = db.Column(db.Text, nullable=True)
    image8 = db.Column(db.Text, nullable=True)
    image9 = db.Column(db.Text, nullable=True)
    length = db.Column(db.Integer, nullable=True)


class Post_comment(db.Model):
    __tablename__ = 'post_comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    time = db.Column(db.DateTime, default=datetime.now)
    likes = db.Column(db.Integer, nullable=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('tp_users.user_id'))
    sender = db.relationship('TpUser', backref="comments")
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    post = db.relationship('Post', backref="comments")

    def to_json(self):
        return {
            "id": self.id,
            "content": self.content,
            "time": self.time,
            "sender_id": self.sender_id,
            "sender_realname": self.sender.realname if self.sender else None,
            "sender_nickname": self.sender.nickname if self.sender else None,
            "sender_pic": self.sender.head_pic if self.sender else None,
            "likes": self.likes,
            "post_id": self.post_id
        }


class Post_comment_reply(db.Model):
    __tablename__ = 'post_comment_reply'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    time = db.Column(db.DateTime, default=datetime.now)
    sender_id = db.Column(db.Integer, db.ForeignKey('tp_users.user_id'))
    sender = db.relationship('TpUser', backref="replies")
    comment_id = db.Column(db.Integer, db.ForeignKey('post_comment.id'))
    comment = db.relationship('Post_comment', backref="replies")

    def to_json(self):
        return {
            "id": self.id,
            "content": self.content,
            "time": self.time,
            "sender_id": self.sender_id,
            "sender_realname": self.sender.realname if self.sender else None,
            "comment_id": self.comment_id
        }


class AccessToken(db.Model):
    __tablename__ = 'access_token'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    access_token = db.Column(db.String(200), nullable=False)
    update_time = db.Column(db.DateTime, default=datetime.now)
    expires_in = db.Column(db.Integer, nullable=False)