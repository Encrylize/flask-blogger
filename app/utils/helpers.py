from urllib.parse import urljoin, urlparse

from flask import request


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


def is_safe_url(target):
    """
    Checks if a URL is safe.

    Args:
        target: The URL to check

    Returns:
        True if the URL is safe, False if it is not.

    """

    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http',
                               'https') and ref_url.netloc == test_url.netloc


def get_redirect_target():
    """
    Gets a safe redirect target.

    Returns:
        The first safe redirect target.

    """

    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        elif is_safe_url(target):
            return target
