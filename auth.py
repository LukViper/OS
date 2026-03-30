import bcrypt, json, time

LOCK_TIME = 60
MAX_ATTEMPTS = 5
attempts = {}

def load_users():
    try:
        with open("users.json") as f:
            return json.load(f)
    except:
        return {}

def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f, indent=4)

def register(username, password, role="user", dept="CS"):
    users = load_users()

    if username in users:
        return False, "User exists"

    if len(password) < 6:
        return False, "Weak password"

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    users[username] = {
        "password": hashed,
        "role": role,
        "department": dept
    }

    save_users(users)
    return True, "Registered"

def login(username, password):
    users = load_users()

    # brute force protection
    if username in attempts:
        if attempts[username]["count"] >= MAX_ATTEMPTS:
            if time.time() - attempts[username]["time"] < LOCK_TIME:
                return False, "Account locked"
            else:
                attempts[username] = {"count": 0}

    if username not in users:
        return False, "User not found"

    if bcrypt.checkpw(password.encode(), users[username]["password"].encode()):
        attempts.pop(username, None)
        return True, users[username]

    attempts[username] = {
        "count": attempts.get(username, {}).get("count", 0) + 1,
        "time": time.time()
    }

    return False, "Wrong password"