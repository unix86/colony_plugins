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

DEFAULT_ENCODING = "utf-8"
""" The default encoding value """

WEB_MVC_MANAGER_RESOURCES_PATH = "web_mvc_manager/manager/resources"
""" The web mvc manager resources path """

TEMPLATES_PATH = WEB_MVC_MANAGER_RESOURCES_PATH + "/templates"
""" The templates path """

AJAX_ENCODER_NAME = "ajx"
""" The ajax encoder name """

JSON_ENCODER_NAME = "json"
""" The json encoder name """

class SidePanelController:
    """
    The side panel controller.
    """

    web_mvc_manager_plugin = None
    """ The web mvc manager plugin """

    web_mvc_manager = None
    """ The web mvc manager """

    def __init__(self, web_mvc_manager_plugin, web_mvc_manager):
        """
        Constructor of the class.

        @type web_mvc_manager_plugin: WebMvcManagerPlugin
        @param web_mvc_manager_plugin: The web mvc manager plugin.
        @type web_mvc_manager: WebMvcManager
        @param web_mvc_manager: The web mvc manager.
        """

        self.web_mvc_manager_plugin = web_mvc_manager_plugin
        self.web_mvc_manager = web_mvc_manager

    def start(self):
        """
        Method called upon structure initialization.
        """

        # retrieves the plugin manager
        plugin_manager = self.web_mvc_manager_plugin.manager

        # retrieves the web mvc manager plugin path
        web_mvc_manager_plugin_path = plugin_manager.get_plugin_path_by_id(self.web_mvc_manager_plugin.id)

        # creates the templates path
        templates_path = web_mvc_manager_plugin_path + "/" + TEMPLATES_PATH + "/side_panel"

        # sets the templates path
        self.set_templates_path(templates_path)

    def handle_configuration(self, rest_request, parameters = {}):
        """
        Handles the given configuration rest request.

        @type rest_request: RestRequest
        @param rest_request: The take the bill index rest request
        to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        @rtype: bool
        @return: The result of the handling.
        """

        # retrieves the template file
        template_file = self.retrieve_template_file("side_panel_configuration.html.tpl")

        # assigns the configuration variables
        self._assign_configuration_variables(template_file)

        # applies the base path to the template file
        self.apply_base_path_template_file(rest_request, template_file)

        # processes the template file and sets the request contents
        self.process_set_contents(rest_request, template_file)

        # returns true
        return True

    def _assign_configuration_variables(self, template_file):
        # retrieves the plugin manager
        plugin_manager = self.web_mvc_manager_plugin.manager

        # assigns the plugin count to the template
        template_file.assign("plugin_count", len(plugin_manager.get_all_plugins()))

        # assigns the plugin loaded count to the template
        template_file.assign("plugin_loaded_count", len(plugin_manager.get_all_loaded_plugins()))

        # assigns the capabilities count to the template
        template_file.assign("capabilities_count", len(plugin_manager.capabilities_plugins_map))

        import psutil
        import os
        import time

        pid = os.getpid()

        process = psutil.Process(pid)

        memory_usage = process.get_memory_info()[0] / 1048576

        cpu_usage = process.get_cpu_percent()

        # assigns the memory usage to the template
        template_file.assign("memory_usage", memory_usage)

        # assigns the cpu usage to the template
        template_file.assign("cpu_usage", cpu_usage)

        current_time = time.time()

        uptime = current_time - plugin_manager.plugin_manager_timestamp

        uptime_string = str(int(uptime)) + "s"

        # assigns the uptime to the template
        template_file.assign("uptime", uptime_string)

