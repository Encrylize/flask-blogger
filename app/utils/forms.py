from flask import redirect, url_for
from flask_wtf import Form
from wtforms import HiddenField

from app.utils.helpers import get_redirect_target, is_safe_url


class RedirectForm(Form):
    """ Redirects the client to another page on submit. """

    next = HiddenField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.next.data:
            self.next.data = get_redirect_target() or ''

    def redirect(self, endpoint='main.index', **values):
        """
        Redirects the client to endpoint if no other safe redirect target is found.

        Args:
            endpoint: The endpoint to redirect to, defaults to 'main.index'
            **values: Values for the endpoint

        Returns:
            A redirection to the URL in the next field, returned by get_redirect_target()
            or endpoint, prioritized in that order.

        """

        if is_safe_url(self.next.data):
            return redirect(self.next.data)

        target = get_redirect_target()
        return redirect(target or url_for(endpoint, **values))

    def populate_obj(self, obj):
        for name, field in self._fields.items():
            if name != 'next':
                field.populate_obj(obj, name)
