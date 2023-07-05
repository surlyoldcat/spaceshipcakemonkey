import json
import boto3


monkeydb = None


def load_db():
    s3 = boto3.resource('s3')
    obj = s3.Object('rkt-rando-temp', 'monkeygraph/db.json')
    return json.loads(obj.get()['Body'].read().decode('utf-8'))


def lambda_handler(event, context):
    # This resolver handles the allSpaceships query, and the field-level
    # resolver for Monkey.spaceships. Differentiated by parentTypeName
    # and fieldName in the event's metadata.
    print('Event: {}'.format(event))
    global monkeydb
    if not monkeydb:
        monkeydb = load_db()

    if event['info']['parentTypeName'] == 'Monkey':
        m = lookup_monkey(event['source']['id'])
        return resolve_monkeyspaceships(m)
    elif event['info']['fieldName'] == 'allSpaceships':
        return resolve_allspaceships()
    else:
        raise Exception('failed to parse query')


def resolve_monkeyspaceships(monkey):
    if not monkey['spaceshipIds']:
        return []

    ships = monkeydb['spaceships']
    matches = [to_spaceship_gql(s) for s in ships if s['spaceshipId'] in monkey['spaceshipIds']]
    return matches


def resolve_allspaceships():
    ships = [to_spaceship_gql(s) for s in monkeydb['spaceships']]
    return ships


def lookup_monkey(id):
    for m in monkeydb['monkeys']:
        if m['id'] == id:
            return m
    return None


def to_spaceship_gql(ss_dict) -> dict:
    return {
        'spaceshipId': ss_dict['spaceshipId'],
        'name': ss_dict['name'],
        'type': ss_dict['type'],
        'crew': []
    }
