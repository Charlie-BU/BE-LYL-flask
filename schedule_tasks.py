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
    # 获取所有用户及其简历信息，避免逐条查询
    users = TpUser.query.all()
    user_ids = [user.user_id for user in users]
    # 批量查询用户的简历
    resumes = TpItem.query.filter(
        and_(TpItem.user_id.in_(user_ids), TpItem.type == 2)
    ).all()
    resumes_map = {resume.user_id: resume for resume in resumes}
    # 批量查询简历作品信息
    resume_ids = [resume.id for resume in resumes]
    works = ItemFiles.query.filter(ItemFiles.id.in_(resume_ids)).all()
    works_map = {work.id: work for work in works}

    count = 0
    updates = []
    for user in users:
        resume = resumes_map.get(user.user_id)
        resume_score = 0
        # 计算简历评分
        if resume and (resume.status in [1, 3]):
            resume_score = 40
            index = ['strength', 'experience']
            for key in index:
                if getattr(resume, key, None):
                    resume_score += 20
            # 检查是否有作品
            work = works_map.get(resume.id)
            if work and work.length > 0:
                resume_score += 20
        # 计算总评分
        active_score = user.active_score
        overall_score = resume_score / 100 * 50 + active_score / 100 * 20
        user.star_as_elite = overall_score
        updates.append(user)
        count += 1
        # 打印进度
        if count % 100 == 0:  # 每100条打印一次
            print(f"已完成：{count}人")
    # 批量提交更新
    db.session.bulk_save_objects(updates)
    db.session.commit()
    print(f"更新完成，总计处理用户数：{count}")
