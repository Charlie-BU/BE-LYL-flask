# coding: utf-8
from exts import db



class TpAccountLog(db.Model):
    __tablename__ = 'tp_account_log'

    log_id = db.Column(db.Integer, primary_key=True, info='日志id')
    user_id = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue(), info='用户id')
    gid = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='触发奖励用户id')
    money = db.Column(db.Numeric(15, 4), server_default=db.FetchedValue(), info='变动金额')
    type = db.Column(db.Integer, server_default=db.FetchedValue(), info='变动类型1余额2积分3金豆4金种子')
    add_time = db.Column(db.Integer, nullable=False, info='变动时间')
    desc = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue(), info='描述')
    order_sn = db.Column(db.String(50), info='订单编号')
    order_id = db.Column(db.Integer, info='订单id')
    pick_order_id = db.Column(db.Integer, info='进货/提货订单id')
    wid = db.Column(db.Integer, server_default=db.FetchedValue(), info='提现表id')
    is_ywy = db.Column(db.Integer, server_default=db.FetchedValue(), info='是否业务员/经理收益1是')



class TpAd(db.Model):
    __tablename__ = 'tp_ad'

    ad_id = db.Column(db.Integer, primary_key=True, info='广告id')
    type = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='广告类型1图片2视频')
    ad_name = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue(), info='广告名称')
    ad_type = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='广告位置1首页轮播2首页菜单3广告位(单张)4广告位(每排3张)5广告位(每排2张)')
    ad_link = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue(), info='链接地址')
    image = db.Column(db.Text, nullable=False, info='图片地址')
    video = db.Column(db.Text, info='视频地址')
    click_count = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='点击量')
    open = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue(), info='是否显示1是')
    sort = db.Column(db.Integer, server_default=db.FetchedValue(), info='排序')
    target = db.Column(db.Integer, server_default=db.FetchedValue(), info='是否开启浏览器新窗口')
    add_time = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='添加时间')



class TpAdmin(db.Model):
    __tablename__ = 'tp_admin'

    admin_id = db.Column(db.SmallInteger, primary_key=True, info='用户id')
    user_name = db.Column(db.String(60), nullable=False, index=True, server_default=db.FetchedValue(), info='用户名')
    email = db.Column(db.String(60), server_default=db.FetchedValue(), info='email')
    password = db.Column(db.String(32), nullable=False, server_default=db.FetchedValue(), info='密码')
    ec_salt = db.Column(db.String(10), info='秘钥')
    add_time = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='添加时间')
    last_login = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='最后登录时间')
    last_ip = db.Column(db.String(15), nullable=False, server_default=db.FetchedValue(), info='最后登录ip')
    nav_list = db.Column(db.Text, info='权限')
    role_id = db.Column(db.SmallInteger, server_default=db.FetchedValue(), info='角色id')



class TpAdminLog(db.Model):
    __tablename__ = 'tp_admin_log'

    log_id = db.Column(db.BigInteger, primary_key=True, info='表id')
    admin_id = db.Column(db.Integer, info='管理员id')
    log_info = db.Column(db.String(255), info='日志描述')
    log_ip = db.Column(db.String(30), info='ip地址')
    log_url = db.Column(db.String(50), info='url')
    log_time = db.Column(db.Integer, info='日志时间')



class TpAdminRole(db.Model):
    __tablename__ = 'tp_admin_role'

    role_id = db.Column(db.SmallInteger, primary_key=True, info='角色ID')
    role_name = db.Column(db.String(30), info='角色名称')
    act_list = db.Column(db.Text, info='权限列表')
    role_desc = db.Column(db.String(255), info='角色描述')



class TpConfig(db.Model):
    __tablename__ = 'tp_config'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), info='配置的key键名')
    value = db.Column(db.String(512), info='配置的val值')
    inc_type = db.Column(db.String(64), info='配置分组')
    desc = db.Column(db.String(50), info='描述')



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
    title = db.Column(db.String(150), nullable=False, server_default=db.FetchedValue(), info='文章标题')
    cat_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='所属分类id')
    description = db.Column(db.String, info='文章摘要')
    image = db.Column(db.String(255), server_default=db.FetchedValue(), info='文章缩略图')
    video = db.Column(db.Text, info='视频地址')
    content = db.Column(db.String, nullable=False)
    sort = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='排序')
    open = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='是否显示1是')
    add_time = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='添加时间')
    update_time = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='更新时间')
    click = db.Column(db.Integer, server_default=db.FetchedValue(), info='浏览量')



