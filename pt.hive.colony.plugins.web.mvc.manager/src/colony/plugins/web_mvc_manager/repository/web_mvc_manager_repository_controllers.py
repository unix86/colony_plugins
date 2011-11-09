#!/usr/bin/python
# -*- coding: utf-8 -*-

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

__author__ = "João Magalhães <joamag@hive.pt>"
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

import time
import copy
import types

import colony.libs.importer_util

SERIALIZER_VALUE = "serializer"
""" The serializer value """

TEMPLATE_FILE_VALUE = "template_file"
""" The template file value """

INSTALLED_VALUE = "installed"
""" The installed value """

UNINSTALLED_VALUE = "uninstalled"
""" The uninstalled value """

WEB_MVC_UTILS_VALUE = "web_mvc_utils"
""" The web mvc utils value """

DEFAULT_ENCODING = "utf-8"
""" The default encoding value """

WEB_MVC_MANAGER_REPOSITORY_RESOURCES_PATH = "web_mvc_manager/repository/resources"
""" The web mvc manager repository resources path """

INSTALLATION_DELAY = 1.0
""" The delay induce uppon installation """

# imports the web mvc utils
web_mvc_utils = colony.libs.importer_util.__importer__(WEB_MVC_UTILS_VALUE)

class RepositoryController:
    """
    The web mvc manager repository controller.
    """

    web_mvc_manager_repository_plugin = None
    """ The web mvc manager repository plugin """

    web_mvc_manager_repository = None
    """ The web mvc manager repository """

    def __init__(self, web_mvc_manager_repository_plugin, web_mvc_manager_repository):
        """
        Constructor of the class.

        @type web_mvc_manager_repository_plugin: WebMvcManagerRepositoryPlugin
        @param web_mvc_manager_repository_plugin: The web mvc manager repository plugin.
        @type web_mvc_manager_repository: WebMvcManagerRepository
        @param web_mvc_manager_repository: The web mvc manager repository.
        """

        self.web_mvc_manager_repository_plugin = web_mvc_manager_repository_plugin
        self.web_mvc_manager_repository = web_mvc_manager_repository

    def start(self):
        """
        Method called upon structure initialization.
        """

        # sets the relative resources path
        self.set_relative_resources_path(WEB_MVC_MANAGER_REPOSITORY_RESOURCES_PATH, extra_templates_path = "repository")

    def validate(self, rest_request, parameters, validation_parameters):
        # returns the result of the require permission call
        return []

    @web_mvc_utils.serialize_exceptions("all")
    @web_mvc_utils.validated_method("repository.list")
    def handle_list_ajx(self, rest_request, parameters = {}):
        # retrieves the json plugin
        json_plugin = self.web_mvc_manager_repository_plugin.json_plugin

        # sets the serializer in the parameters
        parameters[SERIALIZER_VALUE] = json_plugin

        # retrieves the template file
        template_file = self.retrieve_template_file("repository_list_contents.html.tpl")

        # assigns the session variables to the template file
        self.assign_session_template_file(rest_request, template_file)

        # applies the base path to the template file
        self.apply_base_path_template_file(rest_request, template_file)

        # processes the template file and sets the request contents
        self.process_set_contents(rest_request, template_file)

    @web_mvc_utils.serialize_exceptions("all")
    @web_mvc_utils.validated_method("repository.list")
    def handle_list(self, rest_request, parameters = {}):
        # retrieves the template file from the parameters
        template_file = parameters[TEMPLATE_FILE_VALUE]

        # resolves the relative resources path to obtain the absolute page include to be used
        absolute_page_include = self.resolve_relative_path(WEB_MVC_MANAGER_REPOSITORY_RESOURCES_PATH, "templates/repository/repository_list_contents.html.tpl")

        # assigns the includes to the templates
        self.assign_include_template_file(template_file, "page_include", absolute_page_include)
        self.assign_include_template_file(template_file, "side_panel_include", "side_panel/side_panel_configuration.html.tpl")

        # assigns the session variables to the template file
        self.assign_session_template_file(rest_request, template_file)

        # applies the base path to the template file
        self.apply_base_path_template_file(rest_request, template_file)

        # processes the template file and sets the request contents
        self.process_set_contents(rest_request, template_file)

    @web_mvc_utils.serialize_exceptions("all")
    @web_mvc_utils.validated_method("repository.list")
    def handle_partial_list_ajx(self, rest_request, parameters = {}):
        # retrieves the form data by processing the form
        form_data_map = self.process_form_data(rest_request, DEFAULT_ENCODING)

        # retrieves the web search helper
        search_helper = parameters["search_helper"]

        # retrieves the search values
        search_query = form_data_map["search_query"]
        start_record = form_data_map["start_record"]
        number_records = form_data_map["number_records"]

        # converts the the search values
        start_record = int(start_record)
        number_records = int(number_records)

        # retrieves the filtered repositories
        filtered_repositories = self._get_filtered_repositories(rest_request, search_query)

        # retrieves the partial filter from the filtered repositories
        partial_filtered_repositories, start_record, number_records, total_number_records = search_helper.partial_filter(rest_request, filtered_repositories, start_record, number_records)

        # retrieves the template file
        template_file = self.retrieve_template_file("repository_partial_list_contents.html.tpl")

        # assigns the template variables
        template_file.assign("repositories", partial_filtered_repositories)
        template_file.assign("start_record", start_record)
        template_file.assign("number_records", number_records)
        template_file.assign("total_number_records", total_number_records)

        # assigns the session variables to the template file
        self.assign_session_template_file(rest_request, template_file)

        # applies the base path to the template file
        self.apply_base_path_template_file(rest_request, template_file)

        # processes the template file and sets the request contents
        self.process_set_contents(rest_request, template_file)

    @web_mvc_utils.serialize_exceptions("all")
    @web_mvc_utils.validated_method("repository.show")
    def handle_show_ajx(self, rest_request, parameters = {}):
        # retrieves the json plugin
        json_plugin = self.web_mvc_manager_repository_plugin.json_plugin

        # sets the serializer in the parameters
        parameters[SERIALIZER_VALUE] = json_plugin

        # retrieves the repository index pattern
        repository_index = self.get_pattern(parameters, "repository_index", types.IntType)

        # retrieves the specified repository
        repository = self._get_repository(rest_request, repository_index)

        # retrieves the template file
        template_file = self.retrieve_template_file("repository_show_contents.html.tpl")

        # assigns the template variables
        template_file.assign("repository", repository)
        template_file.assign("repository_index", repository_index)

        # assigns the session variables to the template file
        self.assign_session_template_file(rest_request, template_file)

        # applies the base path to the template file
        self.apply_base_path_template_file(rest_request, template_file)

        # processes the template file and sets the request contents
        self.process_set_contents(rest_request, template_file)

    @web_mvc_utils.serialize_exceptions("all")
    @web_mvc_utils.validated_method("repository.show")
    def handle_show(self, rest_request, parameters = {}):
        # retrieves the repository index pattern
        repository_index = self.get_pattern(parameters, "repository_index", types.IntType)

        # retrieves the specified repository
        repository = self._get_repository(rest_request, repository_index)

        # retrieves the template file from the parameters
        template_file = parameters[TEMPLATE_FILE_VALUE]

        # resolves the relative resources path to obtain the absolute page include to be used
        absolute_page_include = self.resolve_relative_path(WEB_MVC_MANAGER_REPOSITORY_RESOURCES_PATH, "templates/repository/repository_show_contents.html.tpl")

        # assigns the includes to the templates
        self.assign_include_template_file(template_file, "page_include", absolute_page_include)
        self.assign_include_template_file(template_file, "side_panel_include", "side_panel/side_panel_update.html.tpl")

        # assigns the template variables
        template_file.assign("repository", repository)
        template_file.assign("repository_index", repository_index)

        # assigns the session variables to the template file
        self.assign_session_template_file(rest_request, template_file)

        # applies the base path to the template file
        self.apply_base_path_template_file(rest_request, template_file)

        # processes the template file and sets the request contents
        self.process_set_contents(rest_request, template_file)

    def _get_repository(self, rest_request, repository_index):
        # retrieves the system updater plugin
        system_updater_plugin = self.web_mvc_manager_repository_plugin.system_updater_plugin

        # retrieves all the repositories
        repositories = system_updater_plugin.get_repositories()

        # retrieves the repository from the repositories list
        repository = repositories[repository_index - 1]

        # retrieves the repository name
        repository_name = repository.name

        # retrieves the repository for the repository with the given name
        repository_information = system_updater_plugin.get_repository_information_by_repository_name(repository_name)

        # returns the repository information
        return repository_information

    def _get_filtered_repositories(self, rest_request, search_query):
        # retrieves the repositories
        repositories = self._get_repositories()

        # creates the filtered repositories list
        filtered_repositories = [repository for repository in repositories if not repository.name.find(search_query) == -1]

        # returns the filtered repositories
        return filtered_repositories

    def _get_filtered_repository_bundles(self, rest_request, search_query, repository_index):
        # retrieves the repository
        repository = self._get_repository(rest_request, repository_index)

        # creates the filtered repository bundles
        filtered_repository_bundles = [repository_bundle for repository_bundle in repository.bundles if not repository_bundle.id.find(search_query) == -1]

        # returns the filtered repository bundles
        return filtered_repository_bundles

    def _get_filtered_repository_plugins(self, rest_request, search_query, repository_index):
        # retrieves the repository
        repository = self._get_repository(rest_request, repository_index)

        # creates the filtered repository plugins
        filtered_repository_plugins = [repository_plugin for repository_plugin in repository.plugins if not repository_plugin.id.find(search_query) == -1]

        # returns the filtered repository plugins
        return filtered_repository_plugins

    def _get_filtered_repository_containers(self, rest_request, search_query, repository_index):
        # retrieves the repository
        repository = self._get_repository(rest_request, repository_index)

        # creates the filtered repository containers
        filtered_repository_containers = [repository_container for repository_container in repository.containers if not repository_container.id.find(search_query) == -1]

        # returns the filtered repository containers
        return filtered_repository_containers

    def _get_repositories(self):
        # retrieves the system updater plugin
        system_updater_plugin = self.web_mvc_manager_repository_plugin.system_updater_plugin

        # retrieves all the repositories
        repositories = system_updater_plugin.get_repositories()

        # returns the repositories
        return repositories

