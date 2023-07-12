
db = [
    {
        "id": 1,
        "name": "USS Fortinbras",
        "type": "attack sub"
    },
    {
        "id": 2,
        "name": "Marianas Trencher",
        "type": "titanium spheroid"
    },
    {
        "id": 3,
        "name": "monkeysub",
        "type": "a sub full of monkeys"
    }
]


def lambda_handler(event, context):
    if event['info']['fieldName'] == 'getSubmarine':
        # return a single Monkey
        return resolve_getsubmarine(event['arguments']['id'])
    elif event['info']['fieldName'] == 'allSubmarines':
        # return a list of Monkeys
        return resolve_allsubmarines()
    else:
        raise Exception('failed to parse query')


def resolve_getsubmarine(id):
    for item in db:
        if item['id'] == id:
            return to_submarine_gql(item)
    return None


def resolve_allsubmarines():
    subs = [to_submarine_gql(s) for s in db]
    return subs


def to_submarine_gql(db_dict: dict) -> dict:
    return {
        'id': db_dict['id'],
        'name': db_dict['name'],
        'type': db_dict['type']
    }
