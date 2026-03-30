import json

def load_resources():
    try:
        with open("resources.json") as f:
            return json.load(f)
    except:
        return []

def save_resources(data):
    with open("resources.json", "w") as f:
        json.dump(data, f, indent=4)

def get_resource(rid):
    for r in load_resources():
        if r["id"] == rid:
            return r
    return None

def add_resource(owner, content):
    resources = load_resources()
    ids = [r["id"] for r in resources]
    rid = max(ids, default=0) + 1

    resources.append({
        "id": rid,
        "owner": owner,
        "content": content
    })

    save_resources(resources)
    return rid

def delete_resource(rid):
    resources = load_resources()
    resources = [r for r in resources if r["id"] != rid]
    save_resources(resources)
