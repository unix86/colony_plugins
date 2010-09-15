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

import os
import re
import stat
import hashlib

import colony.libs.string_buffer_util

import main_service_http_file_handler_exceptions

HANDLER_NAME = "file"
""" The handler name """

CHUNK_FILE_SIZE_LIMIT = 3072
""" The chunk file size limit """

CHUNK_SIZE = 1024
""" The chunk size """

EXPIRATION_DELTA_TIMESTAMP = 31536000
""" The expiration delta timestamp """

FILE_MIME_TYPE_MAPPING = {"html" : "text/html", "txt" : "text/plain", "js" : "text/javascript",
                          "css" : "text/css", "jpg" : "image/jpg", "png" : "image/png"}
""" The map that relates the file extension and the associated mime type """

INVALID_EXPIRATION_STRING_VALUE = "-1"
""" The invalid expiration string value """

RELATIVE_PATHS_REGEX_VALUE = "^\.\.|\/\.\.\/|\\\.\.\\|\.\.$"
""" The relative paths regex value """

RELATIVE_PATHS_REGEX = re.compile(RELATIVE_PATHS_REGEX_VALUE)
""" The relative paths regex """

ACCEPT_RANGES_VALUE = "Accept-Ranges"
""" The accept ranges value """

CONTENT_RANGE_VALUE = "Content-Range"
""" The content range value """

RANGE_VALUE = "Range"
""" The range value """

