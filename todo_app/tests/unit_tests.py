from todo_app.data.card import Card
from todo_app.data.view_model import ViewModel

def test_it_returns_to_do_items():
    items = [
        Card(1, 'Item 1', 'To Do'),
        Card(2, 'Item 2', 'Doing'),
        Card(3, 'Item 3', 'Done'),
        Card(4, 'Item 1', 'To Do'),
    ]

    view_model = ViewModel(items)

    assert len(view_model.to_do_items) == 2
    