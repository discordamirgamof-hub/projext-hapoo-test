import time

def check_level_access(user, required_level):
    return user["level"] >= required_level

def is_in_prison(user):
    return time.time() < user["prison_until"]