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

__revision__ = "$LastChangedRevision: 421 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-20 15:16:53 +0000 (Qui, 20 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import re

import web_mvc_utils_exceptions

DEFAULT_CONTENT_TYPE = "text/html;charset=utf-8"
""" The default content type """

DEFAULT_ENCODING = "utf-8"
""" The default encoding value """

BASE_PATH_VALUE = "base_path"
""" The base path value """

BACK_PATH_VALUE = "../"
""" The back path value """

NAME_TYPE_VALUE = "name"
""" The name type value """

SEQUENCE_TYPE_VALUE = "sequence"
""" The sequence type value """

MAP_TYPE_VALUE = "map"
""" The map type value """

ATTRIBUTE_PARSING_REGEX_VALUE = r"(?P<name>\w+)|(?P<sequence>\[\])|(?P<map>\[\w+\])"
""" The attribute parsing regular expression value """

ATTRIBUTE_PARSING_REGEX = re.compile(ATTRIBUTE_PARSING_REGEX_VALUE)
""" The attribute parsing regex """

def _start_controller(self):
    """
    Starts the controller structures.
    """

    # in case the controller has the start method
    if hasattr(self, "start"):
        # calls the start method
        # in the controller
        self.start()

def process_form_data(self, rest_request, encoding = DEFAULT_ENCODING):
    # retrieves the attributes list
    attributes_list = rest_request.get_attributes_list()

    # creates the base attributes map
    base_attributes_map = {}

    # iterates over all the attributes in the
    # attributes list
    for attribute in attributes_list:
        # retrieves the attribute value from the request
        attribute_value = self.get_attribute_decoded(rest_request, attribute, encoding)

        # start the processing of the form attribute with the base attributes map
        # the base attribute name and the attribute value
        self._process_form_attribute(base_attributes_map, attribute, attribute_value)

    # returns the base attributes map
    return base_attributes_map

def _process_form_attribute(self, parent_structure, current_attribute_name, attribute_value):
    # retrieves the current match result
    match_result = ATTRIBUTE_PARSING_REGEX.match(current_attribute_name)

    # in case there is no match result
    if not match_result:
        # raises the invalid attribute name exception
        raise web_mvc_utils_exceptions.InvalidAttributeName("invalid match value: " + current_attribute_name)

    # retrieves the match result end position
    match_result_end = match_result.end()

    # checks if it's the last attribute name
    is_last_attribute_name = match_result_end == len(current_attribute_name)

    # retrieves the match result value
    match_result_value = match_result.group()

    # in case the match result value is of type map
    # the parentheses need to be removed
    if match_result.lastgroup == MAP_TYPE_VALUE:
        # retrieves the match result value without the parentheses
        match_result_value = match_result_value[1:-1]

    # in case it's the only (last) match available
    if is_last_attribute_name:
        if match_result.lastgroup == NAME_TYPE_VALUE:
            parent_structure[match_result_value] = attribute_value
        elif match_result.lastgroup == SEQUENCE_TYPE_VALUE:
            parent_structure.append(attribute_value)
        elif match_result.lastgroup == MAP_TYPE_VALUE:
            parent_structure[match_result_value] = attribute_value

    # there is more parsing to be made
    else:
        # retrieves the next match value in order to make
        next_match_result = ATTRIBUTE_PARSING_REGEX.match(current_attribute_name, match_result_end)

        # in case there is no next match result
        if not next_match_result:
            # raises the invalid attribute name exception
            raise web_mvc_utils_exceptions.InvalidAttributeName("invalid next match value: " + current_attribute_name)

        # retrieves the next match result value
        next_match_result_value = next_match_result.group()

        if next_match_result.lastgroup == MAP_TYPE_VALUE:
            # retrieves the next match result value without the parentheses
            next_match_result_value = next_match_result_value[1:-1]

        # in case the next match is of type name
        if next_match_result.lastgroup == NAME_TYPE_VALUE:
            # raises the invalid attribute name exception
            raise web_mvc_utils_exceptions.InvalidAttributeName("invalid next match value (is a name): " + current_attribute_name)
        elif next_match_result.lastgroup == SEQUENCE_TYPE_VALUE:
            current_attribute_value = []
        elif next_match_result.lastgroup == MAP_TYPE_VALUE:
            if match_result.lastgroup == SEQUENCE_TYPE_VALUE:
                if next_match_result_value in parent_structure[-1]:
                    current_attribute_value = {}
                else:
                    current_attribute_value = parent_structure[-1]
            elif match_result_value in parent_structure:
                current_attribute_value = parent_structure[match_result_value]
            else:
                current_attribute_value = {}

        if match_result.lastgroup == NAME_TYPE_VALUE:
            parent_structure[match_result_value] = current_attribute_value
        elif match_result.lastgroup == SEQUENCE_TYPE_VALUE:
            parent_structure.append(current_attribute_value)
        elif match_result.lastgroup == MAP_TYPE_VALUE:
            parent_structure[match_result_value] = current_attribute_value

        # retrieves the remaining attribute name
        remaining_attribute_name = current_attribute_name[match_result_end:]

        # processes the next form attribute with the current attribute value as the new parent structure
        # the remaining attribute name as the new current attribute name and the attribute value
        # continues with the same value
        self._process_form_attribute(current_attribute_value, remaining_attribute_name, attribute_value)

