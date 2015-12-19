from urllib.parse import urljoin, urlparse

from flask import redirect, request, url_for
from flask_wtf import Form
from wtforms import HiddenField


class RedirectForm(Form):
    """ Redirects the client to another page on submit. """

    next = HiddenField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.next.data:
            self.next.data = self.get_redirect_target() or ''

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

        if self.is_safe_url(self.next.data):
            return redirect(self.next.data)

        target = self.get_redirect_target()
        return redirect(target or url_for(endpoint, **values))

    @staticmethod
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
        return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

    @classmethod
    def get_redirect_target(cls):
        """
        Gets a safe redirect target.

        Returns:
            The first safe redirect target.

        """

        for target in request.args.get('next'), request.referrer:
            if not target:
                continue
            elif cls.is_safe_url(target):
                return target
