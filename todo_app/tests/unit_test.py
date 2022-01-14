from todo_app.data.item import Item
from todo_app.data.view_model import ViewModel

def test_it_returns_to_do_items():
    items = [
        Item(1, 'Item 1', 'To Do'),
        Item(2, 'Item 2', 'Doing'),
        Item(3, 'Item 3', 'Done'),
        Item(4, 'Item 4', 'To Do'),
    ]

    view_model = ViewModel(items)

    assert len(view_model.to_do_items) == 2

def test_it_returns_doing_items():
    items = [
        Item(1, 'Item 1', 'To Do'),
        Item(2, 'Item 2', 'Doing'),
        Item(3, 'Item 3', 'Done'),
        Item(4, 'Item 4', 'Doing'),
    ]

    view_model = ViewModel(items)

    assert len(view_model.doing_items) == 2

def test_it_returns_done_items():
    items = [
        Item(1, 'Item 1', 'To Do'),
        Item(2, 'Item 2', 'Doing'),
        Item(3, 'Item 3', 'Done'),
        Item(4, 'Item 4', 'Done'),
    ]

    view_model = ViewModel(items)

    assert len(view_model.done_items) == 2
    