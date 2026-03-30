import time

def check_abac(session, action, resource=None):
    hour = time.localtime().tm_hour

    # time restriction
    if action in ["write", "delete"] and hour >= 18:
        return False

    # department restriction
    if action in ["write", "delete"]:
        if session["department"] != "CS":
            return False

    # ownership check
    if resource:
        if resource.get("owner") != session["user"]:
            return False

    return True