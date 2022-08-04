
import pymongo
from todo_app.data.item import Item
from bson.objectid import ObjectId
import os

class TrelloItems:

    def __init__(self):
        self.client = pymongo.MongoClient(os.getenv('MONGO_CONNECTION_STRING'))
        self.db = self.client[os.getenv('MONGO_DATABSE_NAME')]
        self.items = self.db.items

    def get_items(self):
        """
        Fetches all items for the default board.
        
        Returns:
            list: The list of items.
        """

        items = [Item(item) for item in self.items.find()]
        sorted_items = sorted(items, key=lambda item: item.name)

        return sorted_items

    def get_item_by_id(self, item_id):
        """
        Fetches details of item by id.
        
        Returns:
            item: The details of item.
        """

        item = self.items.find_one({"_id": ObjectId(item_id)})
        return Item(item)

    def add_item(self, name):
        """
        Adds a new item with specific name.

        Returns: The created item or None if item does not exist.
        """
        item = {
            "name": name,
            "status": 'To Do'
        }

        self.items.insert_one(item)

    def change_status(self, item_id):
        """
        Move the item to the next list.

        Returns: The updated item or None if item does not exist.
        """
        current_item = self.get_item_by_id(item_id)
        
        if current_item.status == 'To Do':
            new_status = 'Doing'
        elif current_item.status == 'Doing':
            new_status = 'Done'
        else:
            new_status = 'To Do'
        
        self.items.update_one({"_id": ObjectId(item_id)}, {"$set": {"status": new_status}})
