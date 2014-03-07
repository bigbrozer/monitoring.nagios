# -*- coding: utf-8 -*-
# Copyright (C) Vincent BESANCON <besancon.vincent@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
# OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""Base module for all probes."""

import logging as log

logger = log.getLogger('monitoring.nagios.probes')


class Probe(object):
    """Base class for defining a new Probe."""
    def __init__(self):
        logger.debug('')
        logger.debug('=== BEGIN NEW PROBE INIT ===')
        logger.debug('Instanciating a new probe of type %s.',
                     self.__class__.__name__)

        if 'Probe' == self.__class__.__name__:
            logger.debug('=== END PROBE INIT ===')