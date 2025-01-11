from models import TpUser


def update_login_state():
    # users = TpUser.query.all()
    user = TpUser.query.get(999)
    print(user)
