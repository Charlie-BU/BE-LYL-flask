from datetime import datetime, timedelta
from sqlalchemy import func, and_

from decorator import with_app_context
from models import *


def calc_active_score(user, rule):
    if rule == "logged_yesterday":
        user.active_score += 10 if user.active_score <= 90 else (
                100 - user.active_score) if (90 < user.active_score <= 100) else 0
        print(user)
    elif rule == "unlogged":
        user.active_score -= 5 if user.active_score >= 5 else user.active_score if (
                0 <= user.active_score < 5) else 0


@with_app_context
def update_active_score():
    print("更新开始")
    # 获取昨天和今天的时间戳
    yesterday = datetime.today() - timedelta(days=1)
    yesterday = datetime(yesterday.year, yesterday.month, yesterday.day)
    yesterday_timestamp = int(yesterday.timestamp())
    today = datetime.today()
    today = datetime(today.year, today.month, today.day)
    today_timestamp = int(today.timestamp())
    # 昨天登录的用户
    users_logged_yesterday = TpUser.query.filter(and_(
        TpUser.last_login >= yesterday_timestamp,
        TpUser.last_login < today_timestamp
    )).all()
    # 今天登录的用户（在0:00开始的极短间隔内登录，无需处理）
    # users_logged_today = TpUser.query.filter(
    #     TpUser.last_login >= today_timestamp
    # ).all()
    # 两天都没登录的用户
    users_unlogged = TpUser.query.filter(
        TpUser.last_login < yesterday_timestamp
    ).all()
    # 批量更新分数
    for user in users_logged_yesterday:
        calc_active_score(user, "logged_yesterday")
    for user in users_unlogged:
        calc_active_score(user, "unlogged")
    db.session.commit()
    print('更新结束')


@with_app_context
def update_all_users_star():
    users = TpUser.query.all()
    count = 0
    for user in users:
        # INDEX1-简历评分
        resume = TpItem.query.filter(and_(TpItem.user_id == user.id, TpItem.type == 2)).first()
        resume_score = 0
        # 有简历（发布成功）：40分；三个指标：每个20分
        if resume and (resume.status in [1, 3]):
            resume_score = 40
            index = ['strength', 'experience']
            for key in index:
                if getattr(resume, key, None):  # 如果resume中的字段有key不为None；若无key，则返回None
                    resume_score += 20
            # 拿到简历作品，有则加20
            works = ItemFiles.query.get(resume.id)
            if works and works.length > 0:
                resume_score += 20
        # INDEX2-用户活跃度
        active_score = user.active_score
        overall_score = resume_score / 100 * 50 + active_score / 100 * 20
        user.star_as_elite = overall_score
        db.session.commit()
        count += 1
        print(f"已完成：{count}人")