class RepositoryBundlesController:
    """
    The web mvc manager repository bundles controller.
    """

    web_mvc_manager_repository_plugin = None
    """ The web mvc manager repository plugin """

    web_mvc_manager_repository = None
    """ The web mvc manager repository """

    def __init__(self, web_mvc_manager_repository_plugin, web_mvc_manager_repository):
        """
        Constructor of the class.

        @type web_mvc_manager_repository_plugin: WebMvcManagerRepositoryPlugin
        @param web_mvc_manager_repository_plugin: The web mvc manager repository plugin.
        @type web_mvc_manager_repository: WebMvcManagerRepository
        @param web_mvc_manager_repository: The web mvc manager repository.
        """

        self.web_mvc_manager_repository_plugin = web_mvc_manager_repository_plugin
        self.web_mvc_manager_repository = web_mvc_manager_repository

    def start(self):
        """
        Method called upon structure initialization.
        """

        # sets the relative resources path
        self.set_relative_resources_path(WEB_MVC_MANAGER_REPOSITORY_RESOURCES_PATH, extra_templates_path = "repository_bundles")

    def validate(self, rest_request, parameters, validation_parameters):
        # returns the result of the require permission call
        return []

    @web_mvc_utils.serialize_exceptions("all")
    @web_mvc_utils.validated_method("repository.list")
    def handle_list_ajx(self, rest_request, parameters = {}):
        # retrieves the json plugin
        json_plugin = self.web_mvc_manager_repository_plugin.json_plugin

        # sets the serializer in the parameters
        parameters[SERIALIZER_VALUE] = json_plugin

        # retrieves the repository index pattern
        repository_index = self.get_pattern(parameters, "repository_index", types.IntType)

        # retrieves the template file
        template_file = self.retrieve_template_file("repository_bundles_list_contents.html.tpl")

        # assigns the repository index to the template
        template_file.assign("repository_index", repository_index)

        # assigns the session variables to the template file
        self.assign_session_template_file(rest_request, template_file)

        # applies the base path to the template file
        self.apply_base_path_template_file(rest_request, template_file)

        # processes the template file and sets the request contents
        self.process_set_contents(rest_request, template_file)

    @web_mvc_utils.serialize_exceptions("all")
    @web_mvc_utils.validated_method("repository.list")
    def handle_list(self, rest_request, parameters = {}):
        # retrieves the template file from the parameters
        template_file = parameters[TEMPLATE_FILE_VALUE]

        # retrieves the repository index pattern
        repository_index = self.get_pattern(parameters, "repository_index", types.IntType)

        # resolves the relative resources path to obtain the absolute page include to be used
        absolute_page_include = self.resolve_relative_path(WEB_MVC_MANAGER_REPOSITORY_RESOURCES_PATH, "templates/repository_bundles/repository_bundles_list_contents.html.tpl")

        # assigns the includes to the templates
        self.assign_include_template_file(template_file, "page_include", absolute_page_include)
        self.assign_include_template_file(template_file, "side_panel_include", "side_panel/side_panel_configuration.html.tpl")

        # assigns the repository index to the template
        template_file.assign("repository_index", repository_index)

        # assigns the session variables to the template file
        self.assign_session_template_file(rest_request, template_file)

        # applies the base path to the template file
        self.apply_base_path_template_file(rest_request, template_file)

        # processes the template file and sets the request contents
        self.process_set_contents(rest_request, template_file)

    @web_mvc_utils.serialize_exceptions("all")
    @web_mvc_utils.validated_method("repository.list")
    def handle_partial_list_ajx(self, rest_request, parameters = {}):
        # retrieves the json plugin
        json_plugin = self.web_mvc_manager_repository_plugin.json_plugin

        # sets the serializer in the parameters
        parameters[SERIALIZER_VALUE] = json_plugin

        # retrieves the required controllers
        web_mvc_manager_repository_repository_controller = self.web_mvc_manager_repository.web_mvc_manager_repository_repository_controller

        # retrieves the form data by processing the form
        form_data_map = self.process_form_data(rest_request, DEFAULT_ENCODING)

        # retrieves the web search helper
        search_helper = parameters["search_helper"]

        # retrieves the repository index pattern
        repository_index = self.get_pattern(parameters, "repository_index", types.IntType)

        # retrieves the search values
        search_query = form_data_map["search_query"]
        start_record = form_data_map["start_record"]
        number_records = form_data_map["number_records"]

        # converts the the search values
        start_record = int(start_record)
        number_records = int(number_records)

        # retrieves the filtered repositories
        filtered_repository_bundles = web_mvc_manager_repository_repository_controller._get_filtered_repository_bundles(rest_request, search_query, repository_index)

        # retrieves the partial filter from the filtered repository bundles
        partial_filtered_repository_bundles, start_record, number_records, total_number_records = search_helper.partial_filter(rest_request, filtered_repository_bundles, start_record, number_records)

        # retrieves the template file
        template_file = self.retrieve_template_file("repository_bundles_partial_list_contents.html.tpl")

        # assigns the template variables
        template_file.assign("repository_bundles", partial_filtered_repository_bundles)
        template_file.assign("start_record", start_record)
        template_file.assign("number_records", number_records)
        template_file.assign("total_number_records", total_number_records)

        # assigns the session variables to the template file
        self.assign_session_template_file(rest_request, template_file)

        # applies the base path to the template file
        self.apply_base_path_template_file(rest_request, template_file)

        # processes the template file and sets the request contents
        self.process_set_contents(rest_request, template_file)

    @web_mvc_utils.serialize_exceptions("all")
    @web_mvc_utils.validated_method("repository.install_bundle")
    def handle_install_bundle_serialized(self, rest_request, parameters = {}):
        # retrieves the serializer
        serializer = parameters[SERIALIZER_VALUE]

        # retrieves the form data by processing the form
        form_data_map = self.process_form_data(rest_request, DEFAULT_ENCODING)

        # retrieves the communication helper
        communication_helper = parameters["communication_helper"]

        # retrieves the bundle id
        bundle_id = form_data_map["bundle_id"]

        # retrieves the bundle version
        bundle_version = form_data_map["bundle_version"]

        # install the bundle and retrieves the result
        install_bundle_result = self._install_bundle(rest_request, bundle_id, bundle_version)

        # serializes the install result using the serializer
        serialized_status = serializer.dumps(install_bundle_result)

        # sets the serialized status as the rest request contents
        self.set_contents(rest_request, serialized_status)

        # sends the serialized broadcast message
        communication_helper.send_serialized_broadcast_message(parameters, "web_mvc_manager/communication", "web_mvc_manager/plugin/install", serialized_status)

    def handle_install_bundle_json(self, rest_request, parameters = {}):
        # retrieves the json bundle
        json_plugin = self.web_mvc_manager_repository_plugin.json_plugin

        # sets the serializer in the parameters
        parameters[SERIALIZER_VALUE] = json_plugin

        # handles the request with the general
        # handle install bundle serialized method
        self.handle_install_bundle_serialized(rest_request, parameters)

    @web_mvc_utils.serialize_exceptions("all")
    @web_mvc_utils.validated_method("repository.uninstall_bundle")
    def handle_uninstall_bundle_serialized(self, rest_request, parameters = {}):
        # retrieves the serializer
        serializer = parameters[SERIALIZER_VALUE]

        # retrieves the form data by processing the form
        form_data_map = self.process_form_data(rest_request, DEFAULT_ENCODING)

        # retrieves the communication helper
        communication_helper = parameters["communication_helper"]

        # retrieves the bundle id
        bundle_id = form_data_map["bundle_id"]

        # retrieves the bundle version
        bundle_version = form_data_map["bundle_version"]

        # uninstall the bundle and retrieves the result
        uninstall_bundle_result = self._uninstall_bundle(rest_request, bundle_id, bundle_version)

        # serializes the uninstall result using the serializer
        serialized_status = serializer.dumps(uninstall_bundle_result)

        # sets the serialized status as the rest request contents
        self.set_contents(rest_request, serialized_status)

        # sends the serialized broadcast message
        communication_helper.send_serialized_broadcast_message(parameters, "web_mvc_manager/communication", "web_mvc_manager/plugin/install", serialized_status)

    def handle_uninstall_bundle_json(self, rest_request, parameters = {}):
        # retrieves the json plugin
        json_plugin = self.web_mvc_manager_repository_plugin.json_plugin

        # sets the serializer in the parameters
        parameters[SERIALIZER_VALUE] = json_plugin

        # handles the request with the general
        # handle uninstall bundle serialized method
        self.handle_uninstall_bundle_serialized(rest_request, parameters)

    def _install_bundle(self, rest_request, bundle_id, bundle_version):
        # retrieves the plugin manager
        plugin_manager = self.web_mvc_manager_repository_plugin.manager

        # retrieves the system updater plugin
        system_updater_plugin = self.web_mvc_manager_repository_plugin.system_updater_plugin

        # creates the delta plugin install map
        delta_plugin_install_map = {
            INSTALLED_VALUE : [],
            UNINSTALLED_VALUE : []
        }

        # retrieves the (beginning) list of available bundles
        available_plugins_beginning = copy.copy(plugin_manager.get_all_plugins())

        # tries to install the bundle
        system_updater_plugin.install_bundle(bundle_id, bundle_version)

        # sleeps for a second to give time for the autoloader to update
        # this delay is induced on purpose
        time.sleep(INSTALLATION_DELAY)

        # retrieves the (end) list of available plugins
        available_plugins_end = plugin_manager.get_all_plugins()

        # iterates over all the plugins available at the beginning
        # to check if they exist in the current available plugins
        for available_plugin_beginning in available_plugins_beginning:
            if not available_plugin_beginning in available_plugins_end:
                delta_plugin_install_map[UNINSTALLED_VALUE].append(available_plugin_beginning.id)

        # iterates over all the plugins available at the end
        # to check if they exist in the previously available plugins
        for available_plugin_end in available_plugins_end:
            if not available_plugin_end in available_plugins_beginning:
                delta_plugin_install_map[INSTALLED_VALUE].append(available_plugin_end.id)

        # returns the delta plugin install map
        return delta_plugin_install_map

    def _uninstall_bundle(self, rest_request, bundle_id, bundle_version):
        # retrieves the plugin manager
        plugin_manager = self.web_mvc_manager_repository_plugin.manager

        # retrieves the system updater plugin
        system_updater_plugin = self.web_mvc_manager_repository_plugin.system_updater_plugin

        # creates the delta plugin install map
        delta_plugin_install_map = {
            INSTALLED_VALUE : [],
            UNINSTALLED_VALUE : []
        }

        # retrieves the (beginning) list of available plugins
        available_plugins_beginning = copy.copy(plugin_manager.get_all_plugins())

        # tries to uninstall the bundle
        system_updater_plugin.uninstall_bundle(bundle_id, bundle_version)

        # sleeps for a second to give time for the autoloader to update
        # this delay is induced on purpose
        time.sleep(INSTALLATION_DELAY)

        # retrieves the (end) list of available plugins
        available_plugins_end = plugin_manager.get_all_plugins()

        # iterates over all the plugins available at the beginning
        # to check if they exist in the current available plugins
        for available_plugin_beginning in available_plugins_beginning:
            if not available_plugin_beginning in available_plugins_end:
                delta_plugin_install_map[UNINSTALLED_VALUE].append(available_plugin_beginning.id)

        # iterates over all the plugins available at the end
        # to check if they exist in the previously available plugins
        for available_plugin_end in available_plugins_end:
            if not available_plugin_end in available_plugins_beginning:
                delta_plugin_install_map[INSTALLED_VALUE].append(available_plugin_end.id)

        # returns the delta plugin install map
        return delta_plugin_install_map

