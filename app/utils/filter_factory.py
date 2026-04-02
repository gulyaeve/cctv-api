


def filter_factory(filter_mapping: dict, filter_by):
    conditions = []
    for key, value in filter_by.items():
        if key in filter_mapping:
            conditions.append(filter_mapping[key] == value)
        else:
            print(f"Warning: Unknown filter key '{key}' ignored.")
    return conditions