def get_base_path(self, rest_request):
    """
    Retrieves the base path according to
    the current rest request path.

    @type rest_request: RestRequest
    @param rest_request: The rest request to be used to retrieve
    the base path.
    @rtype: String
    @return: The base path.
    """

    # retrieves the path list length
    path_list_length = len(rest_request.path_list)

    # creates the base path
    base_path = str()

    # iterates over all the path list length without
    # the delta value
    for _index in range(path_list_length - 2):
        # adds the back path to the base path
        base_path += BACK_PATH_VALUE

    # returns the base path
    return base_path

def set_contents(self, rest_request, contents = ""):
    # sets the content type for the rest request
    rest_request.set_content_type(DEFAULT_CONTENT_TYPE)

    # sets the result for the rest request
    rest_request.set_result_translated(contents)

    # flushes the rest request
    rest_request.flush()

def retrieve_template_file(self, file_name = None):
    # creates the template file path
    template_file_path = self.templates_path + "/" + file_name

    # parses the template file path
    template_file = self.template_engine_manager_plugin.parse_file_path_encoding(template_file_path, "Cp1252")

    # returns the template file
    return template_file

def apply_base_path_template_file(self, rest_request, template_file):
    """
    Applies the base path to the template file according to
    the current rest request path.

    @type rest_request: RestRequest
    @param rest_request: The rest request to be used to set the base path.
    @type template_file: TemplateFile
    @param template_file: The template to be "applied" with the base path.
    """

    # retrieves the base path
    base_path = self.get_base_path(rest_request);

    # assigns the area value
    template_file.assign(BASE_PATH_VALUE, base_path)

def get_session_attribute(self, rest_request, session_attribute_name):
    # tries to retrieve the rest request session
    rest_request_session = rest_request.get_session()

    # in case the rest request session
    # is invalid
    if not rest_request_session:
        # returns none (invalid)
        return None

    # retrieves the attribute from the session
    session_attribute = rest_request_session.get_attribute(session_attribute_name)

    # returns the session attribute
    return session_attribute

def set_session_attribute(self, rest_request, session_attribute_name, session_attribute_value):
    # tries to retrieve the rest request session
    rest_request_session = rest_request.get_session()

    # in case the rest request session
    # is invalid
    if not rest_request_session:
        # start a session if none is started
        rest_request.start_session()

        # retrieves the rest request session
        rest_request_session = rest_request.get_session()

    # sets the attribute in the session
    rest_request_session.set_attribute(session_attribute_name, session_attribute_value)

def unset_session_attribute(self, rest_request, session_attribute_name):
    # tries to retrieve the rest request session
    rest_request_session = rest_request.get_session()

    # in case the rest request session
    # is invalid
    if not rest_request_session:
        # returns none (invalid)
        return None

    # unsets the attribute from the session
    rest_request_session.unset_attribute(session_attribute_name)

def get_attribute_decoded(self, rest_request, attribute_name, encoding = DEFAULT_ENCODING):
    # retrieves the attribute value from the attribute name
    attribute_value = rest_request.get_attribute(attribute_name)

    # in case the attribute value is valid
    if attribute_value:
        # unquotes the attribute value
        attribute_value_unquoted = rest_request.request.unquote_plus(attribute_value)

        # decodes the attribute value
        attribute_value_decoded = attribute_value_unquoted.decode(encoding)

        # the attribute value decoded
        return attribute_value_decoded
    else:
        # returns the empty value
        return ""

def get_templates_path(self):
    """
    Retrieves the templates path.

    @rtype: Sring
    @return: The templates path.
    """

    return self.templates_path

def set_templates_path(self, templates_path):
    """
    Sets the templates path.

    @type templates_path: String
    @param templates_path: The templates path.
    """

    self.templates_path = templates_path

def get_template_engine_manager_plugin(self):
    """
    Retrieves the template engine manager plugin.

    @rtype: Plugin
    @return: The template engine manager plugin.
    """

    return self.template_engine_manager_plugin

def set_template_engine_manager_plugin(self, template_engine_manager_plugin):
    """
    Sets the template engine manager plugin.

    @type template_engine_manager_plugin: String
    @param template_engine_manager_plugin: The templates path.
    """

    self.template_engine_manager_plugin = template_engine_manager_plugin
