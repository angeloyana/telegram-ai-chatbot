def get_full_name(user) -> str:
    if user.last_name:
        return f'{user.first_name} {user.last_name}'
    return user.first_name
