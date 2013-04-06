# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, division
import importlib


def is_available(*capacities):
    """Detects if the environment is available for use in the (optionally)
    specified capacities.
    """

    try:
        # Attempt to import cyclone
        importlib.import_module('cyclone')

        # TODO: check to see if cyclone is actually being used.

        # Successfully detected the cyclone connector.
        return True

    except ImportError:
        # Cyclone is not installed
        return False
