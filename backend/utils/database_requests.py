def get_value_from_model(model, **kwargs):
    try:
        value = model.objects.get(**kwargs)
    except:
        value = None
    return value


def filter_objects_from_model(model, **kwargs):
    try:
        value = model.objects.filter(**kwargs)
    except:
        value = None
    return value


def get_all_objects_from_model(model):
    try:
        values = model.objects.all()
    except:
        values = None
    return values
