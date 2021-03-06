#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2012 Hive Solutions Lda.
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

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2012 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony.base.system

class FileGridfsPlugin(colony.base.system.Plugin):
    """
    The main class for the File Gridfs plugin.
    """

    id = "pt.hive.colony.plugins.data.file.gridfs"
    name = "File Gridfs"
    description = "File Gridfs Plugin"
    version = "1.0.0"
    author = "Hive Solutions Lda. <development@hive.pt>"
    platforms = [
        colony.base.system.CPYTHON_ENVIRONMENT
    ]
    capabilities = [
        "threads",
        "file_engine"
    ]
    dependencies = [
        colony.base.system.PackageDependency("MongoDB python bindings", "pymongo", "1.6.x", "http://mongodb.org"),
        colony.base.system.PackageDependency("MongoDB GridFS python bindings", "gridfs", "1.6.x", "http://mongodb.org")
    ]
    main_modules = [
        "data.file_gridfs.system"
    ]

    file_gridfs = None
    """ The file gridfs """

    def load_plugin(self):
        colony.base.system.Plugin.load_plugin(self)
        import data.file_gridfs.system
        self.file_gridfs = data.file_gridfs.system.FileGridfs(self)

    def get_engine_name(self):
        return self.file_gridfs.get_engine_name()

    def get_internal_version(self):
        return self.file_gridfs.get_internal_version()

    def create_connection(self, connection_parameters):
        return self.file_gridfs.create_connection(connection_parameters)

    def close_connection(self, connection):
        return self.file_gridfs.close_connection(connection)

    def get(self, connection, file_name):
        return self.file_gridfs.get(connection, file_name)

    def put(self, connection, file_path, file_name):
        return self.file_gridfs.put(connection, file_path, file_name)

    def put_file(self, connection, file, file_name):
        return self.file_gridfs.put_file(connection, file, file_name)

    def put_data(self, connection, data, file_name):
        return self.file_gridfs.put_data(connection, data, file_name)

    def delete(self, connection, file_name):
        return self.file_gridfs.delete(connection, file_name)

    def list(self, connection, directory_name):
        return self.file_gridfs.list(connection, directory_name)
