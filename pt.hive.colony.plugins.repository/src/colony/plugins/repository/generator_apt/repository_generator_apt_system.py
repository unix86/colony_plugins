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

__revision__ = "$LastChangedRevision: 8461 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2010-05-12 06:45:34 +0100 (qua, 12 Mai 2010) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os

ADAPTER_NAME = "apt"
""" The adapter name """

SOURCE_VALUE = "source"
""" The source value """

TARGET_VALUE = "target"
""" The target value """

CONTENTS_VALUE = "contents"
""" The contents value """

FILE_VALUE = "file"
""" The file value """

NAME_VALUE = "name"
""" The name value """

VERSION_VALUE = "version"
""" The version value """

ARCHITECTURE_VALUE = "architecture"
""" The architecture value """

NAME_SEPARATION_TOKEN = "_"
""" The name separation token """

FILE_EXTENSION_VALUE = ".deb"
""" The file extension value """

class RepositoryGeneratorApt:
    """
    The repository generator apt class.
    """

    repository_generator_apt_plugin = None
    """ The repository generator apt plugin """

    def __init__(self, repository_generator_apt_plugin):
        """
        Constructor of the class.

        @type repository_generator_apt_plugin: RepositoryGeneratorAptPlugin
        @param repository_generator_apt_plugin: The repository generator apt plugin.
        """

        self.repository_generator_apt_plugin = repository_generator_apt_plugin

    def get_adapter_name(self):
        """
        Retrieves the adapter name.

        @rtype: String
        @return: The adapter name.
        """

        return ADAPTER_NAME

    def generate_repository(self, parameters):
        """
        Generates a repository for the given parameters.

        @type parameters: Dictionary
        @param parameters: The parameters for the repository generation.
        """

        # retrieves the packaging deb plugin
        packaging_deb_plugin = self.repository_generator_apt_plugin.packaging_deb_plugin

        # retrieves the source from the parameters
        source = parameters[SOURCE_VALUE]

        # retrieves the target from the parameters
        target = parameters[TARGET_VALUE]

        # in case the target path does not exist
        if not os.path.exists(target):
            # creates the target directories
            os.makedirs(target)

        # retrieves the contents from the parameters
        contents = parameters[CONTENTS_VALUE]

        # retrieves the file from the parameters
        files = contents.get(FILE_VALUE, [])

        # iterates over all the files to process them
        for file in files:
            # retrieves the file attributes
            file_name = file[NAME_VALUE]
            file_version = file.get(VERSION_VALUE, "1.0.0")
            file_architecture = file.get(ARCHITECTURE_VALUE, "all")

            complete_file_name = file_name + NAME_SEPARATION_TOKEN + file_version + NAME_SEPARATION_TOKEN + file_architecture + FILE_EXTENSION_VALUE

            complete_file_path = source + "/" + complete_file_name

            # creates the deb file parameters map
            deb_file_parameters = {"file_path" : complete_file_path,
                                   "file_format" : "tar_gz"}

            # creates the deb file
            deb_file = packaging_deb_plugin.create_file(deb_file_parameters)

            # opens the deb file
            deb_file.open("rb")

            # closes the deb file
            deb_file.close()
