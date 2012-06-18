#===============================================================================
# -*- coding: UTF-8 -*-
# Module        : log
# Author        : Vincent BESANCON aka 'v!nZ' <besancon.vincent@gmail.com>
# Description   : Base to have some logging.
#-------------------------------------------------------------------------------
# This file is part of NagiosPPT (Nagios Python Plugin Template).
#
# NagiosPPT is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# NagiosPPT is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with NagiosPPT.  If not, see <http://www.gnu.org/licenses/>.
#===============================================================================

import logging as log

# Setup basic logging
log.basicConfig(format='[%(levelname)s] (%(module)s) %(message)s')
logger = log.getLogger('monitoring')
logger.setLevel(log.INFO)

# TODO: find a way to show the correct module name where this is called.
def debug_multiline(message):
    for line in message.splitlines():
        logger.debug("\t%s" % line)