class RepositoryPluginsController:
    """
    The web mvc manager repository plugins controller.
    """

    web_mvc_manager_repository_plugin = None
    """ The web mvc manager repository plugin """

    web_mvc_manager_repository = None
    """ The web mvc manager repository """

    def __init__(self, web_mvc_manager_repository_plugin, web_mvc_manager_repository):
        """
        Constructor of the class.

        @type web_mvc_manager_repository_plugin: WebMvcManagerRepositoryPlugin
        @param web_mvc_manager_repository_plugin: The web mvc manager repository plugin.
        @type web_mvc_manager_repository: WebMvcManagerRepository
        @param web_mvc_manager_repository: The web mvc manager repository.
        """

        self.web_mvc_manager_repository_plugin = web_mvc_manager_repository_plugin
        self.web_mvc_manager_repository = web_mvc_manager_repository

    def start(self):
        """
        Method called upon structure initialization.
        """

        # sets the relative resources path
        self.set_relative_resources_path(WEB_MVC_MANAGER_REPOSITORY_RESOURCES_PATH, extra_templates_path = "repository_plugins")

    def validate(self, rest_request, parameters, validation_parameters):
        # returns the result of the require permission call
        return []

    @web_mvc_utils.serialize_exceptions("all")
    @web_mvc_utils.validated_method("repository.list")
    def handle_list_ajx(self, rest_request, parameters = {}):
        # retrieves the json plugin
        json_plugin = self.web_mvc_manager_repository_plugin.json_plugin

        # sets the serializer in the parameters
        parameters[SERIALIZER_VALUE] = json_plugin

        # retrieves the repository index pattern
        repository_index = self.get_pattern(parameters, "repository_index", types.IntType)

        # retrieves the template file
        template_file = self.retrieve_template_file("repository_plugins_list_contents.html.tpl")

        # assigns the repository index to the template
        template_file.assign("repository_index", repository_index)

        # assigns the session variables to the template file
        self.assign_session_template_file(rest_request, template_file)

        # applies the base path to the template file
        self.apply_base_path_template_file(rest_request, template_file)

        # processes the template file and sets the request contents
        self.process_set_contents(rest_request, template_file)

    @web_mvc_utils.serialize_exceptions("all")
    @web_mvc_utils.validated_method("repository.list")
    def handle_list(self, rest_request, parameters = {}):
        # retrieves the template file from the parameters
        template_file = parameters[TEMPLATE_FILE_VALUE]

        # retrieves the repository index pattern
        repository_index = self.get_pattern(parameters, "repository_index", types.IntType)

        # resolves the relative resources path to obtain the absolute page include to be used
        absolute_page_include = self.resolve_relative_path(WEB_MVC_MANAGER_REPOSITORY_RESOURCES_PATH, "templates/repository_plugins/repository_plugins_list_contents.html.tpl")

        # assigns the includes to the templates
        self.assign_include_template_file(template_file, "page_include", absolute_page_include)
        self.assign_include_template_file(template_file, "side_panel_include", "side_panel/side_panel_configuration.html.tpl")

        # assigns the repository index to the template
        template_file.assign("repository_index", repository_index)

        # assigns the session variables to the template file
        self.assign_session_template_file(rest_request, template_file)

        # applies the base path to the template file
        self.apply_base_path_template_file(rest_request, template_file)

        # processes the template file and sets the request contents
        self.process_set_contents(rest_request, template_file)

    @web_mvc_utils.serialize_exceptions("all")
    @web_mvc_utils.validated_method("repository.list")
    def handle_partial_list_ajx(self, rest_request, parameters = {}):
        # retrieves the json plugin
        json_plugin = self.web_mvc_manager_repository_plugin.json_plugin

        # sets the serializer in the parameters
        parameters[SERIALIZER_VALUE] = json_plugin

        # retrieves the required controllers
        web_mvc_manager_repository_repository_controller = self.web_mvc_manager_repository.web_mvc_manager_repository_repository_controller

        # retrieves the form data by processing the form
        form_data_map = self.process_form_data(rest_request, DEFAULT_ENCODING)

        # retrieves the web search helper
        search_helper = parameters["search_helper"]

        # retrieves the repository index pattern
        repository_index = self.get_pattern(parameters, "repository_index", types.IntType)

        # retrieves the search values
        search_query = form_data_map["search_query"]
        start_record = form_data_map["start_record"]
        number_records = form_data_map["number_records"]

        # converts the repository index to integer
        repository_index = int(repository_index)

        # converts the the search values
        start_record = int(start_record)
        number_records = int(number_records)

        # retrieves the filtered repositories
        filtered_repository_plugins = web_mvc_manager_repository_repository_controller._get_filtered_repository_plugins(rest_request, search_query, repository_index)

        # retrieves the partial filter from the filtered repository plugins
        partial_filtered_repository_plugins, start_record, number_records, total_number_records = search_helper.partial_filter(rest_request, filtered_repository_plugins, start_record, number_records)

        # retrieves the template file
        template_file = self.retrieve_template_file("repository_plugins_partial_list_contents.html.tpl")

        # assigns the template variables
        template_file.assign("repository_plugins", partial_filtered_repository_plugins)
        template_file.assign("start_record", start_record)
        template_file.assign("number_records", number_records)
        template_file.assign("total_number_records", total_number_records)

        # assigns the session variables to the template file
        self.assign_session_template_file(rest_request, template_file)

        # applies the base path to the template file
        self.apply_base_path_template_file(rest_request, template_file)

        # processes the template file and sets the request contents
        self.process_set_contents(rest_request, template_file)

    @web_mvc_utils.serialize_exceptions("all")
    @web_mvc_utils.validated_method("repository.install_plugin")
    def handle_install_plugin_serialized(self, rest_request, parameters = {}):
        # retrieves the serializer
        serializer = parameters[SERIALIZER_VALUE]

        # retrieves the form data by processing the form
        form_data_map = self.process_form_data(rest_request, DEFAULT_ENCODING)

        # retrieves the communication helper
        communication_helper = parameters["communication_helper"]

        # retrieves the plugin id
        plugin_id = form_data_map["plugin_id"]

        # retrieves the plugin version
        plugin_version = form_data_map["plugin_version"]

        # install the plugin and retrieves the result
        install_plugin_result = self._install_plugin(rest_request, plugin_id, plugin_version)

        # serializes the install result using the serializer
        serialized_status = serializer.dumps(install_plugin_result)

        # sets the serialized status as the rest request contents
        self.set_contents(rest_request, serialized_status)

        # sends the serialized broadcast message
        communication_helper.send_serialized_broadcast_message(parameters, "web_mvc_manager/communication", "web_mvc_manager/plugin/install", serialized_status)

    def handle_install_plugin_json(self, rest_request, parameters = {}):
        # retrieves the json plugin
        json_plugin = self.web_mvc_manager_repository_plugin.json_plugin

        # sets the serializer in the parameters
        parameters[SERIALIZER_VALUE] = json_plugin

        # handles the request with the general
        # handle install plugin serialized method
        self.handle_install_plugin_serialized(rest_request, parameters)

    @web_mvc_utils.serialize_exceptions("all")
    @web_mvc_utils.validated_method("repository.uninstall_plugin")
    def handle_uninstall_plugin_serialized(self, rest_request, parameters = {}):
        # retrieves the serializer
        serializer = parameters[SERIALIZER_VALUE]

        # retrieves the form data by processing the form
        form_data_map = self.process_form_data(rest_request, DEFAULT_ENCODING)

        # retrieves the communication helper
        communication_helper = parameters["communication_helper"]

        # retrieves the plugin id
        plugin_id = form_data_map["plugin_id"]

        # retrieves the plugin version
        plugin_version = form_data_map["plugin_version"]

        # uninstall the plugin and retrieves the result
        uninstall_plugin_result = self._uninstall_plugin(rest_request, plugin_id, plugin_version)

        # serializes the uninstall result using the serializer
        serialized_status = serializer.dumps(uninstall_plugin_result)

        # sets the serialized status as the rest request contents
        self.set_contents(rest_request, serialized_status)

        # sends the serialized broadcast message
        communication_helper.send_serialized_broadcast_message(parameters, "web_mvc_manager/communication", "web_mvc_manager/plugin/install", serialized_status)

    def handle_uninstall_plugin_json(self, rest_request, parameters = {}):
        # retrieves the json plugin
        json_plugin = self.web_mvc_manager_repository_plugin.json_plugin

        # sets the serializer in the parameters
        parameters[SERIALIZER_VALUE] = json_plugin

        # handles the request with the general
        # handle uninstall plugin serialized method
        self.handle_uninstall_plugin_serialized(rest_request, parameters)

    def _install_plugin(self, rest_request, plugin_id, plugin_version):
        # retrieves the plugin manager
        plugin_manager = self.web_mvc_manager_repository_plugin.manager

        # retrieves the system updater plugin
        system_updater_plugin = self.web_mvc_manager_repository_plugin.system_updater_plugin

        # creates the delta plugin install map
        delta_plugin_install_map = {
            INSTALLED_VALUE : [],
            UNINSTALLED_VALUE : []
        }

        # retrieves the (beginning) list of available plugins
        available_plugins_beginning = copy.copy(plugin_manager.get_all_plugins())

        # tries to install the plugin
        system_updater_plugin.install_plugin(plugin_id, plugin_version)

        # sleeps for a second to give time for the autoloader to update
        # this delay is induced on purpose
        time.sleep(INSTALLATION_DELAY)

        # retrieves the (end) list of available plugins
        available_plugins_end = plugin_manager.get_all_plugins()

        # iterates over all the plugins available at the beginning
        # to check if they exist in the current available plugins
        for available_plugin_beginning in available_plugins_beginning:
            if not available_plugin_beginning in available_plugins_end:
                delta_plugin_install_map[UNINSTALLED_VALUE].append(available_plugin_beginning.id)

        # iterates over all the plugins available at the end
        # to check if they exist in the previously available plugins
        for available_plugin_end in available_plugins_end:
            if not available_plugin_end in available_plugins_beginning:
                delta_plugin_install_map[INSTALLED_VALUE].append(available_plugin_end.id)

        # returns the delta plugin install map
        return delta_plugin_install_map

    def _uninstall_plugin(self, rest_request, plugin_id, plugin_version):
        # retrieves the plugin manager
        plugin_manager = self.web_mvc_manager_repository_plugin.manager

        # retrieves the system updater plugin
        system_updater_plugin = self.web_mvc_manager_repository_plugin.system_updater_plugin

        # creates the delta plugin install map
        delta_plugin_install_map = {
            INSTALLED_VALUE : [],
            UNINSTALLED_VALUE : []
        }

        # retrieves the (beginning) list of available plugins
        available_plugins_beginning = copy.copy(plugin_manager.get_all_plugins())

        # tries to uninstall the plugin
        system_updater_plugin.uninstall_plugin(plugin_id, plugin_version)

        # sleeps for a second to give time for the autoloader to update
        # this delay is induced on purpose
        time.sleep(INSTALLATION_DELAY)

        # retrieves the (end) list of available plugins
        available_plugins_end = plugin_manager.get_all_plugins()

        # iterates over all the plugins available at the beginning
        # to check if they exist in the current available plugins
        for available_plugin_beginning in available_plugins_beginning:
            if not available_plugin_beginning in available_plugins_end:
                delta_plugin_install_map[UNINSTALLED_VALUE].append(available_plugin_beginning.id)

        # iterates over all the plugins available at the end
        # to check if they exist in the previously available plugins
        for available_plugin_end in available_plugins_end:
            if not available_plugin_end in available_plugins_beginning:
                delta_plugin_install_map[INSTALLED_VALUE].append(available_plugin_end.id)

        # returns the delta plugin install map
        return delta_plugin_install_map

