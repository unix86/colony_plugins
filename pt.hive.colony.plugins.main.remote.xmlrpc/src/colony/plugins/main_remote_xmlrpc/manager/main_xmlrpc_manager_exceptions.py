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

class ServiceException(Exception):
    """
    The service exception class.
    """

    pass

class ServiceRequestNotTranslatable(ServiceException):
    """
    The service request not translatable class.
    """

    pass

class BadServiceRequest(ServiceException):
    """
    The bad service request class.
    """

    pass

class InvalidNumberArguments(BadServiceRequest):
    """
    The invalid number arguments class.
    """

    def __init__(self, message):
        """
        Constructor of the class.
        
        @type message: String
        @param message: The message to be printed.
        """

        BadServiceRequest.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.
        
        @rtype: String
        @return: The string representation of the class.
        """

        return "Invalid number of arguments: %s" % self.message

class InvalidMethod(BadServiceRequest):
    """
    The invalid method class.
    """

    def __init__(self, message):
        """
        Constructor of the class.
        
        @type message: String
        @param message: The message to be printed.
        """

        BadServiceRequest.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.
        
        @rtype: String
        @return: The string representation of the class.
        """

        return "Invalid Method: %s" % self.message

class XmlEncodeException(Exception):
    """
    The xml encode exception class.
    """

    def __init__(self, object):
        """
        Constructor of the class.
        
        @type object: Object
        @param object: The object containing the encoding problems.
        """

        Exception.__init__(self)
        self.object = object

    def __str__(self):
        """
        Returns the string representation of the class.
        
        @rtype: String
        @return: The string representation of the class.
        """

        return "Object not encodeable: %s" % self.object

class XmlDecodeException(Exception):
    """
    The xml decode exception class.
    """

    def __init__(self, message):
        """
        Constructor of the class.
        
        @type message: String
        @param message: The message to be printed.
        """

        Exception.__init__(self)
        self.message = message

    def __str__(self):
        """
        Returns the string representation of the class.
        
        @rtype: String
        @return: The string representation of the class.
        """

        return self.message
