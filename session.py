import secrets, time

sessions = {}
TIMEOUT = 60

def create_session(username, role, dept):
    sid = secrets.token_hex(16)
    sessions[sid] = {
        "user": username,
        "role": role,
        "department": dept,
        "created": time.time()
    }
    return sid

def validate_session(sid):
    if sid not in sessions:
        return False

    if time.time() - sessions[sid]["created"] > TIMEOUT:
        del sessions[sid]
        return False

    return True

def get_session(sid):
    return sessions.get(sid)

def destroy_session(sid):
    sessions.pop(sid, None)

def list_sessions():
    return sessions