class RepositoryContainersController:
    """
    The web mvc manager repository containers controller.
    """

    web_mvc_manager_repository_plugin = None
    """ The web mvc manager repository plugin """

    web_mvc_manager_repository = None
    """ The web mvc manager repository """

    def __init__(self, web_mvc_manager_repository_plugin, web_mvc_manager_repository):
        """
        Constructor of the class.

        @type web_mvc_manager_repository_plugin: WebMvcManagerRepositoryPlugin
        @param web_mvc_manager_repository_plugin: The web mvc manager repository plugin.
        @type web_mvc_manager_repository: WebMvcManagerRepository
        @param web_mvc_manager_repository: The web mvc manager repository.
        """

        self.web_mvc_manager_repository_plugin = web_mvc_manager_repository_plugin
        self.web_mvc_manager_repository = web_mvc_manager_repository

    def start(self):
        """
        Method called upon structure initialization.
        """

        # sets the relative resources path
        self.set_relative_resources_path(WEB_MVC_MANAGER_REPOSITORY_RESOURCES_PATH, extra_templates_path = "repository_containers")

    def validate(self, rest_request, parameters, validation_parameters):
        # returns the result of the require permission call
        return []

    @web_mvc_utils.serialize_exceptions("all")
    @web_mvc_utils.validated_method("repository.list")
    def handle_list_ajx(self, rest_request, parameters = {}):
        # retrieves the json plugin
        json_plugin = self.web_mvc_manager_repository_plugin.json_plugin

        # sets the serializer in the parameters
        parameters[SERIALIZER_VALUE] = json_plugin

        # retrieves the repository index pattern
        repository_index = self.get_pattern(parameters, "repository_index", types.IntType)

        # retrieves the template file
        template_file = self.retrieve_template_file("repository_containers_list_contents.html.tpl")

        # assigns the repository index to the template
        template_file.assign("repository_index", repository_index)

        # assigns the session variables to the template file
        self.assign_session_template_file(rest_request, template_file)

        # applies the base path to the template file
        self.apply_base_path_template_file(rest_request, template_file)

        # processes the template file and sets the request contents
        self.process_set_contents(rest_request, template_file)

    @web_mvc_utils.serialize_exceptions("all")
    @web_mvc_utils.validated_method("repository.list")
    def handle_list(self, rest_request, parameters = {}):
        # retrieves the template file from the parameters
        template_file = parameters[TEMPLATE_FILE_VALUE]

        # retrieves the repository index pattern
        repository_index = self.get_pattern(parameters, "repository_index", types.IntType)

        # resolves the relative resources path to obtain the absolute page include to be used
        absolute_page_include = self.resolve_relative_path(WEB_MVC_MANAGER_REPOSITORY_RESOURCES_PATH, "templates/repository_containers/repository_containers_list_contents.html.tpl")

        # assigns the includes to the templates
        self.assign_include_template_file(template_file, "page_include", absolute_page_include)
        self.assign_include_template_file(template_file, "side_panel_include", "side_panel/side_panel_configuration.html.tpl")

        # assigns the repository index to the template
        template_file.assign("repository_index", repository_index)

        # assigns the session variables to the template file
        self.assign_session_template_file(rest_request, template_file)

        # applies the base path to the template file
        self.apply_base_path_template_file(rest_request, template_file)

        # processes the template file and sets the request contents
        self.process_set_contents(rest_request, template_file)

    @web_mvc_utils.serialize_exceptions("all")
    @web_mvc_utils.validated_method("repository.list")
    def handle_partial_list_ajx(self, rest_request, parameters = {}):
        # retrieves the json plugin
        json_plugin = self.web_mvc_manager_repository_plugin.json_plugin

        # sets the serializer in the parameters
        parameters[SERIALIZER_VALUE] = json_plugin

        # retrieves the required controllers
        web_mvc_manager_repository_repository_controller = self.web_mvc_manager_repository.web_mvc_manager_repository_repository_controller

        # retrieves the form data by processing the form
        form_data_map = self.process_form_data(rest_request, DEFAULT_ENCODING)

        # retrieves the web search helper
        search_helper = parameters["search_helper"]

        # retrieves the repository index pattern
        repository_index = self.get_pattern(parameters, "repository_index", types.IntType)

        # retrieves the search values
        search_query = form_data_map["search_query"]
        start_record = form_data_map["start_record"]
        number_records = form_data_map["number_records"]

        # converts the the search values
        start_record = int(start_record)
        number_records = int(number_records)

        # retrieves the filtered repositories
        filtered_repository_containers = web_mvc_manager_repository_repository_controller._get_filtered_repository_containers(rest_request, search_query, repository_index)

        # retrieves the partial filter from the filtered repository containers
        partial_filtered_repository_containers, start_record, number_records, total_number_records = search_helper.partial_filter(rest_request, filtered_repository_containers, start_record, number_records)

        # retrieves the template file
        template_file = self.retrieve_template_file("repository_containers_partial_list_contents.html.tpl")

        # assigns the template variables
        template_file.assign("repository_containers", partial_filtered_repository_containers)
        template_file.assign("start_record", start_record)
        template_file.assign("number_records", number_records)
        template_file.assign("total_number_records", total_number_records)

        # assigns the session variables to the template file
        self.assign_session_template_file(rest_request, template_file)

        # applies the base path to the template file
        self.apply_base_path_template_file(rest_request, template_file)

        # processes the template file and sets the request contents
        self.process_set_contents(rest_request, template_file)

    @web_mvc_utils.serialize_exceptions("all")
    @web_mvc_utils.validated_method("repository.install_container")
    def handle_install_container_serialized(self, rest_request, parameters = {}):
        # retrieves the serializer
        serializer = parameters[SERIALIZER_VALUE]

        # retrieves the form data by processing the form
        form_data_map = self.process_form_data(rest_request, DEFAULT_ENCODING)

        # retrieves the communication helper
        communication_helper = parameters["communication_helper"]

        # retrieves the container id
        container_id = form_data_map["container_id"]

        # retrieves the container version
        container_version = form_data_map["container_version"]

        # install the container and retrieves the result
        install_container_result = self._install_container(rest_request, container_id, container_version)

        # serializes the install result using the serializer
        serialized_status = serializer.dumps(install_container_result)

        # sets the serialized status as the rest request contents
        self.set_contents(rest_request, serialized_status)

        # sends the serialized broadcast message
        communication_helper.send_serialized_broadcast_message(parameters, "web_mvc_manager/communication", "web_mvc_manager/plugin/install", serialized_status)

    def handle_install_container_json(self, rest_request, parameters = {}):
        # retrieves the json container
        json_plugin = self.web_mvc_manager_repository_plugin.json_plugin

        # sets the serializer in the parameters
        parameters[SERIALIZER_VALUE] = json_plugin

        # handles the request with the general
        # handle install container serialized method
        self.handle_install_container_serialized(rest_request, parameters)

    @web_mvc_utils.serialize_exceptions("all")
    @web_mvc_utils.validated_method("repository.uninstall_container")
    def handle_uninstall_container_serialized(self, rest_request, parameters = {}):
        # retrieves the serializer
        serializer = parameters[SERIALIZER_VALUE]

        # retrieves the form data by processing the form
        form_data_map = self.process_form_data(rest_request, DEFAULT_ENCODING)

        # retrieves the communication helper
        communication_helper = parameters["communication_helper"]

        # retrieves the container id
        container_id = form_data_map["container_id"]

        # retrieves the container version
        container_version = form_data_map["container_version"]

        # uninstall the container and retrieves the result
        uninstall_container_result = self._uninstall_container(rest_request, container_id, container_version)

        # serializes the uninstall result using the serializer
        serialized_status = serializer.dumps(uninstall_container_result)

        # sets the serialized status as the rest request contents
        self.set_contents(rest_request, serialized_status)

        # sends the serialized broadcast message
        communication_helper.send_serialized_broadcast_message(parameters, "web_mvc_manager/communication", "web_mvc_manager/plugin/install", serialized_status)

    def handle_uninstall_container_json(self, rest_request, parameters = {}):
        # retrieves the json plugin
        json_plugin = self.web_mvc_manager_repository_plugin.json_plugin

        # sets the serializer in the parameters
        parameters[SERIALIZER_VALUE] = json_plugin

        # handles the request with the general
        # handle uninstall container serialized method
        self.handle_uninstall_container_serialized(rest_request, parameters)

    def _install_container(self, rest_request, container_id, container_version):
        # retrieves the plugin manager
        plugin_manager = self.web_mvc_manager_repository_plugin.manager

        # retrieves the system updater plugin
        system_updater_plugin = self.web_mvc_manager_repository_plugin.system_updater_plugin

        # creates the delta plugin install map
        delta_plugin_install_map = {
            INSTALLED_VALUE : [],
            UNINSTALLED_VALUE : []
        }

        # retrieves the (beginning) list of available containers
        available_plugins_beginning = copy.copy(plugin_manager.get_all_plugins())

        # tries to install the container
        system_updater_plugin.install_container(container_id, container_version)

        # sleeps for a second to give time for the autoloader to update
        # this delay is induced on purpose
        time.sleep(INSTALLATION_DELAY)

        # retrieves the (end) list of available plugins
        available_plugins_end = plugin_manager.get_all_plugins()

        # iterates over all the plugins available at the beginning
        # to check if they exist in the current available plugins
        for available_plugin_beginning in available_plugins_beginning:
            if not available_plugin_beginning in available_plugins_end:
                delta_plugin_install_map[UNINSTALLED_VALUE].append(available_plugin_beginning.id)

        # iterates over all the plugins available at the end
        # to check if they exist in the previously available plugins
        for available_plugin_end in available_plugins_end:
            if not available_plugin_end in available_plugins_beginning:
                delta_plugin_install_map[INSTALLED_VALUE].append(available_plugin_end.id)

        # returns the delta plugin install map
        return delta_plugin_install_map

    def _uninstall_container(self, rest_request, container_id, container_version):
        # retrieves the plugin manager
        plugin_manager = self.web_mvc_manager_repository_plugin.manager

        # retrieves the system updater plugin
        system_updater_plugin = self.web_mvc_manager_repository_plugin.system_updater_plugin

        # creates the delta plugin install map
        delta_plugin_install_map = {
            INSTALLED_VALUE : [],
            UNINSTALLED_VALUE : []
        }

        # retrieves the (beginning) list of available plugins
        available_plugins_beginning = copy.copy(plugin_manager.get_all_plugins())

        # tries to uninstall the container
        system_updater_plugin.uninstall_container(container_id, container_version)

        # sleeps for a second to give time for the autoloader to update
        # this delay is induced on purpose
        time.sleep(INSTALLATION_DELAY)

        # retrieves the (end) list of available plugins
        available_plugins_end = plugin_manager.get_all_plugins()

        # iterates over all the plugins available at the beginning
        # to check if they exist in the current available plugins
        for available_plugin_beginning in available_plugins_beginning:
            if not available_plugin_beginning in available_plugins_end:
                delta_plugin_install_map[UNINSTALLED_VALUE].append(available_plugin_beginning.id)

        # iterates over all the plugins available at the end
        # to check if they exist in the previously available plugins
        for available_plugin_end in available_plugins_end:
            if not available_plugin_end in available_plugins_beginning:
                delta_plugin_install_map[INSTALLED_VALUE].append(available_plugin_end.id)

        # returns the delta plugin install map
        return delta_plugin_install_map