class TpGoodsSearch(db.Model):
    __tablename__ = 'tp_goods_search'

    id = db.Column(db.Integer, primary_key=True, info='表id')
    user_id = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue(), info='用户id')
    type = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='类型1用户2企业')
    key_word = db.Column(db.String, index=True, info='搜索关键字')



class TpGzhUser(db.Model):
    __tablename__ = 'tp_gzh_user'

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, server_default=db.FetchedValue(), info='用户id')
    avatar = db.Column(db.String(255), info='第三方头像地址')
    province = db.Column(db.String(100), info='省份')
    city = db.Column(db.String(100), info='城市')
    nick_name = db.Column(db.String(100), info='昵称')
    gender = db.Column(db.String(10), info='性别')
    openid = db.Column(db.String(255), info='微信openid')
    unionid = db.Column(db.String(255), info='微信unionid')
    subscribe = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='是否关注了公众号1是')
    subscribe_scene = db.Column(db.String(255), info='返回用户关注的渠道来源，ADD_SCENE_SEARCH 公众号搜索，ADD_SCENE_ACCOUNT_MIGRATION 公众号迁移，ADD_SCENE_PROFILE_CARD 名片分享，ADD_SCENE_QR_CODE 扫描二维码，ADD_SCENE_PROFILE_LINK 图文页内名称点击，ADD_SCENE_PROFILE_ITEM 图文页右上角菜单，ADD_SCENE_PAID 支付后关注，ADD_SCENE_WECHAT_ADVERTISEMENT 微信广告，ADD_SCENE_REPRINT 他人转载 ,ADD_SCENE_LIVESTREAM 视频号直播，ADD_SCENE_CHANNELS 视频号 , ADD_SCENE_OTHERS 其他')
    subscribe_time = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='用户关注时间，为时间戳。如果用户曾多次关注，则取最后关注时间')
    remark = db.Column(db.String(255), info='公众号运营者对粉丝的备注，公众号运营者可在微信公众平台用户管理界面对粉丝添加备注')
    add_time = db.Column(db.Integer, nullable=False, info='创建时间')
    update_time = db.Column(db.Integer, info='更新时间')



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
    user_id = db.Column(db.Integer, server_default=db.FetchedValue(), info='用户id')
    type = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='类型1项目2简历')
    title = db.Column(db.String(255), info='项目标题')
    birthday = db.Column(db.String(255), info='出生年月')
    property = db.Column(db.Text, info='工作属性')
    citys = db.Column(db.Text, info='期望城市')
    salary = db.Column(db.String(255), info='薪资')
    sex = db.Column(db.Integer, server_default=db.FetchedValue(), info='性别1男2女')
    salary_unit = db.Column(db.String(100), info='薪资单位')
    tags = db.Column(db.Text, info='擅长项目/项目标签')
    post = db.Column(db.Text, info='招聘/应聘岗位')
    talents = db.Column(db.Text, info='擅长技能/需求技能')
    hz_start_time = db.Column(db.String(255), info='合作开始时间')
    hz_end_time = db.Column(db.String(255), info='合作结束时间')
    strength = db.Column(db.Text, info='个人优势/项目需求')
    experience = db.Column(db.Text, info='项目经历/岗位职责')
    remark = db.Column(db.Text, info='备注信息')
    status = db.Column(db.Integer, server_default=db.FetchedValue(), info='状态：-1待审核1成功2失败3启用中4已停用')
    refresh_time = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='刷新时间')
    reason = db.Column(db.String(255), info='拒绝原因')
    check_time = db.Column(db.Integer, server_default=db.FetchedValue(), info='审核时间')
    refuse_time = db.Column(db.Integer, server_default=db.FetchedValue(), info='拒绝时间')
    add_time = db.Column(db.Integer, nullable=False, info='创建时间')
    update_time = db.Column(db.Integer, info='更新时间')



