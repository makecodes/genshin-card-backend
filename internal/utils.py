def money_to_db(value):
    value = str(value)
    value = value.replace(".", "")
    value = value.replace(",", ".")
    return value


def empty_object():
    return {}


def empty_list():
    return []
