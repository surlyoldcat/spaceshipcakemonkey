import json
import boto3

monkeydb = None


def load_db():
    s3 = boto3.resource('s3')
    obj = s3.Object('rkt-rando-temp', 'monkeygraph/db.json')
    return json.loads(obj.get()['Body'].read().decode('utf-8'))


def lambda_handler(event, context):
    # this Resolver only looks up Cakes for a Monkey.
    # we expect the event to have a Monkey in the Source field.
    print('Event: {}'.format(event))
    global monkeydb
    if not monkeydb:
        monkeydb = load_db()

    if event['info']['parentTypeName'] == 'Monkey':
        m = lookup_monkey(event['source']['id'])
        return resolve_monkeycakes(m)
    else:
        raise Exception('failed to parse query')


def resolve_monkeycakes(monkey):
    if not monkey['cakeIds']:
        return []

    cakes = monkeydb['cakes']
    matches = [to_cake_gql(c) for c in cakes if c['cakeId'] in monkey['cakeIds']]
    return matches


def lookup_monkey(id):
    for m in monkeydb['monkeys']:
        if m['id'] == id:
            return m
    return


def to_cake_gql(cake_dict) -> dict:
    return {
        'cakeId': cake_dict['cakeId'],
        'cakeType': cake_dict['cakeType'],
    }