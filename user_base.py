def check_username(username):
    min_login_length = 4
    return (username.isalpha() and
            len(username) >= min_login_length)

users = dict()
users_by_service_login = dict()