class TpItemsChat(db.Model):
    __tablename__ = 'tp_items_chat'

    id = db.Column(db.BigInteger, primary_key=True)
    item_id = db.Column(db.BigInteger, nullable=False, server_default=db.FetchedValue(), info='项目/简历表id')
    type = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='类型1项目2简历3客服')
    user_id = db.Column(db.Integer, server_default=db.FetchedValue(), info='用户id')
    to_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='接收消息用户id')
    add_time = db.Column(db.Integer, nullable=False, info='创建时间')
    update_time = db.Column(db.Integer, info='更新时间')



class TpItemsCollect(db.Model):
    __tablename__ = 'tp_items_collect'

    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.Integer, server_default=db.FetchedValue(), info='用户id')
    item_id = db.Column(db.BigInteger, nullable=False, server_default=db.FetchedValue(), info='项目/简历表id')
    type = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='类型1项目2简历')
    add_time = db.Column(db.Integer, nullable=False, info='创建时间')
    update_time = db.Column(db.Integer, info='更新时间')



class TpItemsRefresh(db.Model):
    __tablename__ = 'tp_items_refresh'

    id = db.Column(db.BigInteger, primary_key=True)
    item_id = db.Column(db.BigInteger, nullable=False, server_default=db.FetchedValue(), info='项目/简历表id')
    user_id = db.Column(db.Integer, server_default=db.FetchedValue(), info='用户id')
    add_time = db.Column(db.Integer, nullable=False, info='创建时间')
    update_time = db.Column(db.Integer, info='更新时间')



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
    code = db.Column(db.String(13), info='插件编码')
    name = db.Column(db.String(55), info='中文名字')
    version = db.Column(db.String(255), info='插件的版本')
    author = db.Column(db.String(30), info='插件作者')
    config = db.Column(db.Text, info='配置信息')
    config_value = db.Column(db.Text, info='配置值信息')
    desc = db.Column(db.String(255), info='插件描述')
    status = db.Column(db.Integer, server_default=db.FetchedValue(), info='是否启用')
    type = db.Column(db.String(50), info='插件类型 payment支付 login 登陆 shipping物流')
    icon = db.Column(db.String(255), info='图标')
    bank_code = db.Column(db.Text, info='网银配置信息')
    scene = db.Column(db.Integer, server_default=db.FetchedValue(), info='使用场景 0PC+手机 1手机 2PC 3APP 4小程序')



class TpProtocol(db.Model):
    __tablename__ = 'tp_protocol'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False, server_default=db.FetchedValue(), info='文章标题')
    type = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='类型1身份证2手机号')
    content = db.Column(db.String, nullable=False)
    image = db.Column(db.Text, nullable=False, info='图片')
    gs_name = db.Column(db.Text, nullable=False, info='公司名称')
    cl_time = db.Column(db.Text, nullable=False, info='成立时间')
    gs_gm = db.Column(db.Text, nullable=False, info='公司规模')
    zy_yw = db.Column(db.Text, nullable=False, info='主营业务')
    address = db.Column(db.Text, info='具体位置')
    latitude = db.Column(db.String(100), info='纬度')
    longitude = db.Column(db.String(100), info='经度')
    phone = db.Column(db.String(100), info='联系电话')
    add_time = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='添加时间')
    update_time = db.Column(db.Integer, info='更新时间')



class TpRegion(db.Model):
    __tablename__ = 'tp_region'

    id = db.Column(db.Integer, primary_key=True, info='表id')
    name = db.Column(db.String(32), info='地区名称')
    level = db.Column(db.Integer, server_default=db.FetchedValue(), info='地区等级 分省市县区')
    parent_id = db.Column(db.Integer, info='父id')



class TpSmsLog(db.Model):
    __tablename__ = 'tp_sms_log'

    id = db.Column(db.Integer, primary_key=True, info='表id')
    mobile = db.Column(db.String(11), server_default=db.FetchedValue(), info='手机号')
    code = db.Column(db.String(10), server_default=db.FetchedValue(), info='验证码')
    scene = db.Column(db.Integer, server_default=db.FetchedValue(), info='发送场景1:修改银行卡信息 2:注册 3:找回密码 4:修改密码 5提现 6转赠 7修改交易密码')
    is_use = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='是否已使用1是')
    add_time = db.Column(db.Integer, server_default=db.FetchedValue(), info='发送时间')



