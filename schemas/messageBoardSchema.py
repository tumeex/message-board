def individual_serial(todo) -> dict:
    return {
        "id": str(todo["_id"]),
        "messages": todo["messages"],
        "members": todo["members"],
        "owner": todo["owner"],
    }

def list_of_serials(todos) -> list:
    return [individual_serial(todo) for todo in todos]
