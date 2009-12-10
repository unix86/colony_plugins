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

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Ter, 21 Out 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os
import sys
import getopt
import logging

import os.path

import libs.extension_system

import wiki_parser
import wiki_visitor
import wiki_html_generation
import wiki_extension_system

WIKI_EXTENSIONS = ("wiki", "wik")
""" The valid wiki extensions list """

class WikiGenerator:
    """
    The wiki generator class.
    """

    extension_manager = None
    """ The extension manager """

    configuration_map = {}
    """ The configuration map """

    def __init__(self):
        """
        Constructor of the class.
        """

        # creates a new extension manager
        self.extension_manager = libs.extension_system.ExtensionManager(["./extensions"])
        self.extension_manager.set_extension_class(wiki_extension_system.WikiExtension)
        self.extension_manager.start_logger()
        self.extension_manager.load_system()

        # creates the configuration map
        self.configuration_map = {"AUTO_NUMBERED_SECTIONS" : True}

    def generate_wiki(self, file_path, verbose, debug):
        """
        Generates the wiki structure for the given file path,
        and options.

        @type file_path: String
        @param file_path:  The file path to generate the wiki structure.
        @type verbose: bool
        @param verbose: If the log is going to be of type verbose.
        @type debug: bool
        @param debug: If the log is going to be of type debug.
        """

        # walks the file path
        os.path.walk(file_path, self.generate_wiki_file, None)

    def generate_wiki_file(self, args, file_path, names):
        """
        Generates the wiki for the given file and arguments.

        @type args: List
        @param args:  The arguments for the generation.
        @type file_path: String
        @param file_path: The file path for the generation.
        @type names: List
        @param names: The list of name for the current file path.
        """

        # iterates over all the names
        for name in names:
            # splits the name
            name_splitted = name.split(".")

            # retrieves the name extension
            name_extension = name_splitted[-1]

            # in case the name extension is valid
            if name_extension in WIKI_EXTENSIONS:
                # creates the full file name
                full_file_path = file_path + "/" + name

                # retrieves the partial name
                partial_name = "".join(name_splitted[:-1])

                # creates the full partial name
                full_partial_name = file_path + "/" + partial_name

                # prints an info message
                logging.error("Processing: %s" % full_file_path)

                # opens the wiki file
                wiki_file = open(full_file_path)

                # reads the wiki file contents
                wiki_file_contents = wiki_file.read()

                # closes the wiki file
                wiki_file.close()

                # strips the wiki file contents (to remove extra spaces and lines)
                wiki_file_contents = wiki_file_contents.strip()

                # parses the javascript file retrieving the result
                parse_result = wiki_parser.parser.parse(wiki_file_contents)

                # creates the generator visitor
                generation_visitor = wiki_html_generation.HtmlGenerationVisitor()
                generation_visitor.set_extension_manager(self.extension_manager)
                generation_visitor.set_configuration_map(self.configuration_map)

                parse_result.accept_double(generation_visitor)

                # retrieves the html value
                html_value = generation_visitor.get_string_buffer().getvalue()

                # opens the html file
                html_file = open(full_partial_name + ".html", "w+")

                # writes the html value to the html file
                html_file.write(html_value)

                # closes the html file
                html_file.close()

if __name__ == "__main__":
    # starts the verbose flag as false
    verbose = False

    # starts the debug flag as false
    debug = False

    # start the file path value as None
    file_path = None

    # retrieves the argument options
    opts, args = getopt.getopt(sys.argv[1:], "vdf:", ["verbose", "debug", "file="])

    # iterates over all the given options
    for option, value in opts:
        if option in ("-v", "--verbose"):
            verbose = True
        elif option in ("-d", "--debug"):
            debug = True
        elif option in ("-f", "--file"):
            file_path = value

    # creates the wiki generator
    wiki_generator = WikiGenerator()

    # generates the wiki
    wiki_generator.generate_wiki(file_path, verbose, debug)
