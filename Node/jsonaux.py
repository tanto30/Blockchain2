from json import dumps, JSONEncoder


class CustomJSON(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return obj.__dict__


def jsonify(obj):
    return dumps(obj, indent=4, sort_keys=True, cls=CustomJSON)
