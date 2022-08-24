from todo_app.data.item import Item
from todo_app.data.view_model import ViewModel

def test_it_returns_to_do_items():
    items = [
        Item({"_id": 1, "name": 'Item 1', "status": 'To Do'}),
        Item({"_id": 2, "name": 'Item 1', "status": 'Doing'}),
        Item({"_id": 3, "name": 'Item 1', "status": 'Done'}),
        Item({"_id": 4, "name": 'Item 1', "status": 'To Do'}),
    ]

    view_model = ViewModel(items)

    assert len(view_model.to_do_items) == 2

def test_it_returns_doing_items():
    items = [
        Item({"_id": 1, "name": 'Item 1', "status": 'To Do'}),
        Item({"_id": 2, "name": 'Item 1', "status": 'Doing'}),
        Item({"_id": 3, "name": 'Item 1', "status": 'Done'}),
        Item({"_id": 4, "name": 'Item 1', "status": 'Doing'}),
    ]

    view_model = ViewModel(items)

    assert len(view_model.doing_items) == 2

def test_it_returns_done_items():
    items = [
        Item({"_id": 1, "name": 'Item 1', "status": 'To Do'}),
        Item({"_id": 2, "name": 'Item 1', "status": 'Doing'}),
        Item({"_id": 3, "name": 'Item 1', "status": 'Done'}),
        Item({"_id": 4, "name": 'Item 1', "status": 'Done'}),
    ]
    view_model = ViewModel(items)

    assert len(view_model.done_items) == 2
    