class TpSystemMenu(db.Model):
    __tablename__ = 'tp_system_menu'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), info='权限名字')
    group = db.Column(db.String(20), info='所属分组')
    right = db.Column(db.Text, info='权限码(控制器+动作)')
    open = db.Column(db.Integer, server_default=db.FetchedValue(), info='状态1显示0隐藏')



class TpTag(db.Model):
    __tablename__ = 'tp_tags'

    id = db.Column(db.Integer, primary_key=True, info='id')
    name = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue(), info='名称')
    type = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue(), info='标签类型1项目类型2职能标签3擅长技能4所在城市5工作属性')
    pid = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='父id')
    level = db.Column(db.Integer, server_default=db.FetchedValue(), info='等级')
    sort = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='顺序排序')
    is_show = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='是否显示')
    is_hot = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='是否推荐1是')
    add_time = db.Column(db.Integer, nullable=False, info='创建时间')
    update_time = db.Column(db.Integer, info='更新时间')



class TpThirdUser(db.Model):
    __tablename__ = 'tp_third_user'

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, server_default=db.FetchedValue(), info='用户id')
    type = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='类型1支付宝用户2微信用户')
    avatar = db.Column(db.String(255), info='第三方头像地址')
    province = db.Column(db.String(100), info='省份')
    city = db.Column(db.String(100), info='城市')
    nick_name = db.Column(db.String(100), info='昵称')
    gender = db.Column(db.String(10), info='性别')
    user_id = db.Column(db.String(100), info='第三方用户id')
    openid = db.Column(db.String(255), info='app微信openid')
    xcx_openid = db.Column(db.String(255), info='小程序微信openid')
    unionid = db.Column(db.String(255), info='微信unionid')
    add_time = db.Column(db.Integer, nullable=False, info='创建时间')
    update_time = db.Column(db.Integer, info='更新时间')
    sessionKey = db.Column(db.String(255), info='微信sessionKey')



class TpUserAddres(db.Model):
    __tablename__ = 'tp_user_address'

    address_id = db.Column(db.Integer, primary_key=True, info='表id')
    user_id = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue(), info='用户id')
    consignee = db.Column(db.String(60), nullable=False, server_default=db.FetchedValue(), info='收货人')
    province = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue(), info='省份')
    city = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue(), info='城市')
    district = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue(), info='地区')
    address = db.Column(db.String(120), nullable=False, server_default=db.FetchedValue(), info='地址')
    mobile = db.Column(db.String(60), nullable=False, server_default=db.FetchedValue(), info='手机')
    is_default = db.Column(db.Integer, server_default=db.FetchedValue(), info='默认收货地址')



class TpUserSign(db.Model):
    __tablename__ = 'tp_user_sign'

    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.Integer, info='用户id')
    day = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='签到天数')
    money = db.Column(db.Numeric(10, 2), nullable=False, server_default=db.FetchedValue(), info='奖励金额')
    extra_money = db.Column(db.Numeric(10, 2), nullable=False, server_default=db.FetchedValue(), info='额外奖励金额')
    add_time = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='签到时间')



class TpUser(db.Model):
    __tablename__ = 'tp_users'

    user_id = db.Column(db.Integer, primary_key=True, info='表id')
    password = db.Column(db.String(32), nullable=False, server_default=db.FetchedValue(), info='密码')
    paypwd = db.Column(db.String(32), info='支付密码')
    head_pic = db.Column(db.String(255), info='头像')
    nickname = db.Column(db.String(50), info='第三方返回昵称')
    mobile = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue(), info='手机号码')
    level = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='会员级别对应user_level表id')
    realname = db.Column(db.String(100), info='真实姓名')
    firm_name = db.Column(db.String(255), info='公司名称')
    kf_name = db.Column(db.String(255), info='客服名称')
    idcard = db.Column(db.String(100), info='身份证号')
    person_cert = db.Column(db.String(255), info='身份证正面')
    person_cert1 = db.Column(db.String(255), info='身份证反面')
    zhifubao = db.Column(db.String(255), info='支付宝')
    bank_name = db.Column(db.String(255), info='银行名称')
    bank_card = db.Column(db.String(255), info='银行卡号')
    bank_zh = db.Column(db.String(255), info='开户支行')
    weixin = db.Column(db.String(255), info='微信号')
    balance = db.Column(db.Numeric(15, 4), nullable=False, server_default=db.FetchedValue(), info='余额')
    reg_time = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='注册时间')
    reid = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='推荐人id')
    jt_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='间推用户id')
    rekey = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue(), info='推荐码')
    zt_num = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='直推有效人数')
    td_num = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='团队人数')
    lj_sign = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='连续签到天数')
    sign_money = db.Column(db.Numeric(15, 2), nullable=False, server_default=db.FetchedValue(), info='已签到获得的总积分')
    is_sign = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='今日是否已签到1是')
    last_login = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='最后登录时间')
    last_ip = db.Column(db.String(15), nullable=False, server_default=db.FetchedValue(), info='最后登录ip')
    is_lock = db.Column(db.Integer, server_default=db.FetchedValue(), info='是否被锁定冻结')
    is_kf = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='是否客服1是')
    is_online = db.Column(db.Integer, server_default=db.FetchedValue(), info='是否在线1是')
    openid = db.Column(db.String(255), info='微信openid')
    user_token = db.Column(db.String(50), nullable=False, info='用户token')
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
    add_time = db.Column(db.Integer, info='创建时间')
    update_time = db.Column(db.Integer, info='更新时间')
    contract_id = db.Column(db.Integer, server_default=db.FetchedValue())
    kf_wx = db.Column(db.String(255, 'utf8mb4_bin'))