class PluginController:
    """
    The web mvc manager plugin controller.
    """

    web_mvc_manager_plugin = None
    """ The web mvc manager plugin """

    web_mvc_manager = None
    """ The web mvc manager """

    def __init__(self, web_mvc_manager_plugin, web_mvc_manager):
        """
        Constructor of the class.

        @type web_mvc_manager_plugin: WebMvcManagerPlugin
        @param web_mvc_manager_plugin: The web mvc manager plugin.
        @type web_mvc_manager: WebMvcManager
        @param web_mvc_manager: The web mvc manager.
        """

        self.web_mvc_manager_plugin = web_mvc_manager_plugin
        self.web_mvc_manager = web_mvc_manager

    def start(self):
        """
        Method called upon structure initialization.
        """

        # retrieves the plugin manager
        plugin_manager = self.web_mvc_manager_plugin.manager

        # retrieves the web mvc manager plugin path
        web_mvc_manager_plugin_path = plugin_manager.get_plugin_path_by_id(self.web_mvc_manager_plugin.id)

        # creates the templates path
        templates_path = web_mvc_manager_plugin_path + "/" + TEMPLATES_PATH + "/plugin"

        # sets the templates path
        self.set_templates_path(templates_path)

    def handle_new(self, rest_request, parameters = {}):
        # returns in case the required permissions are not set
        if not self.web_mvc_manager.require_permissions(self, rest_request):
            return True

        # creates a new company in case this is a post request
        if rest_request.is_post():
            pass
            # retrieves the contents
            #contents = rest_request.request.read()

            # tenho de sacar o temp file do plugin manager
            # tenho de criar um ficheiro temporario e tenho de instalar o cenas
            # com base nisso

#            try:
#                # retrieves the template file
#                template_file = self.retrieve_template_file("company_edit_contents.html.tpl")
#
#                # creates the company
#                company = self._create_company(rest_request)
#
#                # assigns the company to the template
#                template_file.assign("company", company)
#
#                # assigns the result message to the template
#                template_file.assign("result_message", "Empresa criada com sucesso.")
#            except take_the_bill_main_exceptions.EntityValidationFailed, exception:
#                # retrieves the template file
#                template_file = self.retrieve_template_file("company_new_contents.html.tpl")
#
#                # retrieves the company from the exception
#                company = exception.entity
#
#                # assigns the company to the template
#                template_file.assign("company", company)
#
#                # assigns the result message to the template
#                template_file.assign("result_message", "Ocorreu um erro ao criar a empresa.")

        # in case the encoder name is ajax
        if rest_request.encoder_name == AJAX_ENCODER_NAME:
            # retrieves the template file
            template_file = self.retrieve_template_file("plugin_new_contents.html.tpl")
        else:
            # retrieves the template file
            template_file = self.retrieve_template_file("../general.html.tpl")

            # sets the page to be included
            template_file.assign("page_include", "plugin/plugin_new_contents.html.tpl")

            # sets the side panel to be included
            template_file.assign("side_panel_include", "side_panel/side_panel_configuration.html.tpl")

        # assigns the session variables to the template file
        self.assign_session_template_file(rest_request, template_file)

        # applies the base path to the template file
        self.apply_base_path_template_file(rest_request, template_file)

        # processes the template file and sets the request contents
        self.process_set_contents(rest_request, template_file)

        # returns true
        return True

    def handle_show(self, rest_request, parameters = {}):
        # returns in case the required permissions are not set
        if not self.web_mvc_manager.require_permissions(self, rest_request):
            return True

        # in case the encoder name is ajax
        if rest_request.encoder_name == AJAX_ENCODER_NAME:
            # retrieves the template file
            template_file = self.retrieve_template_file("plugin_edit_contents.html.tpl")
        else:
            # retrieves the template file
            template_file = self.retrieve_template_file("../general.html.tpl")

            # sets the page to be included
            template_file.assign("page_include", "plugin/plugin_edit_contents.html.tpl")

            # sets the side panel to be included
            template_file.assign("side_panel_include", "side_panel/side_panel_configuration.html.tpl")

        # retrieves the specified plugin
        plugin = self._get_plugin(rest_request)

        # assigns the plugin to the template
        template_file.assign("plugin", plugin)

        # assigns the session variables to the template file
        self.assign_session_template_file(rest_request, template_file)

        # applies the base path to the template file
        self.apply_base_path_template_file(rest_request, template_file)

        # processes the template file and sets the request contents
        self.process_set_contents(rest_request, template_file)

        # returns true
        return True

    def handle_list(self, rest_request, parameters = {}):
        # returns in case the required permissions are not set
        if not self.web_mvc_manager.require_permissions(self, rest_request):
            return True

        # in case the encoder name is ajax
        if rest_request.encoder_name == AJAX_ENCODER_NAME:
            # retrieves the template file
            template_file = self.retrieve_template_file("plugin_list_contents.html.tpl")
        else:
            # retrieves the template file
            template_file = self.retrieve_template_file("../general.html.tpl")

            # sets the page to be included
            template_file.assign("page_include", "plugin/plugin_list_contents.html.tpl")

            # sets the side panel to be included
            template_file.assign("side_panel_include", "side_panel/side_panel_configuration.html.tpl")

            # assigns the configuration (side panel) variable to the template
            self.web_mvc_manager.web_mvc_manager_side_panel_controller._assign_configuration_variables(template_file)

        # retrieves the plugin manager
        plugin_manager = self.web_mvc_manager_plugin.manager

        # assigns the plugins to the template
        template_file.assign("plugins", plugin_manager.get_all_plugins())

        # assigns the session variables to the template file
        self.assign_session_template_file(rest_request, template_file)

        # applies the base path to the template file
        self.apply_base_path_template_file(rest_request, template_file)

        # processes the template file and sets the request contents
        self.process_set_contents(rest_request, template_file)

        # returns true
        return True

    def handle_change_status(self, rest_request, parameters = {}):
        # returns in case the required permissions are not set
        if not self.web_mvc_manager.require_permissions(self, rest_request):
            return True

        # in case the encoder name is ajax
        if rest_request.encoder_name == JSON_ENCODER_NAME:
            # changes the plugin status and retrieves the result
            change_status_plugin_result = self._change_status_plugin(rest_request)

            # retrieves the json plugin
            json_plugin = self.web_mvc_manager_plugin.json_plugin

            # serializes the change status result using the json plugin
            serialized_status = json_plugin.dumps(change_status_plugin_result)

            # sets the serialized status as the rest request contents
            self.set_contents(rest_request, serialized_status)

            return True

        # returns true
        return True

    def _get_plugin(self, rest_request):
        # retrieves the plugin manager
        plugin_manager = self.web_mvc_manager_plugin.manager

        # retrieves the plugin's id from the rest request's path list
        plguin_id = rest_request.path_list[-1]

        # retrieves the plugin from the given plugin id
        plugin = plugin_manager._get_plugin_by_id(plguin_id)

        return plugin

    def _change_status_plugin(self, rest_request):
        # retrieves the plugin manager
        plugin_manager = self.web_mvc_manager_plugin.manager

        # processes the form data
        form_data_map = self.process_form_data(rest_request, DEFAULT_ENCODING)

        # partitions the form data
        plugin_id = form_data_map["plugin_id"]
        plugin_status = form_data_map["plugin_status"]

        import copy

        all_loaded_plugins_initial = copy.copy(plugin_manager.get_all_loaded_plugins())

        if plugin_status == "load":
            plugin_manager.load_plugin(plugin_id)
        elif plugin_status == "unload":
            plugin_manager.unload_plugin(plugin_id)

        all_loaded_plugins = plugin_manager.get_all_loaded_plugins()

        map = {"unloaded" : [], "loaded" : []}

        for loaded_plugin_initial in all_loaded_plugins_initial:
            if not loaded_plugin_initial in all_loaded_plugins:
                map["unloaded"].append(loaded_plugin_initial.id)

        for loaded_plugin in all_loaded_plugins:
            if not loaded_plugin in all_loaded_plugins_initial:
                map["loaded"].append(loaded_plugin.id)

        return map

