
from todo_app.data.card import Card
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

    return next((list_with_cards for list_with_cards in lists if list_with_cards['name'] == name), None)

def get_cards():
    """
    Fetches all cards for the default board.
    
    Returns:
        list: The list of cards.
    """

    lists = get_lists()
    cards = []
    
    for list_with_cards in lists:
        for card in list_with_cards['cards']:
            new_card = Card(card['id'], card['name'], list_with_cards['name'])
            cards.append(new_card)

    return cards

def get_card_by_id(card_id):
    """
    Fetches details of card by id.
    
    Returns:
        card: The details of card.
    """

    cards = get_cards()
    return next((card for card in cards if card.id == card_id), None)

def add_card(name):
    """
    Adds a new card with specific name.

    Returns: The created card or None if card does not exist.
    """
    list_with_cards = get_list_by_name('To Do')
    params = get_params_with_auth({'name': name, 'idList': list_with_cards['id']})
    url = get_url('/1/cards')

    response = requests.post(url = url, params = params)
    card = response.json()

    return Card(card['id'], card['name'], list_with_cards['name'])

def change_status(card_id):
    """
    Move the card to the next list.

    Returns: The updated card or None if card does not exist.
    """
    current_card = get_card_by_id(card_id)
    if current_card.status == 'To Do':
        new_status = 'Doing'
    elif current_card.status == 'Doing':
        new_status = 'Done'
    else:
        new_status = 'To Do'
    new_list = get_list_by_name(new_status)
    params = get_params_with_auth({'idList': new_list['id']})
    url = get_url('/1/cards/%s' % card_id)

    response = requests.put(url = url, params = params)
    new_card = response.json()
    return Card(new_card['id'], new_card['name'], new_status)