class TpWxMenu(db.Model):
    __tablename__ = 'tp_wx_menu'

    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.Integer, server_default=db.FetchedValue(), info='菜单级别')
    name = db.Column(db.String(50), nullable=False, server_default=db.FetchedValue())
    sort = db.Column(db.Integer, server_default=db.FetchedValue(), info='排序')
    type = db.Column(db.String(20), server_default=db.FetchedValue(), info='0 view 1 click')
    value = db.Column(db.String(255))
    token = db.Column(db.String(50), nullable=False, server_default=db.FetchedValue())
    pid = db.Column(db.Integer, server_default=db.FetchedValue(), info='上级菜单')



class TpWxUser(db.Model):
    __tablename__ = 'tp_wx_user'

    id = db.Column(db.Integer, primary_key=True, info='表id')
    uid = db.Column(db.Integer, nullable=False, index=True, info='uid')
    wxname = db.Column(db.String(60), nullable=False, server_default=db.FetchedValue(), info='公众号名称')
    aeskey = db.Column(db.String(256), nullable=False, server_default=db.FetchedValue(), info='aeskey')
    encode = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='encode')
    appid = db.Column(db.String(50), nullable=False, server_default=db.FetchedValue(), info='appid')
    appsecret = db.Column(db.String(50), nullable=False, server_default=db.FetchedValue(), info='appsecret')
    wxid = db.Column(db.String(64), nullable=False, server_default=db.FetchedValue(), info='公众号原始ID')
    weixin = db.Column(db.String(64), nullable=False, info='微信号')
    headerpic = db.Column(db.String(255), nullable=False, info='头像地址')
    token = db.Column(db.String(255), nullable=False, info='token')
    w_token = db.Column(db.String(150), nullable=False, server_default=db.FetchedValue(), info='微信对接token')
    add_time = db.Column(db.Integer, nullable=False, info='添加时间')
    update_time = db.Column(db.Integer, nullable=False, info='更新时间')
    tplcontentid = db.Column(db.String(2), nullable=False, server_default=db.FetchedValue(), info='内容模版ID')
    share_ticket = db.Column(db.String(150), nullable=False, server_default=db.FetchedValue(), info='分享ticket')
    share_dated = db.Column(db.String(15), nullable=False, info='share_dated')
    authorizer_access_token = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue(), info='authorizer_access_token')
    authorizer_refresh_token = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue(), info='authorizer_refresh_token')
    authorizer_expires = db.Column(db.String(10), nullable=False, info='authorizer_expires')
    type = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='类型')
    web_access_token = db.Column(db.String(200), server_default=db.FetchedValue(), info=' 网页授权token')
    web_refresh_token = db.Column(db.String(200), server_default=db.FetchedValue(), info='web_refresh_token')
    web_expires = db.Column(db.Integer, nullable=False, info='过期时间')
    qr = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue(), info='qr')
    menu_config = db.Column(db.Text, info='菜单')
    wait_access = db.Column(db.Integer, server_default=db.FetchedValue(), info='微信接入状态,0待接入1已接入')
