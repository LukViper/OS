from auth import register, login, load_users
from session import create_session, validate_session, get_session, destroy_session
from rbac import check_access
from abac import check_abac
import time

current_session = None

# ---------- Helpers ----------

def is_admin(session):
    return session and session.get("role") == "admin"

def require_auth():
    global current_session
    if not current_session or not validate_session(current_session):
        print("Session expired or invalid. Please login again.")
        current_session = None
        return False
    return True

def get_prompt(session):
    remaining = int(300 - (time.time() - session["created"]))
    if remaining < 0:
        remaining = 0
    return f"[{session['user']}:{session['role']} | {remaining}s] >> "

# ---------- Core Loop ----------

def action_loop():
    global current_session

    while True:
        if not require_auth():
            break

        session = get_session(current_session)
        prompt = get_prompt(session)
        action = input(prompt).strip()

        if action == "logout":
            destroy_session(current_session)
            current_session = None
            print("Logged out")
            break

        if action == "exit":
            exit()

        # RBAC check
        if not check_access(session["role"], action):
            print("RBAC: Access denied")
            continue

        # ABAC check
        resource = {"owner": session["user"]}  # simple mock resource
        if not check_abac(session, action, resource):
            print("ABAC: Access denied")
            continue

        print(f"{action} executed successfully")

# ---------- Menu ----------

def menu():
    print("""
1. login
2. adduser
3. exit
""")

# ---------- Main ----------

while True:
    menu()
    choice = input(">> ").strip()

    # ---------- LOGIN ----------
    if choice == "1":
        u = input("Username: ")
        p = input("Password: ")

        success, data = login(u, p)

        if success:
            current_session = create_session(u, data["role"], data["department"])
            print(f"Logged in as {u} ({data['role']})")
            action_loop()
        else:
            print(data)

    # ---------- ADD USER ----------
    elif choice == "2":
        users = load_users()

        # bootstrap: create first admin
        if not users:
            print("No users found. Create initial admin.")
            u = input("Username: ")
            p = input("Password: ")
            print(register(u, p, "admin", "CS"))
            continue

        # require admin session
        if not require_auth():
            continue

        session = get_session(current_session)

        if session["role"] != "admin":
            print("Only admin can add users")
            continue

        u = input("New username: ")
        p = input("Password: ")
        r = input("Role (admin/user): ")
        d = input("Department: ")

        print(register(u, p, r, d))

    # ---------- EXIT ----------
    elif choice == "3":
        break