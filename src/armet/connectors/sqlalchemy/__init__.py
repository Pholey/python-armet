# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, division


def is_available(*capacities):
    """
    Detects if the environment is available for use in
    the (optionally) specified capacities.
    """
    try:
        # Attempted import
        import sqlalchemy  # flake8: noqa

        # TODO: Add additional checks to assert that flask is actually
        #   in use and available.

        # Detected connector.
        return True

    except ImportError:
        # Failed to import.
        return False