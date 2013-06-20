# -*- coding: utf-8 -*-
"""
Describes the authentication protocols and generalizations used to
authenticate access to a resource endpoint.
"""
from __future__ import absolute_import, unicode_literals, division
from armet import http
import base64


class Authentication(object):

    def __init__(self, **kwargs):
        """Initialize authentication protocol; establish parameters."""

        #! Whether returning `None` from `authenticate` indicates
        #! unauthenticated; or, simply no authenticated user.
        self.allow_anonymous = kwargs.get('allow_anonymous', True)

    def authenticate(self, resource):
        """Gets the a user if they are authenticated; else None.

        @retval False    Unable to authenticate.
        @retval None     Able to authenticate but failed.
        @retval <user>   User object representing the current user.
        """
        return None

    def unauthenticated(self):
        """
        Callback that is invoked when after a user is determined to
        be unauthenticated.
        """
        raise http.exceptions.Forbidden()


class BasicAuthentication(Authentication):

    def __init__(self, **kwargs):
        kwargs.setdefault('allow_anonymous', False)
        super(BasicAuthentication, self).__init__(**kwargs)

    def authenticate(self, resource):
        # Retrieve the authorization header.
        header = resource.request.headers.get('Authorization')

        try:
            # Split the authorization header into method and credentials.
            method, creds = (header or '').split(' ', 1)

        except ValueError:
            # Strange format in the header.
            return False

        if method.lower() != 'basic':
            # Not BASIC authentication.
            return False

        try:
            # Decode creds into username and password.
            creds = base64.b64decode(creds.encode('utf8')).decode('utf8')
            username, password = creds.split(':', 1)

        except ValueError:
            # Strange format in the authorization header.
            # We know enough that the user is attempting basic authentication.
            return None

        # Retreive and return the user object.
        return self.get_user(resource, username=username, password=password)

    def get_user(self, **kwargs):
        """
        Callback that is invoked when a user is attempting to be
        authenticated with a set of credentials.
        """
        return None