BYTES_VALUE = "bytes"
""" The bytes value """

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
        """
        Retrieves the handler name.

        @rtype: String
        @return: The handler name.
        """

        return HANDLER_NAME

    def handle_request(self, request):
        """
        Handles the given http request.

        @type request: HttpRequest
        @param request: The http request to be handled.
        """

        # retrieves the resource manager plugin
        resource_manager_plugin = self.main_service_http_file_handler_plugin.resource_manager_plugin

        # retrieves the handler configuration
        handler_configuration = self.main_service_http_file_handler_plugin.get_configuration_property("handler_configuration").get_data()

        # retrieves the handler configuration property
        handler_configuration_property = self.main_service_http_file_handler_plugin.get_configuration_property("handler_configuration")

        # in case the handler configuration property is defined
        if handler_configuration_property:
            # retrieves the handler configuration
            handler_configuration = handler_configuration_property.get_data()
        else:
            # sets the handler configuration as an empty map
            handler_configuration = {}

        # retrieves the default path
        default_path = handler_configuration.get("default_path", "/")

        # retrieves the default page
        default_page = handler_configuration.get("default_page", "index.html")

        # retrieves the default relative paths
        relative_paths = handler_configuration.get("relative_paths", False)

        # sets the base directory for file search
        base_directory = request.properties.get("base_path", default_path)

        # sets the default page
        default_page = request.properties.get("default_page", default_page)

        # retrieves the relative paths
        relative_paths = request.properties.get("relative_paths", relative_paths)

        # retrieves the requested resource path
        resource_path = request.get_resource_path()

        # retrieves the handler path
        handler_path = request.get_handler_path()

        # retrieves the real base directory
        real_base_directory = resource_manager_plugin.get_real_string_value(base_directory)

        # in case the relative paths are disabled
        if not relative_paths:
            # escapes the resource path in the relatives paths
            resource_path = self._escape_relative_paths(resource_path)

        # in case there is a valid handler path
        if handler_path:
            path = resource_path.replace(handler_path, "", 1)
        else:
            path = resource_path

        # in case the path is the base one
        if path == "/" or path == "":
            path = "/" + default_page

        # retrieves the extension of the file
        extension = path.split(".")[-1]

        # retrieves the associated mime type
        if extension in FILE_MIME_TYPE_MAPPING:
            mime_type = FILE_MIME_TYPE_MAPPING[extension]
        else:
            mime_type = None

        # creates the complete path
        complete_path = real_base_directory + "/" + path

        # in case the paths does not exist
        if not os.path.exists(complete_path):
            # raises file not found exception with 404 http error code
            raise main_service_http_file_handler_exceptions.FileNotFoundException(resource_path, 404)

        # retrieves the file stat
        file_stat = os.stat(complete_path)

        # retrieves the modified timestamp
        modified_timestamp = file_stat[stat.ST_MTIME]

        # computes the etag value base in the file stat and
        # modified timestamp
        etag_value = self._compute_etag(file_stat, modified_timestamp)

        # verifies the resource to validate any modification
        if not request.verify_resource_modification(modified_timestamp, etag_value):
            # sets the request mime type
            request.content_type = mime_type

            # sets the request status code
            request.status_code = 304

            # returns immediately
            return

        # calculates the expiration timestamp from the modified timestamp
        # incrementing the delta timestamp for expiration
        expiration_timestamp = modified_timestamp + EXPIRATION_DELTA_TIMESTAMP

        # sets the request mime type
        request.content_type = mime_type

        # sets the request status code
        request.status_code = 200

        # sets the last modified timestamp
        request.set_last_modified_timestamp(modified_timestamp)

        # sets the expiration timestamp in the request
        request.set_expiration_timestamp(expiration_timestamp)

        # sets the etag in the request
        request.set_etag(etag_value)

        # in case the complete path is a directory
        if os.path.isdir(complete_path):
            # processes the path as a directory
            self._process_directory(request, complete_path)
        # otherwise
        else:
            # processes the path as a file
            self._process_file(request, complete_path)

    def _process_directory(self, request, complete_path):
        """
        Processes a directory request for the given complete
        path and request.

        @type request: HttpRequest
        @param request: The http request to be handled.
        @type complete_path: String
        @param complete_path: The complete path to the directory.
        """

        # retrieves the directory names for the complete path
        directory_names = os.listdir(complete_path)

        # iterates over all the directory names
        for directory_name in directory_names:
            request.write("<div><a href=\"" + directory_name + "\">", 0, True)

            # writes the file contents
            request.write(directory_name, 0, True)

            request.write("</a></div>", 0, True)

    def _process_file(self, request, complete_path):
        """
        Processes a file request for the given complete
        path and request.

        @type request: HttpRequest
        @param request: The http request to be handled.
        @type complete_path: String
        @param complete_path: The complete path to the file.
        """

        # opens the requested file
        file = open(complete_path, "rb")

        # retrieves the file size
        file_size = os.path.getsize(complete_path)

        # processes and retrieves the ranges to be used
        ranges = self._process_ranges(request, file_size)

        # in case the file size is bigger than
        # the chunk file size limit
        if file_size > CHUNK_FILE_SIZE_LIMIT:
            # creates the chunk handler instance
            chunk_handler = ChunkHandler(file, file_size, ranges)

            # processes the ranges value in the chunk handler
            chunk_handler.process_ranges()

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
            request.write(file_contents, 1, False)

    def _process_ranges(self, request, file_size):
        """
        Processes the ranges for the given request,
        using the given file size.

        @type request: HttpRequest
        @param request: The http request to used in the processing.
        @type file_size: int
        @param file_size: The size of the file to be used.
        """

        # sets the accept ranges header
        request.set_header(ACCEPT_RANGES_VALUE, BYTES_VALUE)

        # retrieves the range header
        range_header = request.get_header(RANGE_VALUE)

        # in case there is no range header
        if not range_header:
            # returns immediately
            return None

        # splits the range header retrieving the key
        # and the values
        key, values = range_header.split("=")

        # in case the key is not bytes
        if not key == BYTES_VALUE:
            # return immediately
            return None

        # splits the values retrieving the range values
        range_values = values.split(",")

        # creates the list of ranges in number mode
        ranges_number_list = []

        # iterates over all the range values
        for range_value in range_values:
            # splits the range retrieving the initial value
            # and the end value
            initial_value, end_value = range_value.split("-")

            # converts both the initial and the end values to number
            initial_value_number = initial_value and int(initial_value) or - 1
            end_value_number = end_value and int(end_value) or - 1

            # creates the range number tuple with both the initial and end values
            range_number_tuple = (initial_value_number, end_value_number)

            # adds the range number tuple to the ranges number list
            ranges_number_list.append(range_number_tuple)

        # retrieves the length of the ranges number list
        ranges_number_list_length = len(ranges_number_list)

        # in case the length of the ranges number list
        # is bigger than one, the feature is not implemented
        if ranges_number_list_length > 1:
            # raises the not implemented exception
            raise main_service_http_file_handler_exceptions.NotImplementedException("no support for multiple ranges", 501)

        # retrieves the first range value
        first_range_value = ranges_number_list[0]

        # converts the first range value to string
        first_range_string_value = self._range_to_string(first_range_value, file_size)

        # sets the content range header value
        request.set_header(CONTENT_RANGE_VALUE, first_range_string_value)

        # sets the request status code
        request.status_code = 206

        # returns the ranges number list
        return ranges_number_list

    def _compute_etag(self, file_stat, modified_timestamp):
        """
        Computes the etag for the given file stat and
        modified timestamp.

        @type file_stat: Dictionary
        @param file_stat: The file stat values dictionary.
        @type modified_timestamp: int
        @param modified_timestamp: The last modified timestamp.
        @rtype: String
        @return: The etag value.
        """

        # retrieves the md5 builder
        md5 = hashlib.md5()

        # retrieves the size
        size = file_stat[stat.ST_SIZE]

        # creates the modification plus size string
        modification_size_string = str(modified_timestamp + size)

        # updates the md5 hash with the modification
        # plus size string
        md5.update(modification_size_string)

        # retrieves the md5 hex digest as the etag value
        etag_value = md5.hexdigest()

        # returns the etag value
        return etag_value

    def _escape_relative_paths(self, path):
        """
        Escapes the relative path values in the given path.

        @type path: String
        @param path: The path to be escaped.
        @rtype: String
        @return: The escaped path.
        """

        # escapes the paths in the relative paths value
        escaped_path = RELATIVE_PATHS_REGEX.sub("", path)

        # returns the escaped path
        return escaped_path

    def _range_to_string(self, range_value, file_size):
        """
        Converts the given range value to a string value,
        using the given file size as reference.

        @type range_value: Tuple
        @param range_value: The range value to be converted to string.
        @type file_size: int
        @param file_size: The size of the file to be used as reference.
        @rtype: String
        @return: The string value for the range.
        """

        # creates a string buffer to hold the range
        range_string_buffer = colony.libs.string_buffer_util.StringBuffer()

        # retrieves the range initial and end values
        initial_value, end_value = range_value

        # writes the initial part
        range_string_buffer.write(BYTES_VALUE)
        range_string_buffer.write(" ")

        # converts both the initial and end values to string
        initial_value_string = initial_value == -1 and "0" or str(initial_value)
        end_value_string = end_value == -1 and str(file_size - 1) or str(end_value)

        # writes the initial and end values to the range string buffer
        range_string_buffer.write(initial_value_string)
        range_string_buffer.write("-")
        range_string_buffer.write(end_value_string)

        # writes the final file size part in the
        # the range string buffer
        range_string_buffer.write("/")
        range_string_buffer.write(str(file_size))

        # retrieves the range string value
        range_string_value = range_string_buffer.get_value()

        # returns the range string value
        return range_string_value

