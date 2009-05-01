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

__revision__ = "$LastChangedRevision: 1089 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2009-01-22 23:19:39 +0000 (qui, 22 Jan 2009) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

TEST_IMAGE_PATH = "printing/manager/resources/test_logo.png"
""" The test image relative path """

import printing_language_parser

class PrintingManager:
    """
    The printing manager class.
    """

    printing_manager_plugin = None
    """ The printing manager plugin """

    def __init__(self, printing_manager_plugin):
        """
        Constructor of the class.

        @type printing_manager_plugin: PrintingManagerPlugin
        @param printing_manager_plugin: The printing manager plugin.
        """

        self.printing_manager_plugin = printing_manager_plugin

    def print_test(self, printing_options = {}):
        self.printing_manager_plugin.printing_plugins[0].print_test(printing_options)

    def print_test_image(self, printing_options = {}):
        # retrieves the plugin manager
        plugin_manager = self.printing_manager_plugin.manager

        # retrieves the plugin path
        plugin_path = plugin_manager.get_plugin_path_by_id(self.printing_manager_plugin.id)

        # creates the complete image path
        image_path = plugin_path + "/" + TEST_IMAGE_PATH

        self.printing_manager_plugin.printing_plugins[0].print_test_image(image_path, printing_options)

    def print_printing_language(self, printing_language_string, printing_options = {}):
        # creates a new printing language parser
        parser = printing_language_parser.PrintingLanguageParser()

        # sets the printing language string in the parser
        parser.string = printing_language_string

        # parses the string
        parser.parse_string()

        # retrieves the printing document
        printing_document = parser.get_value()

        self.printing_manager_plugin.printing_plugins[0].print_printing_language(printing_document, printing_options)
