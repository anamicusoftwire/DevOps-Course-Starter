class Item:

    def __init__(self, id, name, status):
        self.name = name
        self.id = id
        self.status = status

    def __init__(self, item):
        self.name = item["name"]
        self.id = item["_id"]
        self.status = item["status"]

    def __repr__(self) -> str:
        return str({
            "id": self.id,
            "name": self.name,
            "status": self.status
        })

