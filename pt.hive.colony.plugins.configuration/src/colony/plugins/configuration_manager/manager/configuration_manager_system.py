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

class ConfigurationManager:
    """
    The configuration manager class.
    """

    configuration_manager_plugin = None
    """ The configuration manager plugin """

    def __init__(self, configuration_manager_plugin):
        """
        Constructor of the class.

        @type configuration_manager_plugin: ConfigurationManagerPlugin
        @param configuration_manager_plugin: Thee configuration manager plugin.
        """

        self.configuration_manager_plugin = configuration_manager_plugin

    def configuration_model_provider_load(self, configuration_model_provider_plugin):
        # retrieves the plugin manager
        plugin_manager = self.configuration_manager_plugin.manager

        # retrieves the configuration model provider plugin id
        configuration_model_provider_plugin_id = configuration_model_provider_plugin.id

        # retrieves the configuration models bundle
        configuration_models_bundle = configuration_model_provider_plugin.get_configuration_property("configuration_models_bundle", {})

        # retrieves the plugin path
        plugin_path = plugin_manager.get_plugin_path_by_id(configuration_model_provider_plugin_id)

        # retrieves the plugin configuration paths
        plugin_configuration_paths = plugin_manager.get_plugin_configuration_paths_by_id(configuration_model_provider_plugin_id)

        # unpacks the plugin configuration paths to get the global and the profile
        # configuration paths
        plugin_global_configuration_path, plugin_profile_configuration_path = plugin_configuration_paths

        # iterates over the configuration models bundle
        for configuration_model in configuration_models_bundle:

            configuration_model_properties = configuration_models_bundle[configuration_model]

            global_value = configuration_model_properties.get("global", False)

            replace_value = configuration_model_properties.get("replace", False)

            if global_value:
                configuration_model_target_path = plugin_global_configuration_path + "/" + configuration_model
            else:
                configuration_model_target_path = plugin_profile_configuration_path + "/" + configuration_model

            # in case the configuration model target path does not exists
            # or the replace flag is active
            if not os.path.exists(configuration_model_target_path) or replace_value:
                configuration_model_file = open(plugin_path + "/" + configuration_model, "rb")

                configuration_model_target_file = open(plugin_path + "/" + configuration_model, "wb")

                configuration_model_file_contents = configuration_model_file.read()

                configuration_model_file.close()

                configuration_model_target_file.write(configuration_model_file_contents)

                configuration_model_target_file.close()

    def configuration_model_provider_unload(self, configuration_model_provider_plugin):
        pass
