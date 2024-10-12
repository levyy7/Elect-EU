# Dummy database (use MongoDB or SQL in production)
users_db = {}

def get_user_by_email(email):
    return users_db.get(email)

def save_secret_for_user(email, secret):
    if email in users_db:
        users_db[email]['2fa_secret'] = secret
    else:
        users_db[email] = {'email': email, '2fa_secret': secret}
