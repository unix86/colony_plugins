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

__revision__ = "$LastChangedRevision: 428 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-20 18:42:55 +0000 (Qui, 20 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os.path

import main_service_http_file_handler_exceptions

HANDLER_NAME = "file"
""" The handler name """

CHUNK_FILE_SIZE_LIMIT = 3072
""" The chunk file size limit """

CHUNK_SIZE = 1024
""" The chunk size """

FILE_MIME_TYPE_MAPPING = {"html" : "text/html", "txt" : "text/plain",
                          "jpg" : "image/jpg", "png" : "image/png"}
""" The map that relates the file extension and the associated mime type """

class MainServiceHttpFileHandler:
    """
    The main service http file handler class.
    """

    main_service_http_file_handler_plugin = None
    """ The main service http file handler plugin """

    def __init__(self, main_service_http_file_handler_plugin):
        """
        Constructor of the class.

        @type main_service_http_file_handler_plugin: MainServiceHttpFileHandlerPlugin
        @param main_service_http_file_handler_plugin: The main service http file handler plugin.
        """

        self.main_service_http_file_handler_plugin = main_service_http_file_handler_plugin

    def get_handler_name(self):
        return HANDLER_NAME

    def handle_request(self, request):
        # sets the base directory
        base_directory = "C:/Program Files/Apache Software Foundation/Apache2.2/htdocs"

        # retrieves the requested path
        path = request.get_resource_path()

        if path == "/":
            path = "/index.html"

        # retrieves the extension of the file
        extension = path.split(".")[-1]

        # retrieves the associated mime type
        if extension in FILE_MIME_TYPE_MAPPING:
            mime_type = FILE_MIME_TYPE_MAPPING[extension]
        else:
            mime_type = None

        # creates the complete path
        complete_path = base_directory + "/" + path

        # in case the paths does not exist
        if not os.path.exists(complete_path):
            # raises file not found exception with 404 http error code
            raise main_service_http_file_handler_exceptions.FileNotFoundException(path, 404)

        # sets the request mime type
        request.content_type = mime_type

        # sets the request status code
        request.status_code = 200

        # opens the requested file
        file = open(complete_path, "rb")

        # retrieves the file size
        file_size = os.path.getsize(complete_path)

        if file_size > CHUNK_FILE_SIZE_LIMIT:
            # creates the chunk handler instance
            chunk_handler = ChunkHandler(file, file_size)

            # sets the request as mediated
            request.mediated = True

            # sets the mediated handler in the request
            request.mediated_handler = chunk_handler
        else:
            # reads the file contents
            file_contents = file.read()

            # closes the file
            file.close()

            # writes the file contents
            request.write(file_contents)

class ChunkHandler:
    """
    The chunk handler class.
    """

    file = None
    """ The file """

    file_size = None
    """ The file size """

    def __init__(self, file, file_size):
        """
        Constructor of the class.

        @type file: File
        @param file: The file.
        @type file_size: int
        @param file_size: The file size.
        """

        self.file = file
        self.file_size = file_size

    def get_size(self):
        """
        Retrieves the size of the file being chunked.

        @rtype: int
        @return: The size of the file being chunked.
        """

        return self.file_size

    def get_chunk(self, chunk_size = CHUNK_SIZE):
        """
        Retrieves the a chunk with the given size.

        @rtype: chunk_size
        @return: The size of the chunk to be retrieved.
        @rtype: String
        @return: A chunk with the given size.
        """

        return self.file.read(chunk_size)

    def close_file(self):
        """
        Closes the file being chunked.
        """

        # closes the file
        self.file.close()