class CapabilityController:
    """
    The web mvc manager capability controller.
    """

    web_mvc_manager_plugin = None
    """ The web mvc manager plugin """

    web_mvc_manager = None
    """ The web mvc manager """

    def __init__(self, web_mvc_manager_plugin, web_mvc_manager):
        """
        Constructor of the class.

        @type web_mvc_manager_plugin: WebMvcManagerPlugin
        @param web_mvc_manager_plugin: The web mvc manager plugin.
        @type web_mvc_manager: WebMvcManager
        @param web_mvc_manager: The web mvc manager.
        """

        self.web_mvc_manager_plugin = web_mvc_manager_plugin
        self.web_mvc_manager = web_mvc_manager

    def start(self):
        """
        Method called upon structure initialization.
        """

        # retrieves the plugin manager
        plugin_manager = self.web_mvc_manager_plugin.manager

        # retrieves the web mvc manager plugin path
        web_mvc_manager_plugin_path = plugin_manager.get_plugin_path_by_id(self.web_mvc_manager_plugin.id)

        # creates the templates path
        templates_path = web_mvc_manager_plugin_path + "/" + TEMPLATES_PATH + "/capability"

        # sets the templates path
        self.set_templates_path(templates_path)

    def handle_show(self, rest_request, parameters = {}):
        # returns in case the required permissions are not set
        if not self.web_mvc_manager.require_permissions(self, rest_request):
            return True

        # in case the encoder name is ajax
        if rest_request.encoder_name == AJAX_ENCODER_NAME:
            # retrieves the template file
            template_file = self.retrieve_template_file("capability_edit_contents.html.tpl")
        else:
            # retrieves the template file
            template_file = self.retrieve_template_file("../general.html.tpl")

            # sets the page to be included
            template_file.assign("page_include", "capability/capability_edit_contents.html.tpl")

            # sets the side panel to be included
            template_file.assign("side_panel_include", "side_panel/side_panel_configuration.html.tpl")

        # retrieves the specified capability
        capability = self._get_capability(rest_request)

        # retrieves the plugins map for the capability
        plugins_capability = self._get_plugins_capability(capability)

        # retrieves the sub capabilities for the capability
        sub_capabilities = self._get_sub_capabilities(capability)

        # assigns the capability to the template
        template_file.assign("capability", capability)

        # assigns the plugins capability to the template
        template_file.assign("plugins_capability", plugins_capability)

        # assigns the sub capabilities to the template
        template_file.assign("sub_capabilities", sub_capabilities)

        # assigns the session variables to the template file
        self.assign_session_template_file(rest_request, template_file)

        # applies the base path to the template file
        self.apply_base_path_template_file(rest_request, template_file)

        # processes the template file and sets the request contents
        self.process_set_contents(rest_request, template_file)

        # returns true
        return True

    def handle_list(self, rest_request, parameters = {}):
        # returns in case the required permissions are not set
        if not self.web_mvc_manager.require_permissions(self, rest_request):
            return True

        # in case the encoder name is ajax
        if rest_request.encoder_name == AJAX_ENCODER_NAME:
            # retrieves the template file
            template_file = self.retrieve_template_file("capability_list_contents.html.tpl")
        else:
            # retrieves the template file
            template_file = self.retrieve_template_file("../general.html.tpl")

            # sets the page to be included
            template_file.assign("page_include", "capability/capability_list_contents.html.tpl")

            # sets the side panel to be included
            template_file.assign("side_panel_include", "side_panel/side_panel_configuration.html.tpl")

        # retrieves the capabilities
        capabilities = self._get_capabilities()

        # assigns the plugins to the template
        template_file.assign("capabilities", capabilities)

        # assigns the session variables to the template file
        self.assign_session_template_file(rest_request, template_file)

        # applies the base path to the template file
        self.apply_base_path_template_file(rest_request, template_file)

        # processes the template file and sets the request contents
        self.process_set_contents(rest_request, template_file)

        # returns true
        return True

    def _get_capabilities(self):
        # retrieves the plugin manager
        plugin_manager = self.web_mvc_manager_plugin.manager

        # retrieves all the capabilities
        capabilities = plugin_manager.capabilities_plugin_instances_map.keys()

        # sorts all the capabilities
        capabilities.sort()

        return capabilities

    def _get_capability(self, rest_request):
        # retrieves the capability from the rest request's path list
        capability = rest_request.path_list[-1]

        return capability

    def _get_plugins_capability(self, capability):
        # retrieves the plugin manager
        plugin_manager = self.web_mvc_manager_plugin.manager

        # retrieves the plugins providing the capability
        plugins_offering = list(set(plugin_manager.capabilities_plugin_instances_map.get(capability, [])))

        # retrieves the plugins allowing the capability
        plugins_allowing = list(set(plugin_manager.capabilities_plugins_map.get(capability, [])))

        # creates an unique set of plugins offering the capability
        plugins_offering_unique = set(plugins_offering)

        # creates an unique set of plugins allowing the capability
        plugins_allowing_unique = set(plugins_allowing)

        return {"providing" : plugins_offering_unique, "allowing" : plugins_allowing_unique}

    def _get_sub_capabilities(self, capability):
        # retrieves the plugin manager
        plugin_manager = self.web_mvc_manager_plugin.manager

        # retrieves the sub capabilities for the capability
        sub_capabilities = plugin_manager.capabilities_sub_capabilities_map.get(capability, [])

        return sub_capabilities
