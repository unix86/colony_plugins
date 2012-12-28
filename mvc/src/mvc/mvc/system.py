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

import re
import types

import colony.base.system
import colony.libs.map_util
import colony.libs.string_buffer_util

import exceptions
import file_handler
import communication

NAMED_GROUPS_REGEX_VALUE = "\(\?\P\<[a-zA-Z_][a-zA-Z0-9_]*\>(.+?)\)"
""" The named groups regex value """

NAMED_GROUPS_REGEX = re.compile(NAMED_GROUPS_REGEX_VALUE)
""" The named groups regex """

REGEX_COMPILATION_LIMIT = 99
""" The regex compilation limit """

GET_DEFAULT_PARAMETERS_VALUE = "get_default_parameters"
""" The get default parameters value """

DEFAULT_STATUS_CODE = 200
""" The default status code """

class Mvc(colony.base.system.System):
    """
    The mvc class.
    """

    mvc_file_handler = None
    """ The mvc file handler """

    mvc_communication_handler = None
    """ The mvc communication handler """

    clear_pending = False
    """ Flag that controls if the rest sessions should be
    cleared at the next tick of handling """

    matching_regex_list = []
    """ The list of matching regex to be used in
    patterns matching """

    matching_regex_base_values_map = {}
    """ The map containing the base values for the
    various matching regex """

    communication_matching_regex_list = []
    """ The list of matching regex to be used in
    communication patterns matching """

    communication_matching_regex_base_values_map = {}
    """ The map containing the base values for the
    various communication matching regex """

    resource_matching_regex_list = []
    """ The list of matching regex to be used in
    resource patterns matching """

    resource_matching_regex_base_values_map = {}
    """ The map containing the base values for the
    various resource matching regex """

    mvc_service_patterns_map = {}
    """ The mvc service patterns map """

    mvc_service_pattern_escaped_map = {}
    """ The mvc service pattern escaped map """

    mvc_service_pattern_compiled_map = {}
    """ The mvc service pattern compiled map """

    mvc_service_patterns_list = []
    """ The mvc service patterns list for indexing """

    mvc_service_communication_patterns_map = {}
    """ The mvc service communication patterns map """

    mvc_service_communication_patterns_list = []
    """ The mvc service communication patterns list
    for indexing """

    mvc_service_resource_patterns_map = {}
    """ The mvc service resource patterns map """

    mvc_service_resource_patterns_list = []
    """ The mvc service resource patterns list for
    indexing """

    def __init__(self, plugin):
        colony.base.system.System.__init__(self, plugin)

        self.matching_regex_list = []
        self.matching_regex_base_values_map = {}
        self.communication_matching_regex_list = []
        self.communication_matching_regex_base_values_map = {}
        self.resource_matching_regex_list = []
        self.resource_matching_regex_base_values_map = {}
        self.mvc_service_patterns_map = {}
        self.mvc_service_pattern_escaped_map = {}
        self.mvc_service_pattern_compiled_map = {}
        self.mvc_service_patterns_list = []
        self.mvc_service_communication_patterns_map = {}
        self.mvc_service_communication_patterns_list = []
        self.mvc_service_resource_patterns_map = {}
        self.mvc_service_resource_patterns_list = []

        self.mvc_file_handler = file_handler.MvcFileHandler(plugin)
        self.mvc_communication_handler = communication.MvcCommunicationHandler(plugin)

    def start_system(self):
        """
        Starts the mvc system structures.
        This method starts all the persistent and
        background execution tasks for mvc.

        Note that the execution og background tasks
        is conditioned to the current thread execution
        policy and permissions from the manager.
        """

        # retrieves the plugin manager reference and uses it to check
        # if the communication handler processing system should be
        # started, because if threads are not allowed no process should
        # be started (violates manger rules)
        plugin_manager = self.plugin.manager
        if plugin_manager.allow_threads: self.mvc_communication_handler.start_processing()

    def stop_system(self):
        """
        Stops the mvc system structures.
        This method stops all the persistent and
        background execution tasks for mvc.
        """

        # retrieves the plugin manager to recall the option to load or not
        # the communication handler in case the handler has been started it
        # must now be stopped to avoid any memory or other resource leak
        plugin_manager = self.plugin.manager
        if plugin_manager.allow_threads: self.mvc_communication_handler.stop_processing()

    def get_routes(self):
        """
        Retrieves the list of regular expressions to be used as route,
        to the rest service.

        @rtype: List
        @return: The list of regular expressions to be used as route,
        to the rest service.
        """

        return [
            r"^mvc/.*$"
        ]

    def handle_rest_request(self, rest_request):
        """
        Handles the given rest request, the method starts by
        trying to match any of the regular expression in the
        various areas, in case it matches handles it accordingly
        and processes the request (post request execution).

        The execution follows a order of resources, communication
        and at last normal (dynamic) handling.

        @type rest_request: RestRequest
        @param rest_request: The rest request to be handled.
        @rtype: bool
        @return: The result of the handling.
        """

        # in case the clear pending flag is set must remove
        # (clear) all the current sessions from the rest manager
        # this is a global reset (side problems may occur)
        if self.clear_pending: rest_request.clear_sessions(); self.clear_pending = False

        # retrieves the path list, then joins the path list
        # to create the resource path
        path_list = rest_request.get_path_list()
        resource_path = "/".join(path_list)

        # iterates over all the resource matching regex in the
        # resource matching regex list to try to match any of
        # them and execute the proper action if such occurs
        for resource_matching_regex in self.resource_matching_regex_list:
            # tries to math the resource path in case there is no
            # valid resource path match must continue the loop
            resource_path_match = resource_matching_regex.match(resource_path)
            if not resource_path_match: continue

            # handles the match using the resource handler, this should update the
            # response object with the proper contents, then runs the post handling
            # request processor so that the request object remains in the expected state
            self._handle_resource_match(
                rest_request,
                resource_path,
                resource_path_match,
                resource_matching_regex
            )
            self._process_request(rest_request)

            # returns immediately, no more matching tries should
            # occur (already matched)
            return

        # iterates over all the communication matching regex in the
        # communication matching regex list to try to match any of
        # them and execute the proper action if such occurs
        for communication_matching_regex in self.communication_matching_regex_list:
            # tries to math the communication path in case there is no
            # valid communication path match must continue the loop
            communication_path_match = communication_matching_regex.match(resource_path)
            if not communication_path_match: continue

            # handles the match using the communication handler, this should update the
            # response object with the proper contents, then runs the post handling
            # request processor so that the request object remains in the expected state
            self._handle_communication_match(
                rest_request,
                resource_path,
                communication_path_match,
                communication_matching_regex
            )
            self._process_request(rest_request)

            # returns immediately
            return

        # iterates over all the (dynamic) matching regex in the
        # (dynamic) matching regex list to try to match any of
        # them and execute the proper action if such occurs
        for matching_regex in self.matching_regex_list:
            # tries to math the resource path in case there is
            # no valid resource path match must continue the loop
            resource_path_match = matching_regex.match(resource_path)
            if not resource_path_match: continue

            # validate the match and retrieves the handle tuple and in
            # case the handle tuple is invalid continues immediately
            # because it's not possible to process the request
            handle_tuple = self._validate_match(rest_request, resource_path, resource_path_match, matching_regex)
            if not handle_tuple: continue

            # handles the match using the (dynamic) handler, this should update the
            # response object with the proper contents, then runs the post handling
            # request processor so that the request object remains in the expected state
            self._handle_match(rest_request, handle_tuple)
            self._process_request(rest_request)

            # returns immediately
            return

        # raises the mvc request not handled exception, because no mvc
        # service was found for the current request constraints
        raise exceptions.MvcRequestNotHandled("no mvc service plugin could handle the request")

    def load_mvc_service_plugin(self, mvc_service_plugin):
        """
        Loads the given mvc service plugin.

        @type mvc_service_plugin: Plugin
        @param mvc_service_plugin: The mvc service plugin to be loaded.
        """

        # retrieves the mvc service plugin patterns
        mvc_service_plugin_patterns = mvc_service_plugin.get_patterns()

        # iterates over all the patterns in the mvc service plugin patterns
        for mvc_service_plugin_pattern in mvc_service_plugin_patterns:
            # retrieves the pattern key
            pattern_key = mvc_service_plugin_pattern[0]

            # retrieves the pattern value
            pattern_value = mvc_service_plugin_pattern[1:]

            # tries to retrieve the pattern validation regex from the mvc
            # service pattern compiled map
            pattern_validation_regex = self.mvc_service_pattern_compiled_map.get(pattern_key, None)

            # compiles (in case it's necessary) the pattern key, retrieving the
            # pattern validation regex (original regex)
            pattern_validation_regex = pattern_validation_regex or re.compile(pattern_key)

            # creates the pattern attributes (tuple)
            pattern_attributes = (
                pattern_validation_regex,
                pattern_value
            )

            # escapes the pattern key replacing the named
            # group selectors
            pattern_key_escaped = NAMED_GROUPS_REGEX.sub("\g<1>", pattern_key)

            # in case the pattern key escaped does not exists
            # in the mvc service patterns map
            if not pattern_key_escaped in self.mvc_service_patterns_map:
                # creates a new (pattern attributes) list for the pattern key in the
                # mvc service patterns map
                self.mvc_service_patterns_map[pattern_key_escaped] = []

                # adds the pattern to the mvc service patterns list
                self.mvc_service_patterns_list.append(pattern_key_escaped)

            # retrieves the pattern attributes list from the mvc service patterns map
            pattern_attributes_list = self.mvc_service_patterns_map[pattern_key_escaped]

            # removes the pattern attributes from the pattern attributes list
            pattern_attributes_list.append(pattern_attributes)

            # saves the escaped and compiled values of the pattern for latter usage
            self.mvc_service_pattern_escaped_map[pattern_key] = pattern_key_escaped
            self.mvc_service_pattern_compiled_map[pattern_key] = pattern_validation_regex

        # retrieves the mvc service plugin communication patterns
        mvc_service_plugin_communication_patterns = mvc_service_plugin.get_communication_patterns()

        # iterates over all the communication patterns in the mvc service plugin communication patterns
        for pattern_key, pattern_value in mvc_service_plugin_communication_patterns:
            # adds the pattern to the mvc service communication patterns map
            self.mvc_service_communication_patterns_map[pattern_key] = pattern_value

            # adds the pattern to the mvc service communication patterns list
            self.mvc_service_communication_patterns_list.append(pattern_key)

        # retrieves the mvc service plugin resource patterns
        mvc_service_plugin_resource_patterns = mvc_service_plugin.get_resource_patterns()

        # iterates over all the resource patterns in the mvc service plugin resource patterns
        for pattern_key, pattern_value in mvc_service_plugin_resource_patterns:
            # adds the pattern to the mvc service resource patterns map
            self.mvc_service_resource_patterns_map[pattern_key] = pattern_value

            # adds the pattern to the mvc service resource patterns list
            self.mvc_service_resource_patterns_list.append(pattern_key)

        # updates the complete set of matching regex, this should
        # be able to provide the initial version of the regex handler
        # methods association
        self._update_matching_regex()
        self._update_communication_matching_regex()
        self._update_resource_matching_regex()

    def unload_mvc_service_plugin(self, mvc_service_plugin):
        """
        Unloads the given mvc service plugin.

        @type mvc_service_plugin: Plugin
        @param mvc_service_plugin: The mvc service plugin to be unloaded.
        """

        # sets the clear (session) pending flag so that the sessions
        # are cleared for the next handling tick
        self.clear_pending = True

        # retrieves the mvc service plugin patterns
        mvc_service_plugin_patterns = mvc_service_plugin.get_patterns()

        # iterates over all the patterns in the mvc service plugin patterns
        for mvc_service_plugin_pattern in mvc_service_plugin_patterns:
            # retrieves the pattern key
            pattern_key = mvc_service_plugin_pattern[0]

            # retrieves the pattern value
            pattern_value = mvc_service_plugin_pattern[1:]

            # retrieves the pattern key escaped from the mvc service
            # pattern escaped map
            pattern_key_escaped = self.mvc_service_pattern_escaped_map[pattern_key]

            # in case the pattern key escaped exists in the mvc service patterns map
            if pattern_key_escaped in self.mvc_service_patterns_map:
                # retrieves the pattern validation regex from the mvc service
                # pattern compiled map
                pattern_validation_regex = self.mvc_service_pattern_compiled_map[pattern_key]

                # creates the pattern attributes (tuple)
                pattern_attributes = (
                    pattern_validation_regex,
                    pattern_value
                )

                # retrieves the pattern attributes list from the mvc service
                # patterns map
                pattern_attributes_list = self.mvc_service_patterns_map[pattern_key_escaped]

                # removes the pattern attributes from the pattern attributes list
                pattern_attributes_list.remove(pattern_attributes)

                # in case the pattern attributes list is not empty, there are
                # more patterns associated with the pattern key, no need
                # to remove the patter key references, continues the loop
                if pattern_attributes_list: continue

                # removes the pattern attributes list from the mvc service patterns map
                del self.mvc_service_patterns_map[pattern_key_escaped]

                # removes the pattern from the mvc service patterns list
                self.mvc_service_patterns_list.remove(pattern_key_escaped)

        # retrieves the mvc service plugin communication patterns
        mvc_service_plugin_communication_patterns = mvc_service_plugin.get_communication_patterns()

        # iterates over all the communication patterns in the mvc service plugin communication patterns
        for pattern_key, _pattern_value in mvc_service_plugin_communication_patterns:
            # in case the pattern key exists in the mvc service communication patterns map
            if pattern_key in self.mvc_service_communication_patterns_map:
                # removes the pattern from the mvc service communication patterns map
                del self.mvc_service_communication_patterns_map[pattern_key]

                # removes the pattern from the mvc service communication patterns list
                self.mvc_service_communication_patterns_list.remove(pattern_key)

        # retrieves the mvc service plugin resource patterns
        mvc_service_plugin_resource_patterns = mvc_service_plugin.get_resource_patterns()

        # iterates over all the resource patterns in the mvc service plugin resource patterns
        for pattern_key, _pattern_value in mvc_service_plugin_resource_patterns:
            # in case the pattern key exists in the mvc service resource patterns map
            if pattern_key in self.mvc_service_resource_patterns_map:
                # removes the pattern from the mvc service resource patterns map
                del self.mvc_service_resource_patterns_map[pattern_key]

                # removes the pattern from the mvc service resource patterns list
                self.mvc_service_resource_patterns_list.remove(pattern_key)

        # updates the matching regex
        self._update_matching_regex()

        # updates the communication matching regex
        self._update_communication_matching_regex()

        # updates the resource matching regex
        self._update_resource_matching_regex()

    def process_mvc_patterns_reload_event(self, event_name, plugin):
        # unloads the mvc service plugin
        self.unload_mvc_service_plugin(plugin)

        # loads the mvc service plugin
        self.load_mvc_service_plugin(plugin)

    def process_mvc_patterns_load_event(self, event_name, plugin):
        # loads the mvc service plugin
        self.load_mvc_service_plugin(plugin)

    def process_mvc_patterns_unload_event(self, event_name, plugin):
        # unloads the mvc service plugin
        self.unload_mvc_service_plugin(plugin)

    def process_mvc_communication_event(self, event_name, connection_name, message):
        # sends the broadcast message
        self.mvc_communication_handler.send_broadcast(connection_name, message)

    def _handle_resource_match(self, rest_request, resource_path, resource_path_match, resource_matching_regex):
        # retrieves the base value for the matching regex
        base_value = self.resource_matching_regex_base_values_map[resource_matching_regex]

        # retrieves the group index from the resource path match
        group_index = resource_path_match.lastindex

        # calculates the mvc service index from the base value,
        # the group index and subtracts one value and uses it
        # to retrieves the resource pattern
        mvc_service_index = base_value + group_index - 1
        pattern = self.mvc_service_resource_patterns_list[mvc_service_index]

        # retrieves the resource information
        resource_information = self.mvc_service_resource_patterns_map[pattern]

        # unpacks the resource information
        resource_base_path, resource_initial_token = resource_information

        # in case the resource path does not start with the resource
        # initial token  raises the invalid token value
        if not resource_path.startswith(resource_initial_token):
            raise exceptions.InvalidTokenValue("invalid initial path request")

        # retrieves the resources initial token length
        resource_initial_token_length = len(resource_initial_token)

        # creates the file path from the resource base path and file path
        file_path = resource_base_path + "/" + resource_path[resource_initial_token_length + 1:] + "." + rest_request.encoder_name

        # handles the given request by the mvc file handler
        self.mvc_file_handler.handle_request(rest_request.request, file_path)

    def _handle_communication_match(self, rest_request, resource_path, communication_path_match, communication_matching_regex):
        # retrieves the base value for the matching regex
        base_value = self.communication_matching_regex_base_values_map[communication_matching_regex]

        # retrieves the group index from the communication path match
        group_index = communication_path_match.lastindex

        # calculates the mvc service index from the base value,
        # the group index and subtracts one value and uses it to
        # retrieves the communication pattern
        mvc_service_index = base_value + group_index - 1
        pattern = self.mvc_service_communication_patterns_list[mvc_service_index]

        # retrieves the communication information
        communication_information = self.mvc_service_communication_patterns_map[pattern]

        # unpacks the communication information
        data_method, changed_method, connection_name = communication_information

        # handles the given request by the mvc communication handler
        self.mvc_communication_handler.handle_request(rest_request, data_method, changed_method, connection_name)

    def _validate_match(self, rest_request, resource_path, resource_path_match, matching_regex):
        # retrieves the base value for the matching regex
        base_value = self.matching_regex_base_values_map[matching_regex]

        # retrieves the group index from the resource path match
        group_index = resource_path_match.lastindex

        # calculates the mvc service index from the base value,
        # the group index and subtracts one value and uses it to
        # retrieve the pattern
        mvc_service_index = base_value + group_index - 1
        pattern = self.mvc_service_patterns_list[mvc_service_index]

        # retrieves the pattern attributes list from the
        # mvc service patterns map
        pattern_attributes_list = self.mvc_service_patterns_map[pattern]

        # starts the return value
        return_value = None

        # iterates over all the pattern attributes (handler attributes)
        # in the pattern attributes list
        for handler_attributes in pattern_attributes_list:
            # tries to validation the match using the rest request,
            # handler attributes and the resource path
            return_value = self.__validate_match(rest_request, handler_attributes, resource_path)

            # in case the return value is not valid
            # (no success in validation) must continue
            # the loop (keep trying)
            if not return_value: continue

            # breaks the loop (valid match)
            break

        # returns the return value
        return return_value

    def _handle_match(self, rest_request, handler_tuple):
        """
        Handles a regular expression match, redirecting the
        control flow into the appropriate registered handler method.

        This is the method that is equivalent to the general concept
        of "dispatching" for the request.

        @type rest_request: RestRequest
        @param rest_request: The rest request to be "handled".
        @type handler_tuple: Tuple
        @param handler_tuple: The tuple containing the handler method
        and the parameters to be used for handling.
        """

        # unpacks the handler tuple into the handler
        # method and the parameters
        handler_method, parameters = handler_tuple

        # retrieves the controller for the handlers method
        # and then uses it to retrieve its default parameters
        # after that uses the default parameters to extend the
        # parameters map of the handler tuple
        controller = type(handler_method) == types.MethodType and handler_method.im_self
        default_parameters = controller and hasattr(controller, GET_DEFAULT_PARAMETERS_VALUE) and controller.get_default_parameters() or {}
        colony.libs.map_util.map_extend(parameters, default_parameters, copy_base_map = False)

        # handles the mvc request to the handler method
        # (rest request flow)
        handler_method(rest_request, parameters)

    def _process_request(self, rest_request):
        """
        Processes the given rest request, changing its
        attributes to provide a valid rest request.

        @type rest_request: RestRequest
        @param rest_request: The rest request to be "processed".
        """

        # retrieves the rest request status code
        rest_request_status_code = rest_request.get_status_code()

        # checks if the status code is set in the rest request
        # and in case it's not sets the default code (no error)
        is_set_status_code = rest_request_status_code and True or False
        not is_set_status_code and rest_request.set_status_code(DEFAULT_STATUS_CODE)

    def _update_matching_regex(self):
        """
        Updates the matching regex.
        """

        # starts the matching regex value buffer
        matching_regex_value_buffer = colony.libs.string_buffer_util.StringBuffer()

        # clears the matching regex list
        self.matching_regex_list = []

        # clears the matching regex base value map
        self.matching_regex_base_values_map.clear()

        # sets the is first flag
        is_first = True

        # starts the index value
        index = 0

        # starts the current base value
        current_base_value = 0

        # iterates over all the patterns in the mvc service patterns list
        for pattern in self.mvc_service_patterns_list:
            # in case it's the first
            if is_first:
                # unsets the is first flag
                is_first = False
            else:
                # adds the or operand to the matching regex value buffer
                matching_regex_value_buffer.write("|")

            # adds the group name part of the regex to the matching regex value buffer
            matching_regex_value_buffer.write("(" + pattern + ")")

            # increments the index
            index += 1

            # in case the current index is in the limit of the python
            # regex compilation
            if index % REGEX_COMPILATION_LIMIT == 0:
                # retrieves the matching regex value from the matching
                # regex value buffer
                matching_regex_value = matching_regex_value_buffer.get_value()

                # compiles the matching regex value
                matching_regex = re.compile(matching_regex_value)

                # adds the matching regex to the matching regex list
                self.matching_regex_list.append(matching_regex)

                # sets the base value in matching regex base values map
                self.matching_regex_base_values_map[matching_regex] = current_base_value

                # re-sets the current base value
                current_base_value = index

                # resets the matching regex value buffer
                matching_regex_value_buffer.reset()

                # sets the is first flag
                is_first = True

        # retrieves the matching regex value from the matching
        # regex value buffer
        matching_regex_value = matching_regex_value_buffer.get_value()

        # in case the matching regex value is invalid (empty)
        if not matching_regex_value:
            # returns immediately
            return

        # compiles the matching regex value
        matching_regex = re.compile(matching_regex_value)

        # adds the matching regex to the matching regex list
        self.matching_regex_list.append(matching_regex)

        # sets the base value in matching regex base values map
        self.matching_regex_base_values_map[matching_regex] = current_base_value

    def _update_communication_matching_regex(self):
        """
        Updates the communication matching regex.
        """

        # starts the communication matching regex value buffer
        communication_matching_regex_value_buffer = colony.libs.string_buffer_util.StringBuffer()

        # clears the communication matching regex list
        self.communication_matching_regex_list = []

        # clears the communication matching regex base value map
        self.communication_matching_regex_base_values_map.clear()

        # sets the is first flag
        is_first = True

        # starts the index value
        index = 0

        # starts the current base value
        current_base_value = 0

        # iterates over all the patterns in the mvc service communication patterns list
        for pattern in self.mvc_service_communication_patterns_list:
            # in case it's the first
            if is_first:
                # unsets the is first flag
                is_first = False
            else:
                # adds the or operand to the communication matching regex value buffer
                communication_matching_regex_value_buffer.write("|")

            # adds the group name part of the regex to the communication matching regex value buffer
            communication_matching_regex_value_buffer.write("(" + pattern + ")")

            # increments the index
            index += 1

            # in case the current index is in the limit of the python
            # regex compilation
            if index % REGEX_COMPILATION_LIMIT == 0:
                # retrieves the communication matching regex value from the communication matching
                # regex value buffer and compiles it into the proper regex value
                communication_matching_regex_value = communication_matching_regex_value_buffer.get_value()
                reource_matching_regex = re.compile(communication_matching_regex_value)

                # adds the communication matching regex to the matching regex list
                self.communication_matching_regex_list.append(reource_matching_regex)

                # sets the base value in communication matching regex base values map
                self.communication_matching_regex_base_values_map[reource_matching_regex] = current_base_value

                # re-sets the current base value
                current_base_value = index

                # resets the matching regex value buffer
                communication_matching_regex_value_buffer.reset()

                # sets the is first flag
                is_first = True

        # retrieves the communication matching regex value from the communication matching
        # regex value buffer
        communication_matching_regex_value = communication_matching_regex_value_buffer.get_value()

        # in case the communication matching regex value is invalid (empty)
        # must return immediately
        if not communication_matching_regex_value: return

        # compiles the communication matching regex value
        communication_matching_regex = re.compile(communication_matching_regex_value)

        # adds the matching regex to the communication matching regex list
        self.communication_matching_regex_list.append(communication_matching_regex)

        # sets the base value in communication matching regex base values map
        self.communication_matching_regex_base_values_map[communication_matching_regex] = current_base_value

    def _update_resource_matching_regex(self):
        """
        Updates the resource matching regex.
        """

        # starts the resource matching regex value buffer
        resource_matching_regex_value_buffer = colony.libs.string_buffer_util.StringBuffer()

        # clears the resource matching regex list
        self.resource_matching_regex_list = []

        # clears the resource matching regex base value map
        self.resource_matching_regex_base_values_map.clear()

        # sets the is first flag
        is_first = True

        # starts the index value
        index = 0

        # starts the current base value
        current_base_value = 0

        # iterates over all the patterns in the mvc service resource patterns list
        for pattern in self.mvc_service_resource_patterns_list:
            # in case it's the first
            if is_first:
                # unsets the is first flag
                is_first = False
            else:
                # adds the or operand to the resource matching regex value buffer
                resource_matching_regex_value_buffer.write("|")

            # adds the group name part of the regex to the resource matching regex value buffer
            resource_matching_regex_value_buffer.write("(" + pattern + ")")

            # increments the index
            index += 1

            # in case the current index is in the limit of the python
            # regex compilation
            if index % REGEX_COMPILATION_LIMIT == 0:
                # retrieves the resource matching regex value from the resource matching
                # regex value buffer
                resource_matching_regex_value = resource_matching_regex_value_buffer.get_value()

                # compiles the resource matching regex value
                reource_matching_regex = re.compile(resource_matching_regex_value)

                # adds the resource matching regex to the matching regex list
                self.resource_matching_regex_list.append(reource_matching_regex)

                # sets the base value in resource matching regex base values map
                self.resource_matching_regex_base_values_map[reource_matching_regex] = current_base_value

                # re-sets the current base value
                current_base_value = index

                # resets the matching regex value buffer
                resource_matching_regex_value_buffer.reset()

                # sets the is first flag
                is_first = True

        # retrieves the resource matching regex value from the resource matching
        # regex value buffer
        resource_matching_regex_value = resource_matching_regex_value_buffer.get_value()

        # in case the resource matching regex value is invalid (empty)
        # must return immediately
        if not resource_matching_regex_value: return

        # compiles the resource matching regex value
        resource_matching_regex = re.compile(resource_matching_regex_value)

        # adds the matching regex to the resource matching regex list
        self.resource_matching_regex_list.append(resource_matching_regex)

        # sets the base value in resource matching regex base values map
        self.resource_matching_regex_base_values_map[resource_matching_regex] = current_base_value

    def __validate_match(self, rest_request, handler_attributes, resource_path):
        # unpacks the handler attributes, retrieving the handler
        # validation regex and the handler arguments
        validation_regex, arguments = handler_attributes

        # matches the resource path against the validation match
        # in case there is no (resource path) validation match
        # raises the runtime request exception
        validation_match = validation_regex.match(resource_path)
        if not validation_match:
            raise exceptions.RuntimeRequestException("invalid resource path validation match")

        # retrieves the length of the handler arguments, in order to be able
        # to conditionally validate the various parameters from it
        arguments_length = len(arguments)

        # retrieves the complete set of arguments that were provided
        # to be used as attributes by the handler
        method = arguments_length > 0 and arguments[0] or None
        operation_types = arguments_length > 1 and arguments[1] or ("get", "put", "post", "delete")
        encoders = arguments_length > 2 and arguments[2] or None
        contraints = arguments_length > 3 and arguments[3] or {}

        # casts both the operation types and the encoders as tuples
        # so that they remain compatible with the execution code
        operation_types = self.__cast_tuple(operation_types)
        encoders = self.__cast_tuple(encoders)

        # retrieves the request from the rest request to be used
        # in the retrieval of some attributes
        request = rest_request.get_request()

        # retrieves the various attributes associated with both the
        # request and the rest request that are going to be used in
        # the validation process
        operation_type_r = request.operation_type
        operation_type_r = operation_type_r.lower()
        encoder_name_r = rest_request.encoder_name

        # in case the request operation type does not exists in the
        # operation types, must returns with invalid value (validation
        # of operation type failed)
        if not operation_type_r in operation_types: return None

        # in case the encoders are defined and the request encoder name
        # does not exists in the encoders set must return with invalid
        # state (validation of encoder failed)
        if encoders and not encoder_name_r in encoders: return None

        # iterates over the complete set of constraints to
        for contraint_name, contraint_value in contraints.items():
            # retrieves the handler constraint value type
            contraint_value_t = type(contraint_value)

            # retrieves the attribute value base on the
            # handler constraint name
            attribute_value = rest_request.get_attribute(contraint_name)

            # tries to cast the attribute value using the constraint
            # type in case it fails returns in error
            try: attribute_value_c = contraint_value_t(attribute_value)
            except: return None

            # in case the attribute value (casted) is not equals
            # to the handler constraint value must return in error
            if attribute_value_c == contraint_value: return None

        # retrieves the (resource path) validation match groups map
        validation_match_groups_map = validation_match.groupdict()

        # creates the map containing the various parameters to be
        # "pushed" to the lower layer of the mvc stack
        parameters = {
            "file_handler" : self.mvc_file_handler,
            "communication_handler" : self.mvc_communication_handler,
            "method" : operation_type_r,
            "encoder_name" : encoder_name_r,
            "pattern_names" : validation_match_groups_map
        }

        # creates the handler tuple, containing both the method to
        # be used for handling and the parameters to be passed and
        # returns it to the caller method
        handler_tuple = (
            method,
            parameters
        )
        return handler_tuple

    def __cast_tuple(self, value):
        """
        Casts the given value to a tuple,
        converting it if required.

        @type value: Object
        @param value: The value to be "casted".
        @rtype: Tuple
        @return: The casted tuple value.
        """

        # in case the value is invalid, returns
        # the value immediately
        if value == None: return value

        # creates the tuple value from the value and returns
        # the value to the caller method
        tuple_value = type(value) == types.TupleType and value or (value,)
        return tuple_value
