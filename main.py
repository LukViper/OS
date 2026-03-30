from auth import register, login, load_users
from session import *
from rbac import check_access
from abac import check_abac
from resource import *
import time

current_session = None

def require_auth():
    global current_session
    if not current_session or not validate_session(current_session):
        print("Session expired. Login again.")
        current_session = None
        return False
    return True

def prompt(session):
    remaining = int(60 - (time.time() - session["created"]))
    return f"[{session['user']}:{session['role']} | {remaining}s] >> "

def action_loop():
    global current_session

    while True:
        if not require_auth():
            break

        session = get_session(current_session)
        cmd = input(prompt(session)).strip().split()

        if not cmd:
            continue

        action = cmd[0]

        # ---------- COMMAND HANDLING ----------

        if action == "logout":
            destroy_session(current_session)
            current_session = None
            print("Logged out")
            break

        if action == "exit":
            exit()

        if action == "adduser":
            if session["role"] != "admin":
                print("Only admin allowed")
                continue

            u = input("Username: ")
            p = input("Password: ")
            r = input("Role: ")
            d = input("Department: ")

            print(register(u, p, r, d))
            continue


        # ---------- LIST (MUST BE BEFORE VALIDATION) ----------
        if action == "profile":
            print("\n--- USER PROFILE ---")
            print(f"User       : {session['user']}")
            print(f"Role       : {session['role']}")
            print(f"Department : {session['department']}")

            remaining = int(60 - (time.time() - session["created"]))
            if remaining < 0:
                remaining = 0

            print(f"Session TTL: {remaining}s")
            print("---------------------\n")
            continue
        if action == "list":
            resources = list_resources()

            if not resources:
                print("No resources found")
                continue

            for r in resources:
                print(f"ID: {r['id']} | Name: {r['name']} | Owner: {r['owner']}")
            continue


        # ---------- VALID ACTIONS ----------
        if action not in ["read", "write", "delete"]:
            print("Invalid action")
            continue


        # ---------- RBAC ----------
        if not check_access(session["role"], action):
            print("Access denied")
            continue


        # ---------- OPERATIONS ----------
        if action == "read":
            rid = int(input("Resource ID: "))
            res = get_resource(rid)

            if not res:
                print("Not found")
                continue

            print(res["content"])


        elif action == "write":
            name = input("File name: ")
            content = input("Content: ")

            rid = add_resource(session["user"], content, name)
            print(f"Created resource {rid}")


        elif action == "delete":
            rid = int(input("Resource ID: "))
            res = get_resource(rid)

            if not res:
                print("Not found")
                continue

            if not check_abac(session, "delete", res):
                print("ABAC denied")
                continue

            delete_resource(rid)
            print("Deleted")
def menu():
    print("""
1. login
2. adduser
3. exit
""")

while True:
    menu()
    c = input(">> ")

    if c == "1":
        u = input("Username: ")
        p = input("Password: ")

        success, data = login(u, p)

        if success:
            current_session = create_session(u, data["role"], data["department"])
            print(f"Logged in as {u} ({data['role']})")
            action_loop()
        else:
            print(data)

    elif c == "2":
        users = load_users()

        if not users:
            print("Create initial admin")
            u = input("Username: ")
            p = input("Password: ")
            print(register(u, p, "admin", "CS"))
            continue

        if not require_auth():
            continue

        session = get_session(current_session)

        if session["role"] != "admin":
            print("Only admin allowed")
            continue

        u = input("Username: ")
        p = input("Password: ")
        r = input("Role: ")
        d = input("Department: ")

        print(register(u, p, r, d))

    elif c == "3":
        break
