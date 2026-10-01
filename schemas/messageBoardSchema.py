async def individual_serial(todo) -> dict:
    return await {
        #"id": str(todo["_id"]),
        "id": todo["id"],
        "messages": todo["messages"],
        "members": todo["members"],
        "owner": todo["owner"],
    }

async def list_of_serials(todos) -> list:
    return [await individual_serial(todo) for todo in todos]
