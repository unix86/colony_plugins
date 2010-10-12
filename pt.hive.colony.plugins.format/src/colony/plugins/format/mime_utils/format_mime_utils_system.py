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

CONTENT_TYPE_VALUE = "Content-Type"
""" The content type value """

CONTENT_TRANSFER_ENCODING_VALUE = "Content-Transfer-Encoding"
""" The content transfer encoding value """

CONTENT_ID_VALUE = "Content-ID"
""" The content id value """

BASE64_VALUE = "base64"
""" The base64 value """

class FormatMimeUtils:
    """
    The format mime utils class.
    """

    format_mime_utils_plugin = None
    """ The format mime utils plugin """

    def __init__(self, format_mime_utils_plugin):
        """
        Constructor of the class.

        @type format_mime_utils_plugin: FormatMimeUtilsPlugin
        @param format_mime_utils_plugin: The format mime utils plugin.
        """

        self.format_mime_utils_plugin = format_mime_utils_plugin

    def add_mime_message_contents(self, mime_message, contents_path, content_extensions):
        # lists the directory, retrieving the directory entries
        directory_entries = os.listdir(contents_path)

        # iterates over all the directory entries
        for directory_entry in directory_entries:
            # creates the content path appending the directory entry (name)
            # to the (base) contents path
            content_path = os.path.join(contents_path, directory_entry)

            # retrieves the content extension from the content path
            content_extension = os.path.splitext(content_path)[1].lstrip(".")

            # in case the content path refers a directory
            if os.path.isdir(content_path):
                # adds the directory contents
                self.add_mime_message_contents(mime_message, content_path, content_extensions)
            elif content_extension in content_extensions:
                # adds the content to the mime message
                self._add_mime_message_content(mime_message, content_path)

    def _add_mime_message_content(self, mime_message, content_path):
        # retrieves the format mime plugin
        format_mime_plugin = self.format_mime_utils_plugin.format_mime_plugin

        # creates the mime message part for the content
        mime_message_content_part = format_mime_plugin.create_message_part({})

        # opens the content file
        content_file = open(content_path, "rb")

        try:
            # reads the content file contents
            content_file_contents = content_file.read()

            # writes the content file contents in base 64 to
            # the mime message content part
            mime_message_content_part.write_base_64(content_file_contents)

            # retrieves the content rtype for the file name
            content_type = format_mime_plugin.get_mime_type_file_name(content_path)

            # retrieves the base name from the content path
            base_name = os.path.basename(content_path)

            # creates the content id from the base name
            content_id = "<" + base_name + ">"

            print content_type
            print content_id

            # sets the mime message content part headers
            mime_message_content_part.set_header(CONTENT_TYPE_VALUE, content_type)
            mime_message_content_part.set_header(CONTENT_TRANSFER_ENCODING_VALUE, BASE64_VALUE)
            mime_message_content_part.set_header(CONTENT_ID_VALUE, content_id)

            # adds the mime message content part to the mime message
            mime_message.add_part(mime_message_content_part)
        finally:
            # closes the content file
            content_file.close()
