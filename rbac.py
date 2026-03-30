permissions = {
    "admin": ["read", "write", "delete", "manage_users"],
    "user": ["read"]
}

def check_access(role, action):
    return action in permissions.get(role, [])