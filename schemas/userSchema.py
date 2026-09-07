def individual_serial(todo) -> dict:
    return {
        "id": str(todo["_id"]),
        "name": todo["name"],
        "password": todo["password"]
    }

def list_of_serials(todos) -> list:
    return [individual_serial(todo) for todo in todos]
