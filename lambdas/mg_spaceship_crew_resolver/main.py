import json
import boto3

monkeydb = None


def load_db():
    s3 = boto3.resource('s3')
    obj = s3.Object('rkt-rando-temp', 'monkeygraph/db.json')
    data = json.loads(obj.get()['Body'].read().decode('utf-8'))
    return data


def lambda_handler(event, context):
    # NOTE this is a batch resolver, so the event is a list (of spaceships).
    # Each event in the input list should have a Source that is a Spaceship.
    # This is Python, so it doesn't matter so much, but for Go, it is
    # critically important that the return list be the same length and order
    # as the input list.
    print('Event: {}'.format(event))
    global monkeydb
    if not monkeydb:
        monkeydb = load_db()

    crews = []
    for ev in event:
        print("looking up crew for {}".format(ev['source']['name']))
        spaceship_id = ev['source']['spaceshipId']
        monkeys = get_monkeys_on_spaceship(spaceship_id)
        crews.append(monkeys)

    return crews


def get_monkeys_on_spaceship(spaceship_id: int):
    crew = [to_monkey_gql(m) for m in monkeydb['monkeys'] if spaceship_id in m['spaceshipIds']]
    return crew


def to_monkey_gql(monkeydb_dict: dict) -> dict:
    return {
        'id': monkeydb_dict['id'],
        'name': monkeydb_dict['name'],
        'species': monkeydb_dict['species'],
        'cakes': [],
        'spaceships': []
    }




