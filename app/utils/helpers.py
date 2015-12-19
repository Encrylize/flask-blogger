def get_or_create(model, **kwargs):
    """
    Gets or creates an instance of model.

    Args:
        model: SQLAlchemy model
        **kwargs: Model properties

    Returns:
        An instance of model and True if it was created, False if it was not.

    """

    instance = model.query.filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        instance = model(**kwargs)
        return instance, True
