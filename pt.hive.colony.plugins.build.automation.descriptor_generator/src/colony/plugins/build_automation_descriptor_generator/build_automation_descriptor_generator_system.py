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

__author__ = "Tiago Silva <tsilva@hive.pt>"
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

import os.path

import colony.base.plugin_system

AUTHOR_VALUE = "author"

BUILD_AUTOMATION_FILE_PATH_VALUE = "build_automation_file_path"

CAPABILITIES_VALUE = "capabilities"

CAPABILITIES_ALLOWED_VALUE = "capabilities_allowed"

DEPENDENCIES_VALUE = "dependencies"

DESCRIPTION_VALUE = "description"

ID_VALUE = "id"

MAIN_FILE_VALUE = "main_file"

NAME_VALUE = "name"

PLATFORM_VALUE = "platform"

PLUGIN_DESCRIPTOR_VALUE = "plugin_descriptor"

PLUGINS_VALUE = "plugins"

PYTHON_VALUE = "python"

RESOURCES_VALUE = "resources"

SHORT_NAME_VALUE = "short_name"

SUB_PLATFORMS_VALUE = "sub_platforms"

VERSION_VALUE = "version"

DEFAULT_ENCODING = "utf-8"
""" The default encoding """

UNIX_DIRECTORY_SEPARATOR = "/"
""" The unix directory separator """

WINDOWS_DIRECTORY_SEPARATOR = "\\"
""" The windows directory separator """

TEMPLATES_PATH = "build_automation_descriptor_generator/resources/templates"
""" The templates path """

PLUGIN_DESCRIPTOR_DEPENDENCY_FORMAT = "{\"id\" : \"%s\", \"version\" : \"%s\"}"
""" The plugin descriptor dependency format """

PLUGIN_DESCRIPTOR_TEMPLATE_FILE_NAME = "plugin_descriptor_template.tpl"
""" The plugin descriptor template file name """

INIT_FILE_NAME = "__init__.py"
""" The init file name """

JSON_FILE_EXTENSION = ".json"
""" The json file extension """

PYTHON_FILE_EXTENSION = ".py"
""" The python file extension """

SYSTEM_FILE_NAME_ENDING = "_system.py"
""" The system file name ending """

PLUGIN_MODULE_NAME_ENDING = "_plugin"
""" The plugin module name ending """

RESOURCES_DIRECTORY = "/resources"
""" The resources directory """

RESOURCE_FILE_NAME_EXCLUSION_LIST = (".svn", "entries", "all-wcprops", "dir-prop-base")
""" The resource file name exclusion list """

RESOURCE_FILE_EXTENSION_EXCLUSION_LIST = (".svn-base", ".class", ".pyc", ".tmp")
""" The resource file extension exclusion list """

