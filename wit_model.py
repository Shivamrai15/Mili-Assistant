import wit
from encryption import Encryption


access_token = Encryption(
    b"gAAAAABkpXgF4ifploe4p3kNLgW3W8_zYF9Iaq7CqQtrLrA1e1SiW1jjAbOZmty72DVlfojnDJXQqwy2HUw9fgFRDXLeflrtBnL5Lb7NTaVJhkexabpKfcR-6UfqOGiASxzaOMhfVPqF"
).decrypt_text()
client = wit.Wit(access_token=access_token)


def model(query):
    response = client.message(query)
    entities = response["entities"]
    intent = response["intents"][0]["name"]
    return entities, intent