class ChunkHandler:
    """
    The chunk handler class.
    """

    file = None
    """ The file """

    file_size = None
    """ The file size """

    ranges = None
    """ The list of ranges """

    def __init__(self, file, file_size, ranges):
        """
        Constructor of the class.

        @type file: File
        @param file: The file.
        @type file_size: int
        @param file_size: The file size.
        @type ranges: List
        @param ranges: The list of ranges.
        """

        self.file = file
        self.file_size = file_size
        self.ranges = ranges

    def process_ranges(self):
        """
        Processes the ranges of the file request.
        """

        # in case no ranges are defined
        if not self.ranges:
            # returns immediately
            return

        # retrieves the first range
        first_range = self.ranges[0]

        # retrieves both the initial and end value
        # from the first range
        initial_value, _end_value = first_range

        # in case the initial value is valid
        if not initial_value == -1:
            # seeks the file into the initial value
            self.file.seek(initial_value)

    def encode_file(self, encoding_handler, encoding_name):
        """
        Encodes the file using the given encoding handler with the given name.

        @type encoding_handler: Method
        @param encoding_handler: The encoding handler method to be used.
        @type encoding_name: String
        @param encoding_name: The name of the encoding to be used.
        """

        # reads the file contents
        file_contents = self.file.read()

        # encodes the file contents using the given encoding handler
        file_contents_encoded = encoding_handler(file_contents)

        # creates a new string buffer to used as a memory file
        # for the encoded file
        file_contents_encoded_file_buffer = colony.libs.string_buffer_util.StringBuffer(False)

        # writes the file contents encoded into the file contents
        # file buffer
        file_contents_encoded_file_buffer.write(file_contents_encoded)

        # sets the new file
        self.file = file_contents_encoded_file_buffer

        # sets the new file size
        self.file_size = file_contents_encoded_file_buffer.tell()

        # seeks to the beginning of the file
        file_contents_encoded_file_buffer.seek(0)

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