class BuildAutomationDescriptorGenerator:
    """
    The build automation descriptor generator class.
    """

    build_automation_descriptor_generator_plugin = None
    """ The build automation descriptor generator plugin """

    def __init__(self, build_automation_descriptor_generator_plugin):
        """
        Constructor of the class.

        @type build_automation_descriptor_generator_plugin: BuildAutomationValidatorPlugin
        @param build_automation_descriptor_generator_plugin: The build automation descriptor generator plugin
        """

        self.build_automation_descriptor_generator_plugin = build_automation_descriptor_generator_plugin

    def generate_plugin_descriptors(self):
        # retrieves all plugins
        plugins = self.build_automation_descriptor_generator_plugin.manager.get_all_plugins()

        # retrieves the template file path
        template_file_path = self.get_template_file_path()

        # generates plugin descriptors for all plugins
        for plugin in plugins:
            self._generate_plugin_descriptor(plugin, template_file_path)

    def generate_plugin_descriptor(self, plugin_id):
        # retrieves the specified plugin
        plugin = self.build_automation_descriptor_generator_plugin.manager._get_plugin_by_id(plugin_id)

        # retrieves the template file path
        template_file_path = self.get_template_file_path()

        # generates the plugin descriptor for the specified plugin
        self._generate_plugin_descriptor(plugin, template_file_path)

    def _generate_plugin_descriptor(self, plugin, template_file_path):
        # returns in case the plugin is already valid
        if self.build_automation_descriptor_generator_plugin.build_automation_validator_plugin.validate_build_automation_plugin(plugin.id):
            return

        # retrieves the plugin path
        plugin_path = self.build_automation_descriptor_generator_plugin.manager.get_plugin_path_by_id(plugin.id)

        # retrieves the plugin module name
        plugin_module_name = self.build_automation_descriptor_generator_plugin.manager.get_plugin_module_name_by_id(plugin.id)

        # converts the plugin path separators from the windows mode
        # to unix mode
        plugin_path = plugin_path.replace(WINDOWS_DIRECTORY_SEPARATOR, UNIX_DIRECTORY_SEPARATOR)

        # retrieves the plugin system file path
        plugin_system_file_path = self.get_plugin_system_file_path(plugin_path, plugin_module_name)

        # retrieves the plugin root directory path
        plugin_root_directory_path = self.get_plugin_root_directory_path(plugin_system_file_path)

        # validates the plugin descriptor file
        self._generate_plugin_descriptor_file(plugin, plugin_path, plugin_module_name, template_file_path, plugin_system_file_path, plugin_root_directory_path)

    def _generate_plugin_descriptor_file(self, plugin, plugin_path, plugin_module_name, template_file_path, plugin_system_file_path, plugin_root_directory_path):
        # initializes the plugin descriptor map
        plugin_descriptor_map = {}

        # sets the base plugin descriptor attributes
        plugin_descriptor_map[PLATFORM_VALUE] = PYTHON_VALUE
        plugin_descriptor_map[ID_VALUE] = plugin.id
        plugin_descriptor_map[NAME_VALUE] = plugin.name
        plugin_descriptor_map[SHORT_NAME_VALUE] = plugin.short_name
        plugin_descriptor_map[DESCRIPTION_VALUE] = plugin.description
        plugin_descriptor_map[VERSION_VALUE] = plugin.version
        plugin_descriptor_map[AUTHOR_VALUE] = plugin.author

        # creates a string version of the sub platforms allowed attribute
        plugin_descriptor_sub_platforms_string = self.stringify_attribute(plugin.platforms)

        # sets the sub platforms attribute
        plugin_descriptor_map[SUB_PLATFORMS_VALUE] = plugin_descriptor_sub_platforms_string

        # creates a string version of the capabilities attribute
        plugin_descriptor_capabilities_string = self.stringify_attribute(plugin.capabilities)

        # sets the capabilities in the plugin descriptor
        plugin_descriptor_map[CAPABILITIES_VALUE] = plugin_descriptor_capabilities_string

        # sets the capabilities allowed in the plugin descriptor
        plugin_descriptor_map[CAPABILITIES_ALLOWED_VALUE] = self.__generate_plugin_descriptor_file_capabilities_allowed_string(plugin)

        # generates the plugin descriptor file's dependencies
        plugin_descriptor_map[DEPENDENCIES_VALUE] = self.__generate_plugin_descriptor_file_dependencies_string(plugin)

        # retrieves the plugin file name
        plugin_file_name = plugin_module_name + PYTHON_FILE_EXTENSION

        # sets the main file in the plugin descriptor
        plugin_descriptor_map[MAIN_FILE_VALUE] = plugin_file_name

        # retrieves the plugin descriptor resources
        plugin_descriptor_resources = self.__generate_plugin_descriptor_file_resources(plugin_path, plugin_module_name, plugin_system_file_path, plugin_root_directory_path)

        # creates a string version of the resources attribute
        plugin_descriptor_resources_string = self.stringify_attribute(plugin_descriptor_resources)

        # sets the resources attribute in the plugin descriptor
        plugin_descriptor_map[RESOURCES_VALUE] = plugin_descriptor_resources_string

        # saves the plugin descriptor file
        self.save_plugin_descriptor_file(plugin_path, plugin_module_name, plugin_descriptor_map, template_file_path)

    def __generate_plugin_descriptor_file_capabilities_allowed_string(self, plugin):
        # creates a string representation of the plugin's capabilities allowed
        plugin_descriptor_capabilities_allowed_string = unicode(plugin.capabilities_allowed)

        # adds double quotes before each tuple
        plugin_descriptor_capabilities_allowed_string = plugin_descriptor_capabilities_allowed_string.replace("(", "\"(")

        # adds double quotes after each tuple
        plugin_descriptor_capabilities_allowed_string = plugin_descriptor_capabilities_allowed_string.replace(")", ")\"")

        # replaces quotes with double quotes at the beginning of each list
        plugin_descriptor_capabilities_allowed_string = plugin_descriptor_capabilities_allowed_string.replace("['", "[\"")

        # replaces quotes with double quotes at the end of each list
        plugin_descriptor_capabilities_allowed_string = plugin_descriptor_capabilities_allowed_string.replace("']", "\"]")

        # replaces quotes with double quotes
        plugin_descriptor_capabilities_allowed_string = plugin_descriptor_capabilities_allowed_string.replace("',", "\",")

        # replaces quotes with double quotes
        plugin_descriptor_capabilities_allowed_string = plugin_descriptor_capabilities_allowed_string.replace(", '", ", \"")

        # fixes tuple quotes
        plugin_descriptor_capabilities_allowed_string = plugin_descriptor_capabilities_allowed_string.replace("\", %d" % colony.base.plugin_system.SINGLETON_DIFFUSION_SCOPE, "', %d" % colony.base.plugin_system.SINGLETON_DIFFUSION_SCOPE)

        # fixes tuple quotes
        plugin_descriptor_capabilities_allowed_string = plugin_descriptor_capabilities_allowed_string.replace("\", %d" % colony.base.plugin_system.SAME_DIFFUSION_SCOPE, "', %d" % colony.base.plugin_system.SAME_DIFFUSION_SCOPE)

        # fixes tuple quotes
        plugin_descriptor_capabilities_allowed_string = plugin_descriptor_capabilities_allowed_string.replace("\", %d" % colony.base.plugin_system.NEW_DIFFUSION_SCOPE, "', %d" % colony.base.plugin_system.NEW_DIFFUSION_SCOPE)

        return plugin_descriptor_capabilities_allowed_string

    def __generate_plugin_descriptor_file_dependencies_string(self, plugin):
        # retrieves the plugin's dependencies
        plugin_dependencies = plugin.get_all_plugin_dependencies()

        # collects the plugin descriptor dependencies
        plugin_descriptor_dependencies = [PLUGIN_DESCRIPTOR_DEPENDENCY_FORMAT % (plugin_dependency.plugin_id, plugin_dependency.plugin_version) for plugin_dependency in plugin_dependencies]

        # creates a string representation of the plugin descriptor dependencies
        plugin_descriptor_dependencies_string = unicode(plugin_descriptor_dependencies)

        # removes the quotes from the start of the list
        plugin_descriptor_dependencies_string = plugin_descriptor_dependencies_string.replace("['", "[")

        # removes the quotes from the end of the list
        plugin_descriptor_dependencies_string = plugin_descriptor_dependencies_string.replace("']", "]")

        # removes the quotes from the start of the maps
        plugin_descriptor_dependencies_string = plugin_descriptor_dependencies_string.replace("'{", "{")

        # removes the quotes from the end of the maps
        plugin_descriptor_dependencies_string = plugin_descriptor_dependencies_string.replace("}'", "}")

        return plugin_descriptor_dependencies_string

    def __generate_plugin_descriptor_file_resources(self, plugin_path, plugin_module_name, plugin_system_file_path, plugin_root_directory_path):
        # retrieves a list of plugin resource file paths
        plugin_resource_file_paths = self.get_plugin_resource_file_paths(plugin_path, plugin_module_name, plugin_system_file_path, plugin_root_directory_path)

        return plugin_resource_file_paths

    def get_plugin_resource_file_paths(self, plugin_path, plugin_module_name, plugin_system_file_path, plugin_root_directory_path):
        # initializes the list of resource file paths
        resource_file_paths = []

        # retrieves the plugin file name
        plugin_file_name = plugin_module_name + PYTHON_FILE_EXTENSION

        # appends the plugin file name to the resource file paths
        resource_file_paths.append(plugin_file_name)

        # retrieves the root init file path
        plugin_root_init_file_path = plugin_root_directory_path + UNIX_DIRECTORY_SEPARATOR + INIT_FILE_NAME

        # adds the root init file path to the resource file paths
        resource_file_paths.append(plugin_root_init_file_path)

        # crawls the specified path indexing file paths by their file name
        for root, _directories, files in os.walk(plugin_system_file_path):
            for file in files:
                # converts the root path separators from the windows mode
                # to unix mode
                root = root.replace(WINDOWS_DIRECTORY_SEPARATOR, UNIX_DIRECTORY_SEPARATOR)

                # skips in case the file is in the exclusion list or has a file extension in the exclusion list
                if file in RESOURCE_FILE_NAME_EXCLUSION_LIST or self.get_file_extension(file) in RESOURCE_FILE_EXTENSION_EXCLUSION_LIST:
                    continue

                # retrieves the base main module path
                base_resource_path = root.replace(plugin_path, "")

                # retrieves the base resource file path
                base_resource_file_path = base_resource_path + UNIX_DIRECTORY_SEPARATOR + file

                # removes the first slash from the base resource file path
                base_resource_file_path = base_resource_file_path[1:]

                # skips in case the resource file path is already in the list
                if base_resource_file_path in resource_file_paths:
                    continue

                # adds the resource file path to the resource file paths
                resource_file_paths.append(base_resource_file_path)

        return resource_file_paths

    def stringify_attribute(self, attribute_value):
        # creates a string version of the attribute
        attribute_value_string = unicode(attribute_value)

        # removes all unicode indicators
        attribute_value_string = attribute_value_string.replace("[u'", "['")

        # removes all unicode indicators
        attribute_value_string = attribute_value_string.replace(", u'", ", '")

        # replaces all quotes with double quotes
        attribute_value_string = attribute_value_string.replace("'", "\"")

        return attribute_value_string

    def get_plugin_root_directory_path(self, plugin_system_file_path):
        # tokenizes the plugin system file path with the unix directory separator
        plugin_system_file_path_tokens = plugin_system_file_path.split(UNIX_DIRECTORY_SEPARATOR)

        # tokenizes the plugin system file path with the windows directory separator
        if len(plugin_system_file_path_tokens) == 1:
            plugin_system_file_path_tokens = plugin_system_file_path.split(WINDOWS_DIRECTORY_SEPARATOR)

        # retrieves the plugin directory root path
        plugin_directory_root_path = plugin_system_file_path_tokens[plugin_system_file_path_tokens.index(PLUGINS_VALUE) + 1]

        return plugin_directory_root_path

    def get_plugin_system_file_path(self, plugin_path, plugin_module_name):
        # retrieves the plugin system file name
        plugin_system_file_name = plugin_module_name[:-1 * len(PLUGIN_MODULE_NAME_ENDING)] + SYSTEM_FILE_NAME_ENDING

        # searches for the directory where the plugin system file is contained
        for root, _directories, files in os.walk(plugin_path):
            for file in files:
                if file == plugin_system_file_name:
                    # converts the root path separators from the windows mode
                    # to unix mode
                    root = root.replace(WINDOWS_DIRECTORY_SEPARATOR, UNIX_DIRECTORY_SEPARATOR)

                    return root

    def get_file_extension(self, file_path):
        # splits the file into base name and extension
        _base_name, extension = os.path.splitext(file_path)

        # returns the extension
        return extension

    def get_template_file_path(self):
        # retrieves the build automation descriptor generator plugin's path
        build_automation_descriptor_generator_plugin_path = self.build_automation_descriptor_generator_plugin.manager.get_plugin_path_by_id(self.build_automation_descriptor_generator_plugin.id)

        # retrieves the template path
        template_path = build_automation_descriptor_generator_plugin_path + UNIX_DIRECTORY_SEPARATOR + TEMPLATES_PATH

        # retrieves the template file path
        template_file_path = template_path + UNIX_DIRECTORY_SEPARATOR + PLUGIN_DESCRIPTOR_TEMPLATE_FILE_NAME

        return template_file_path

    def save_plugin_descriptor_file(self, plugin_path, plugin_module_name, plugin_descriptor_map, template_file_path):
        # parses the template file path
        template_file = self.build_automation_descriptor_generator_plugin.template_engine_manager_plugin.parse_file_path(template_file_path)

        # assigns an entity to the parsed template file
        template_file.assign(PLUGIN_DESCRIPTOR_VALUE, plugin_descriptor_map)

        # processes the template file
        processed_template_file = template_file.process()

        # decodes the processed template file into a unicode object
        processed_template_file_decoded = processed_template_file.decode(DEFAULT_ENCODING)

        # defines the plugin descriptor file name
        plugin_descriptor_file_name = plugin_module_name + JSON_FILE_EXTENSION

        # defines the plugin descriptor file path
        plugin_descriptor_file_path = plugin_path + UNIX_DIRECTORY_SEPARATOR + plugin_descriptor_file_name

        # opens the plugin descriptor file
        file = open(plugin_descriptor_file_path, "w")

        # writes the plugin descriptor template to the file
        file.write(processed_template_file_decoded)

        # closes the plugin descriptor file
        file.close()
