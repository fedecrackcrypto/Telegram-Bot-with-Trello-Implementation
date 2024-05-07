import requests

BASE_URL = "https://api.trello.com"

async def create_card(id_list: str, API_KEY: str, API_TOKEN: str, **kwargs) -> bool:
    """
    This function accepts the following keyword arguments:
    
    - name (str): The name for the card.
    - desc (str): The description for the card.
    - pos  (oneOf [string, number]): The position of the new card. top, bottom, or a positive float.
    - due (string): A due date for the card
    - start (string): The start date of a card, or null
    - coordinates (string): For use with/by the Map View. Should take the form latitude,longitude
    - idLabels (array<TrelloID>): Comma-separated list of label IDs to add to the card
    """
    url = f"{BASE_URL}/1/cards"
    headers = {"Accept": "application/json"}
    query = {
            'idList': id_list,
            'key': API_KEY,
            'token': API_TOKEN
            }
    for key, value in kwargs.items():
        query[str(key)] = value
    response = requests.post(url, headers=headers,params=query)

    if response.status_code == 200:
        print("Card added")
        return True
    else:
        print("Error creating Card:", response.text)
        return {response.text}

async def get_board(id_board, API_KEY, API_TOKEN, **kwargs):
    
    url = f"{BASE_URL}/1/boards/{id_board}"
    headers = {"Accept": "application/json"}
    query = {
            'key': API_KEY,
            'token': API_TOKEN
            }
    for key, value in kwargs.items():
        query[str(key)] = value
    response = requests.get(url, headers=headers,params=query)

    if response.status_code == 200:
        print(response.content)
    else:
        print("Error getting board:", response.text)




