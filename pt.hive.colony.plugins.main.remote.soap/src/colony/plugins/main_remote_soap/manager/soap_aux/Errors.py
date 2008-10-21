#!/usr/bin/python
# -*- coding: Cp1252 -*-

# Hive Colony Framework
# Copyright (C) 2008 Hive Solutions Lda.
#
# This file is part of Hive Colony Framework.
#
# Hive Colony Framework is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hive Colony Framework is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Hive Colony Framework. If not, see <http://www.gnu.org/licenses/>.

__author__ = "Jo�o Magalh�es <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import exceptions

################################################################################
# Exceptions
################################################################################
class Error(exceptions.Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return "<Error : %s>" % self.msg
    __repr__ = __str__
    def __call__(self):
        return (msg,)

class RecursionError(Error):
    pass

class UnknownTypeError(Error):
    pass

class HTTPError(Error):
    # indicates an HTTP protocol error
    def __init__(self, code, msg):
        self.code = code
        self.msg  = msg
    def __str__(self):
        return "<HTTPError %s %s>" % (self.code, self.msg)
    __repr__ = __str__
    def __call___(self):
        return (self.code, self.msg, )

class UnderflowError(exceptions.ArithmeticError):
    pass
