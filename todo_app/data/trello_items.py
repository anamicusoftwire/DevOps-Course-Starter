
from todo_app.data.item import Item
import requests
import os

_TRELLO_AUTH_PARAMS = {
    'key': os.getenv('TRELLO_API_KEY'),
    'token': os.getenv('TRELLO_TOKEN')
}

def get_url(relative_path):
    return os.getenv('TRELLO_BASE_URL') + relative_path

def get_params_with_auth(params = {}):
    all_params = _TRELLO_AUTH_PARAMS
    all_params.update(params)
    return all_params

def get_boards():
    """
    Fetches all boards from Trello.

    Returns:
        list: The list of boards.
    """

    params = get_params_with_auth()
    url = get_url('/1/members/me/boards')
    
    response = requests.get(url = url, params = params)
    return response.json()

def get_board_by_name(name):
    """
    Fetches board by name.

    Returns:
        list: The details of board or None if board does not exist.
    """

    boards = get_boards()
    return next((board for board in boards if board['name'] == name), None)

def get_lists():
    """
    Fetches all open lists for the default board.

    Returns:
        list: The list of lists.
    """

    board = get_board_by_name(os.getenv('TRELLO_DEFAULT_BOARD_NAME'))
    params = get_params_with_auth({'cards': 'open'})
    url = get_url('/1/boards/%s/lists' % board['id'])

    response = requests.get(url = url, params = params)
    return response.json()

def get_list_by_name(name):
    """
    Fetches list by name.

    Returns:
        list: The details of the list or None if it does not exist.
    """

    lists = get_lists()

    return next((list_with_items for list_with_items in lists if list_with_items['name'] == name), None)

def get_items():
    """
    Fetches all items for the default board.
    
    Returns:
        list: The list of items.
    """

    lists = get_lists()
    items = []
    
    for list_with_items in lists:
        for item in list_with_items['cards']:
            new_item = Item(item['id'], item['name'], list_with_items['name'])
            items.append(new_item)

    return items

def get_item_by_id(item_id):
    """
    Fetches details of item by id.
    
    Returns:
        item: The details of item.
    """

    items = get_items()
    return next((item for item in items if item.id == item_id), None)

def add_item(name):
    """
    Adds a new item with specific name.

    Returns: The created item or None if item does not exist.
    """
    list_with_items = get_list_by_name('To Do')
    params = get_params_with_auth({'name': name, 'idList': list_with_items['id']})
    url = get_url('/1/cards')

    response = requests.post(url = url, params = params)
    item = response.json()

    return Item(item['id'], item['name'], list_with_items['name'])

def change_status(item_id):
    """
    Move the item to the next list.

    Returns: The updated item or None if item does not exist.
    """
    current_item = get_item_by_id(item_id)
    if current_item.status == 'To Do':
        new_status = 'Doing'
    elif current_item.status == 'Doing':
        new_status = 'Done'
    else:
        new_status = 'To Do'
    new_list = get_list_by_name(new_status)
    params = get_params_with_auth({'idList': new_list['id']})
    url = get_url('/1/cards/%s' % item_id)

    response = requests.put(url = url, params = params)
    new_item = response.json()
    return Item(new_item['id'], new_item['name'], new_status)
