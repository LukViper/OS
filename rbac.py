permissions = {
    
   
    "admin": ["read", "write", "delete", "execute", "list", "profile"],
    "user": ["read", "write", "execute", "list", "profile"]

}


def check_access(role, action):
    return action in permissions.get(role, [])