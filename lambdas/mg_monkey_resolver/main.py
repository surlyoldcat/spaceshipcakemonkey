import json
import boto3

monkeydb = None


def load_db():
    # This is a stand-in for a real data access layer. It
    # just grabs the JSON file from S3.
    s3 = boto3.resource('s3')
    obj = s3.Object('rkt-rando-temp', 'monkeygraph/db.json')
    data = json.loads(obj.get()['Body'].read().decode('utf-8'))
    return data


def lambda_handler(event, context):
    # Resolver for BOTH the getMonkey and allMonkeys queries.
    # I just use a 'switch' on the field name to determine which
    # query was requested.
    print('Event: {}'.format(event))
    # Cache the JSON db in lambda memory. Hacky.
    global monkeydb
    if not monkeydb:
        monkeydb = load_db()

    if event['info']['fieldName'] == 'getMonkey':
        # return a single Monkey
        return resolve_getmonkey(event['arguments']['id'])
    elif event['info']['fieldName'] == 'allMonkeys':
        # return a list of Monkeys
        return resolve_allmonkeys()
    else:
        raise Exception('failed to parse query')


def resolve_allmonkeys():
    monkeys = [to_monkey_gql(m) for m in monkeydb['monkeys']]
    return monkeys


def resolve_getmonkey(id: int):
    # look up the Monkey data from the JSON file.
    for m in monkeydb['monkeys']:
        if m['id'] == id:
            return to_monkey_gql(m)
    return None


def to_monkey_gql(monkeydb_dict: dict) -> dict:
    # Note, the cakes and spaceships zero values are not really required,
    # AppSync will populate them with data from field-specific resolvers.
    # I'm just including them here for completeness.
    return {
        'id': monkeydb_dict['id'],
        'name': monkeydb_dict['name'],
        'species': monkeydb_dict['species'],
        'cakes': [],
        'spaceships': []
    }
