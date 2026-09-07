def individual_serial(todo) -> dict:
    return {
        "id": str(todo["_id"]),
        "text": todo["text"],
        "sender": todo["sender"],
        "timestamp": todo["timestamp"]
    }

def list_of_serials(todos) -> list:
    return [individual_serial(todo) for todo in todos]
